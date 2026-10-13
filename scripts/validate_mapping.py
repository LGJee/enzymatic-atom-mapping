"""Check reaction structures and mapping bookkeeping; do not infer a mechanism."""
import argparse
import json
import sys
from collections import Counter

from rdkit import Chem, rdBase


def parse_reaction(text):
    """Parse strict molecular SMILES while retaining explicit and isotopic H."""
    if text.count(">>") != 1:
        raise ValueError("Use exactly one reactant>>product separator.")
    sides = []
    params = Chem.SmilesParserParams()
    params.parseName = False
    params.allowCXSMILES = False
    params.removeHs = False
    for side in text.split(">>"):
        if not side.strip():
            raise ValueError("Both reaction sides must contain structures.")
        molecules = []
        for fragment in side.split("."):
            molecule = Chem.MolFromSmiles(fragment.strip(), params)
            if molecule is None:
                raise ValueError("Invalid molecular SMILES: " + fragment)
            if any(a.GetAtomicNum() == 0 for a in molecule.GetAtoms()):
                raise ValueError("Resolve wildcard atoms before atom-level validation.")
            molecules.append(molecule)
        sides.append(molecules)
    return sides


def signature(molecule):
    copy = Chem.Mol(molecule)
    for atom in copy.GetAtoms():
        atom.SetAtomMapNum(0)
    # Explicit ordinary H is a representation choice; isotopic H is retained.
    copy = Chem.RemoveHs(copy)
    return Chem.MolToSmiles(copy, canonical=True, isomericSmiles=True)


def inventory(molecules):
    elements = Counter()
    isotopes = Counter()
    for molecule in molecules:
        for atom in Chem.AddHs(molecule).GetAtoms():
            elements[atom.GetSymbol()] += 1
            if atom.GetIsotope():
                isotopes[str(atom.GetIsotope()) + atom.GetSymbol()] += 1
    return elements, isotopes


def difference(left, right):
    return {key: right[key] - left[key] for key in sorted(left.keys() | right.keys())
            if right[key] != left[key]}


def map_index(molecules):
    index = {}
    for molecule in molecules:
        for atom in molecule.GetAtoms():
            number = atom.GetAtomMapNum()
            if number > 0:
                if number in index:
                    raise ValueError("Duplicate positive atom-map identifier: " + str(number))
                index[number] = atom
    return index


def validate_mapping(reaction, mapped=None, scope="all"):
    if scope not in ("all", "carbon", "heavy"):
        raise ValueError("Scope must be all, heavy, or carbon.")
    original = parse_reaction(reaction)
    inventories = [inventory(side) for side in original]
    element_delta = difference(inventories[0][0], inventories[1][0])
    isotope_delta = difference(inventories[0][1], inventories[1][1])
    charges = [sum(Chem.GetFormalCharge(m) for m in side) for side in original]
    balance = {
        "element_difference_products_minus_reactants": element_delta,
        "isotope_difference_products_minus_reactants": isotope_delta,
        "formal_charge_difference_products_minus_reactants": charges[1] - charges[0],
        "balanced": not element_delta and not isotope_delta and charges[0] == charges[1],
    }
    report = {
        "rdkit_version": rdBase.rdkitVersion,
        "status": "input_checked",
        "input_balance": balance,
        "warnings": [],
        "mechanistic_correctness": "not_assessed",
    }
    if not balance["balanced"]:
        report["warnings"].append(
            "Input is unbalanced as supplied; no structures or components were changed.")
    if mapped is None:
        return report

    candidate = parse_reaction(mapped)
    for side_number, (before, after) in enumerate(zip(original, candidate), start=1):
        if Counter(map(signature, before)) != Counter(map(signature, after)):
            raise ValueError(
                "Mapped side {} changes supplied structures, stereochemistry, "
                "charges, isotopes, or component multiplicity.".format(side_number))

    indices = [map_index(side) for side in candidate]
    for number in indices[0].keys() & indices[1].keys():
        left, right = indices[0][number], indices[1][number]
        if (left.GetAtomicNum(), left.GetIsotope()) != (
                right.GetAtomicNum(), right.GetIsotope()):
            raise ValueError("Atom-map identifier {} changes element or isotope.".format(number))

    required_ids = []
    coverage = []
    for side in candidate:
        carbons = [a for m in side for a in m.GetAtoms() if a.GetAtomicNum() == 6]
        heavy = [a for m in side for a in m.GetAtoms() if a.GetAtomicNum() > 1]
        atoms = [a for m in side for a in m.GetAtoms()]
        required = {"carbon": carbons, "heavy": heavy, "all": atoms}[scope]
        if any(a.GetAtomMapNum() <= 0 for a in required):
            raise ValueError("Every atom in scope {} must have a positive map identifier.".format(scope))
        required_ids.append({a.GetAtomMapNum() for a in required})
        hydrogens = [a for a in atoms if a.GetAtomicNum() == 1]
        coverage.append({
            "represented_atoms": len(atoms),
            "mapped_represented_atoms": sum(a.GetAtomMapNum() > 0 for a in atoms),
            "explicit_hydrogen_atoms": len(hydrogens),
            "mapped_explicit_hydrogen_atoms": sum(a.GetAtomMapNum() > 0 for a in hydrogens),
            "carbon_atoms": len(carbons),
            "mapped_carbon_atoms": sum(a.GetAtomMapNum() > 0 for a in carbons),
            "heavy_atoms": len(heavy),
            "mapped_heavy_atoms": sum(a.GetAtomMapNum() > 0 for a in heavy),
        })
    if required_ids[0] != required_ids[1]:
        raise ValueError("Required atom identifiers are not conserved between reaction sides.")

    report.update(status="structural_checks_passed", scope=scope,
                  reactant_coverage=coverage[0], product_coverage=coverage[1])
    if scope == "carbon":
        report["warnings"].append(
            "Complete carbon bookkeeping does not establish other-element correspondence.")
    report["warnings"].append(
        "Passing these checks does not establish biochemical or experimental correctness.")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reaction", required=True, help="Original reactant>>product SMILES")
    parser.add_argument("--mapped", help="Candidate atom-mapped reaction SMILES")
    parser.add_argument("--scope", choices=("all", "heavy", "carbon"), default="all",
                        help="all: every represented atom, including explicit H (default); implicit H is not expanded")
    args = parser.parse_args()
    try:
        report = validate_mapping(args.reaction, args.mapped, args.scope)
    except ValueError as error:
        print(json.dumps({"status": "invalid", "error": str(error)}, indent=2))
        return 2
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
