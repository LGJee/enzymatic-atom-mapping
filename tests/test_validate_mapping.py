"""Structural regression tests, not a biochemical accuracy benchmark."""
import importlib.util
import unittest
from pathlib import Path

from rdkit import Chem

path = Path(__file__).resolve().parents[1] / "scripts" / "validate_mapping.py"
spec = importlib.util.spec_from_file_location("validate_mapping", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
validate = module.validate_mapping

FBP = (
    "C([C@@H]1[C@H]([C@@H]([C@](O1)(COP(=O)([O-])[O-])O)O)O)"
    "OP(=O)([O-])[O-]"
)
DHAP = "C(C(=O)COP(=O)(O)O)O"
GAP = "C(C(C=O)O)OP(=O)(O)O"
REACTION = FBP + ">>" + DHAP + "." + GAP


def carbon_map(smiles, numbers):
    molecule = Chem.MolFromSmiles(smiles)
    carbons = [a for a in molecule.GetAtoms() if a.GetAtomicNum() == 6]
    assert len(carbons) == len(numbers)
    for atom, number in zip(carbons, numbers):
        atom.SetAtomMapNum(number)
    return Chem.MolToSmiles(molecule, isomericSmiles=True)


class MappingChecks(unittest.TestCase):
    def test_supplied_cleavage_and_protonation_warning(self):
        # Numbers here denote FBP carbon positions, assigned from its connectivity.
        mapped = (
            carbon_map(FBP, [6, 5, 4, 3, 2, 1]) + ">>" +
            carbon_map(DHAP, [3, 2, 1]) + "." + carbon_map(GAP, [6, 5, 4])
        )
        report = validate(REACTION, mapped)
        self.assertEqual(report["status"], "structural_checks_passed")
        self.assertEqual(report["product_coverage"]["mapped_carbon_atoms"], 6)
        self.assertEqual(
            report["input_balance"]["element_difference_products_minus_reactants"], {"H": 4})
        self.assertEqual(
            report["input_balance"]["formal_charge_difference_products_minus_reactants"], 4)
        self.assertEqual(report["mechanistic_correctness"], "not_assessed")
        with self.assertRaises(ValueError):
            validate(REACTION, mapped, scope="heavy")

    def test_formal_phosphate_transfer_all_heavy_atoms(self):
        # A bookkeeping fixture; it is not an assertion of an enzyme mechanism.
        original = "CCO.OP(=O)(O)O>>CCOP(=O)(O)O.O"
        mapped = (
            "[CH3:1][CH2:2][OH:3].[OH:4][P:5](=[O:6])([OH:7])[OH:8]"
            ">>[CH3:1][CH2:2][O:3][P:5](=[O:6])([OH:7])[OH:8].[OH2:4]"
        )
        report = validate(original, mapped, "heavy")
        self.assertTrue(report["input_balance"]["balanced"])
        self.assertEqual(report["product_coverage"]["mapped_heavy_atoms"], 8)

    def test_triose_phosphate_isomerization(self):
        left = "O=CC(O)COP(=O)(O)O"
        right = "OCC(=O)COP(=O)(O)O"
        report = validate(left + ">>" + right,
                          carbon_map(left, [1, 2, 3]) + ">>" +
                          carbon_map(right, [1, 2, 3]))
        self.assertTrue(report["input_balance"]["balanced"])

    def test_symmetric_representatives(self):
        succinate = "O=C(O)CCC(=O)O"
        for numbers in ([1, 2, 3, 4], [4, 3, 2, 1]):
            result = validate(succinate + ">>" + succinate,
                              carbon_map(succinate, [1, 2, 3, 4]) + ">>" +
                              carbon_map(succinate, numbers))
            self.assertEqual(result["status"], "structural_checks_passed")

    def test_repeated_components_need_distinct_identifiers(self):
        validate("CO.CO>>CO.CO", "[CH3:1]O.[CH3:2]O>>[CH3:1]O.[CH3:2]O")
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            validate("CO.CO>>CO.CO", "[CH3:1]O.[CH3:1]O>>[CH3:1]O.[CH3:2]O")

    def test_element_mismatch(self):
        with self.assertRaisesRegex(ValueError, "element or isotope"):
            validate("CO>>CO", "[CH3:1][OH:2]>>[CH3:2][OH:1]", "heavy")

    def test_missing_and_unconserved_carbon(self):
        for candidate in ("[CH3:1]CO>>[CH3:1][CH2:2]O",
                          "[CH3:1][CH2:2]O>>[CH3:1][CH2:3]O"):
            with self.assertRaises(ValueError):
                validate("CCO>>CCO", candidate)

    def test_component_multiplicity_preserved(self):
        with self.assertRaisesRegex(ValueError, "multiplicity"):
            validate("CO.CO>>CO.CO", "[CH3:1]O>>[CH3:1]O")

    def test_charge_isotope_and_stereochemistry_preserved(self):
        with self.assertRaisesRegex(ValueError, "changes supplied"):
            validate("C[O-]>>C[O-]", "[CH3:1][O-]>>[CH3:1]O")
        with self.assertRaisesRegex(ValueError, "changes supplied"):
            validate("[13CH3]O>>[13CH3]O", "[13CH3:1]O>>[CH3:1]O")
        lactate = "C[C@H](O)C(=O)O"
        with self.assertRaisesRegex(ValueError, "changes supplied"):
            validate(lactate + ">>" + lactate,
                     carbon_map(lactate, [1, 2, 3]) + ">>" +
                     carbon_map("C[C@@H](O)C(=O)O", [1, 2, 3]))

    def test_invalid_input(self):
        for reaction in ("CCO", "CCO>>", "*CO>>*CO", "CO name>>CO", "C1CC>>CC"):
            with self.assertRaises(ValueError):
                validate(reaction)

    def test_structure_checks_cannot_certify_carbon_positions(self):
        # A carbon permutation can pass bookkeeping while lacking mechanistic support.
        result = validate("CCCO>>CCC=O",
                          "[CH3:1][CH2:2][CH2:3]O>>[CH3:3][CH2:2][CH:1]=O")
        self.assertEqual(result["status"], "structural_checks_passed")
        self.assertEqual(result["mechanistic_correctness"], "not_assessed")

    def test_explicit_ordinary_hydrogens_are_equivalent(self):
        result = validate("CO>>CO", "[CH3:1]O>>[H]O[CH3:1]")
        self.assertEqual(result["status"], "structural_checks_passed")


if __name__ == "__main__":
    unittest.main()
