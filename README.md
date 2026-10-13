# Enzymatic Atom Mapping Skill

Map all atoms represented in an enzymatic reaction SMILES by default: all heavy atoms and explicit hydrogen atoms. Implicit hydrogens remain implicit.
This Codex skill uses biochemical sources and a small structural checker.
It is an evidence-guided workflow, not a trained prediction model.

## Install

Paste this into Codex:

~~~text
$skill-installer
Install https://github.com/LGJee/enzymatic-atom-mapping-skill
Use the repository root as the skill named enzymatic-atom-mapping.
~~~

It should be available on your next turn. If it does not appear, restart Codex.
The installer does not overwrite an existing installation.

## Use

**Two steps: select the skill, then paste your reaction.**

1. Select **Enzymatic Atom Mapping** in your skill picker, or type
   `$enzymatic-atom-mapping`.
2. Paste the reaction SMILES in the same message.

~~~text
$enzymatic-atom-mapping
C([C@@H]1[C@H]([C@@H]([C@](O1)(COP(=O)([O-])[O-])O)O)O)OP(=O)([O-])[O-]>>C(C(=O)COP(=O)(O)O)O.C(C(C=O)O)OP(=O)(O)O
~~~

Copy this example to try the skill, or replace it with your own reaction.
If you selected the skill in the picker, paste only the reaction.

This example has different protonation states on the two sides.
The skill should report the imbalance without changing your structures.

SMILES describes a molecule as text. `>>` separates reactants from products;
`.` separates molecules on the same side. You do not need to number atoms first.

**To check a mapping you already have:**

~~~text
$enzymatic-atom-mapping
Check this mapping:
MAPPED_REACTION_SMILES
~~~

No long prompt is needed. Looking up biochemical evidence, preserving your
structures, and reporting uncertainty are already included in the skill.
Reaction names and EC numbers are optional; Codex will ask if the identity
is unclear. You can ask in Chinese or English; results are currently in English.

## What you get

- A table showing reactant-to-product atom correspondences for all mapped elements.
- An atom-mapped reaction SMILES with complete coverage when justified; symmetry-equivalent or model-only assignments are identified as representative or unverified.
- Source links and a clear explanation of any unresolved atom positions.

The agent needs web access for research. LocalMapper, RXNMapper, and EnzymeMap
are optional. Python with RDKit is needed only for automated structural checks.
Installing the skill does not install these dependencies.

<details>
<summary>Optional: manual installation</summary>

Download **Code > Download ZIP**, extract it, rename the folder to
`enzymatic-atom-mapping`, and place it in your Codex user skills directory:

- Current documented location: `~/.agents/skills/`, or
  `%USERPROFILE%\.agents\skills\` on Windows.
- Versions whose bundled installer uses `$CODEX_HOME/skills` default to
  `~/.codex/skills/`, or `%USERPROFILE%\.codex\skills\` on Windows.

Use the location supported by your Codex installation and install only one
copy. `SKILL.md` must be directly inside the skill folder.
See the [official guide](https://learn.chatgpt.com/docs/build-skills).

</details>

<details>
<summary>Advanced: run the structural checker and tests</summary>

Use Python 3.9 or later with RDKit. Run these from the repository root:

~~~bash
conda create -n atom-mapping python=3.11 rdkit -c conda-forge
conda activate atom-mapping
python scripts/validate_mapping.py --reaction 'CCO>>CCO' --mapped '[CH3:1][CH2:2][OH:3]>>[CH3:1][CH2:2][OH:3]'
python -m unittest discover -s tests -v
~~~

Alternatively, use `python -m pip install -r requirements.txt` in an existing
Python environment. Codex can also help check and install missing dependencies.

The checker accepts `--reaction`, optional `--mapped`, and `--scope all`
(default, heavy atoms plus explicit H). Use `--scope heavy` or `--scope carbon`
for a deliberately narrower check. It checks structure preservation, component
multiplicity, charges, isotopes, stereochemistry, map identifiers, and atom
coverage. Input imbalance is reported without silently correcting it.

It returns JSON. Exit code 2 means invalid structures or mapping bookkeeping;
code 0 means only that the machine checks passed. These checks cannot establish
the enzyme mechanism, resolve positional ambiguity, or certify accuracy.

</details>

## Research use and citation

Version 0.1.0. Maintainer: [LGJee](https://github.com/LGJee).
Use [CITATION.cff](CITATION.cff) and record the exact commit used in your study.
Also cite the original sources supporting each atom assignment.
No DOI has been assigned.

Atom-map identifiers are local to each reaction, not automatically biochemical
C1, C2, etc. A structurally consistent mapping can still be mechanistically
wrong. Unresolved assignments must remain qualified.

See [references/evidence.md](references/evidence.md) for evidence sources.
Tests are structural regression checks, not a biochemical accuracy benchmark.
No accuracy percentage is claimed. Third-party data and mapper models are
not included. The original skill and checker use the MIT License; retain
source citations when reusing the evidence notes.
