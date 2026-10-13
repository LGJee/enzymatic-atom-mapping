# Enzymatic Atom Mapping Skill

An English-language Codex skill for evidence-guided atom mapping of enzymatic
reaction SMILES, with particular emphasis on carbon transfer.

It combines an agent's biochemical research workflow with a small RDKit
validator. It is **not** a pretrained mapper, an automatic literature oracle, or
a guarantee of exact isotope trajectories. A structurally consistent mapping
can still be mechanistically wrong.

## Installation

### Install automatically with Codex (recommended)

Open Codex and paste this request into the chat:

~~~text
Use $skill-installer to install the skill from:
https://github.com/LGJee/enzymatic-atom-mapping

The SKILL.md file is at the repository root. Install that root directory
as a skill named enzymatic-atom-mapping in my user skills directory.
If using install-skill-from-github.py, use:
--repo LGJee/enzymatic-atom-mapping --path . --name enzymatic-atom-mapping
~~~

Codex uses its bundled installer to download the files and install the skill.
Allow network access if your Codex permission settings require it. No manual
download or Git command is needed. If the skill is already installed, the
installer stops instead of overwriting it; ask Codex to review an update.

The skill should be available on your next turn. If it does not appear,
restart Codex. See the [official skill installation guide](https://learn.chatgpt.com/docs/build-skills#install-curated-skills-for-local-use).

### Install manually

Alternatively, download this repository using **Code > Download ZIP**, extract
it, and rename the extracted folder to `enzymatic-atom-mapping`. Place the folder
in your Codex user skills directory:

- Current documented location: `~/.agents/skills/` on macOS/Linux, or
  `%USERPROFILE%\.agents\skills\` on Windows.
- Releases whose bundled installer uses `$CODEX_HOME/skills` default to
  `~/.codex/skills/`, or `%USERPROFILE%\.codex\skills\` on Windows.

Use the location supported by your Codex installation, and install only one
copy. `SKILL.md` must be directly inside `enzymatic-atom-mapping`, not in an extra
nested folder. Do not overwrite an existing skill without reviewing it.

### Dependencies

Installing the skill does not install Python, RDKit, or optional mapper models.
For automated structural validation, use Python 3.9 or later with RDKit; see
[Validate a candidate](#validate-a-candidate) below. You can also ask Codex:

~~~text
Check the dependencies for $enzymatic-atom-mapping and install RDKit in a
dedicated environment if it is missing. Run the bundled validator tests.
~~~

## Use the skill

After installation, paste a request such as:

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
