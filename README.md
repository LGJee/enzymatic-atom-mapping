# Enzymatic Atom Mapping

An English-language Codex skill for evidence-guided atom mapping of enzymatic
reaction SMILES, with particular emphasis on carbon transfer.

It combines an agent's biochemical research workflow with a small RDKit
validator. It is **not** a pretrained mapper, an automatic literature oracle, or
a guarantee of exact isotope trajectories. A structurally consistent mapping
can still be mechanistically wrong.

## Install and invoke

Copy this repository into your Codex skills directory as
"enzymatic-atom-mapping" (normally ~/.codex/skills/enzymatic-atom-mapping).
Do not overwrite an existing skill without reviewing it. In a new session,
invoke it with:

~~~text
Use $enzymatic-atom-mapping to establish the carbon atom correspondence for:
C([C@@H]1[C@H]([C@@H]([C@](O1)(COP(=O)([O-])[O-])O)O)O)OP(=O)([O-])[O-]>>C(C(=O)COP(=O)(O)O)O.C(C(C=O)O)OP(=O)(O)O
Consult biochemical sources and primary literature. Preserve the supplied
structures and report any unresolved atom identities.
~~~

The agent needs web access to consult the sources. RDKit is needed only for
the bundled automated checks; candidate prediction tools are optional and are
not bundled. No service credentials or research datasets are included.

## Validate a candidate

Use Python 3.9 or later with RDKit. For example:

~~~bash
conda create -n atom-mapping python=3.11 rdkit -c conda-forge
conda activate atom-mapping
python scripts/validate_mapping.py --reaction 'CCO>>CCO' --mapped '[CH3:1][CH2:2]O>>[CH3:1][CH2:2]O'
python -m unittest discover -s tests -v
~~~

Alternatively, install the dependency with "python -m pip install -r requirements.txt".
All commands above are run from the repository root.

The CLI accepts --reaction, optional --mapped, and --scope carbon (default) or
--scope heavy. It returns JSON and exits with code 2 for invalid structures or
mapping bookkeeping; code 0 means only that the requested machine checks
passed. Input imbalance is reported as a warning without silently correcting
the reaction.

Checks cover:
- Recovery of the supplied structures after map removal, including component
  multiplicity, formal charges, isotopes, and specified stereochemistry.
- Unique positive map IDs on each side; consistent elements and isotopes for
  identifiers shared across sides.
- Complete, conserved carbon or heavy-atom identifiers for the selected scope.
- Elemental, isotopic, and formal charge balance of the supplied input.

These checks do not determine a catalytic mechanism, resolve positional
ambiguity, assess confidence, or establish correspondence of implicit hydrogens.
Different SMILES traversals and component orderings are allowed if the
underlying supplied structures are preserved.

## Results and evidence

The skill reports an evidence status, a scope-qualified mapped reaction,
carbon-position correspondences, relevant EC/database identifiers, source
links, and outstanding uncertainties. Atom-map numbers are reaction-local
labels; they are not automatically biochemical carbon numbers.

Source selection and representative verification cases are documented in
[references/evidence.md](references/evidence.md). The supplied FBP cleavage
example deliberately exposes a protonation imbalance; the checker detects it.
Unit tests include formal phosphate transfer, triose phosphate isomerization,
multi-product cleavage, symmetry, repeated components, and invalid mappings.
They are structural regression tests, **not** a biochemical accuracy benchmark.

## Research use and citation

Version 0.1.0. Maintainer: [LGJee](https://github.com/LGJee).
Use CITATION.cff for repository citation metadata. Record the version and exact
Git commit used in a study, and cite the original databases and literature that
support individual atom assignments. No DOI has been assigned.

No accuracy percentage is claimed. This release has not been benchmarked
against an independent, expert-curated set of enzymatic atom mappings.
Third-party data, mapper models, and their licenses are not included.

The original skill instructions and validator are distributed under the MIT
License. Please retain the source citations when reusing the evidence notes.
