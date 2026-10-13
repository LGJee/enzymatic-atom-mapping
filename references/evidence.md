# Evidence selection and representative cases

These are verification routes, not a database of universally correct mappings.
The named entries below were consulted on 2026-10-13. Re-read the relevant
entry and its supporting literature for the reaction under examination.

## What each source establishes

- [IUBMB Enzyme Nomenclature](https://iubmb.qmul.ac.uk/enzyme/):
  enzyme classification and accepted reaction definitions. An EC number does
  not establish organism-specific details or every atom correspondence.
- [KEGG REACTION](https://www.kegg.jp/kegg/reaction/):
  reaction participants, structures, reaction classes, and cross-references.
  Reaction-class atom labels and mapper labels are not automatically the
  biochemical carbon numbering of a metabolite.
- [Rhea](https://www.rhea-db.org/):
  curated participants, charge-specific structures, reactions, and literature.
  A retrieved reaction equation alone is insufficient evidence for positional
  isotope transfer.
- [M-CSA](https://www.ebi.ac.uk/thornton-srv/m-csa/):
  literature-supported mechanism proposals and bond-change descriptions.
  A representative enzyme mechanism is not necessarily an experimental atom
  tracing result for the user's organism.
- [BRENDA](https://www.brenda-enzymes.org/):
  enzyme-specific literature and experimental annotations. Follow the primary
  references; do not treat a name or EC match alone as mapping validation.

For every substantive inference, retain the reaction/compound identifiers,
the particular supporting statement or mechanism step, the URL, access date,
and version if shown. State which inference follows from the evidence.

## Phosphorylation

[KEGG R00299](https://www.kegg.jp/entry/R00299) identifies ATP-dependent glucose
6-phosphorylation. For carbon tracing, follow the glucose skeleton and locate
the phosphate-bearing carbon by molecular connectivity. Distinguish biochemical
C6 from the sixth carbon encountered in a SMILES string. Phosphate oxygen
assignments require separate evidence; symmetry or protonation can make an
apparently unique all-atom output misleading.

## Aldose–ketose isomerization

[KEGG R00771](https://www.kegg.jp/entry/R00771) identifies glucose-6-phosphate /
fructose-6-phosphate isomerization (EC 5.3.1.9). Check the continuous carbon chain,
carbonyl position, phosphate position, and any ring–chain conversion. Do not
infer chain reversal from reversed SMILES traversal or rotated drawings.

## Fructose-bisphosphate cleavage

- [IUBMB EC 4.1.2.13](https://iubmb.qmul.ac.uk/enzyme/EC4/1/2/13.html)
  defines the aldolase reaction.
- [KEGG R01070](https://www.kegg.jp/entry/R01070) identifies the beta-D-fructose
  1,6-bisphosphate reaction and its triose phosphate products.
- [Rhea 14729](https://www.rhea-db.org/rhea/14729) supplies curated participants
  and literature cross-references.
- [M-CSA entry 52](https://www.ebi.ac.uk/thornton-srv/m-csa/entry/52/)
  describes class II aldolase condensation forming the FBP C3–C4 bond. The
  reverse cleavage separates the C1–C3 fragment into DHAP and C4–C6 into GAP,
  using standard FBP positions. This is a deduction from the mechanism and
  molecular connectivity, not a statement about arbitrary map identifiers.

The provided example mixes a tetraanionic FBP with neutral product phosphates:
it has a net difference of four hydrogens and +4 formal charge between sides.
Its carbon and other heavy-element inventories remain balanced. Report this
representation issue; do not silently change the supplied phosphates or insert
protons. Ring opening, oxygen transfer, proton exchange, and undefined product
stereochemistry need their own scope-qualified assessment.

## Symmetry and repeated molecules

Symmetry can permit multiple equivalent representations of a correspondence.
Distinguish a graph automorphism from an experimentally distinguishable atom
history. Position-specific isotopic labels or enzyme stereoselectivity can break
an apparent symmetry. Report alternatives when the evidence does not resolve
them. Repeated molecules need distinct reaction-local atom maps even if their
carbon-source labels would be identical in a later tracing analysis.

## Interpreting mapper quality

[EnzymeMap's methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC10718068/)
define database quality as a rule's relative occurrence frequency within an EC
class. It is not a calibrated probability of correct mapping, and an absent
score is not a score of zero. Consensus between tools is corroboration rather
than independent experimental validation.

[RDKit's documentation](https://www.rdkit.org/docs/RDKit_Book.html) explains
SMILES parsing, stereochemistry, and atom-map notation. The bundled checker uses
these representations to enforce molecular preservation and mapping invariants;
it cannot prove a mechanism or rank plausible positional assignments.
