---
name: enzymatic-atom-mapping
description: Establish evidence-supported atom correspondences for enzymatic reaction SMILES using biochemical databases and primary literature. Use for mapping or reviewing supplied reactants and products, especially when general atom mappers disagree.
---

# Enzymatic Atom Mapping

Default to mapping every atom represented in the supplied SMILES: all heavy atoms (C, O, N, P, S, etc.) and explicit hydrogen atoms, including isotopic hydrogen. Explicit H means a separate [H], [2H], etc. atom; H counts within [CH3] or similar brackets do not receive independent map IDs. Keep implicit hydrogens implicit; do not expand or add atoms or components unless the user asks. Use a carbon-only mapping only when requested or when a complete candidate cannot be justified, and state why the output is partial. Separate complete mapping coverage from mechanistic support for each correspondence. This skill requires access to biochemical sources and, for automated checks, an environment containing RDKit. It is an evidence-guided agent workflow, not a trained prediction model.

## Interpret the supplied reaction

Accept reactant>>product SMILES and optional EC numbers, reaction names, organism information, or database identifiers. Identify the compounds and likely enzyme reaction before requesting annotations. Ask when unresolved identities or competing mechanisms would materially change the mapping.

Check the input with scripts/validate_mapping.py when RDKit is available. This reports elemental, isotopic, and charge balance without altering the input. Inspect ring versus open-chain forms, stereochemistry, protonation, and repeated molecular components. Missing hydrogens or cofactors can explain imbalance; report them rather than silently changing the supplied structures. Remove only confirmed formatting escapes, not legitimate bond-stereochemistry syntax.

## Find evidence for atom transfer

Consult [references/evidence.md](references/evidence.md) for source selection and representative cases. Search specific IUBMB, KEGG, Rhea, M-CSA, and BRENDA entries and their primary literature. A database reaction equation confirms participants; it does not by itself establish every atom correspondence.

Record the retrieved entry, URL, access date, and supported claim. Distinguish direct experimental evidence, a published mechanistic proposal, and deductions from connectivity. Do not claim to have read inaccessible material. Prioritize an experimentally or mechanistically justified assignment over a candidate selected only by minimum bond edits or tool agreement.

LocalMapper, RXNMapper, and EnzymeMap may supply candidates if available. Compare correspondences after aligning the molecular structures, not by raw map numbers or SMILES text. Their scores have different meanings; EnzymeMap's database quality is a rule-frequency statistic, not a probability of correctness. This skill does not grant permission to upload input to external prediction services.

## Construct and inspect the correspondence

- Trace all conserved atoms through supported bond-breaking, bond-forming, and rearrangement events, including cofactors and transferred groups. For cleavage, account for all labelled products; for condensation, account for each substrate contribution.
- Align alternative SMILES traversals by structure and stereochemistry. Consider symmetry and report unresolved positional alternatives. A unique serialization does not prove a unique physical assignment.
- Give repeated stoichiometric molecules distinct reaction-local map identifiers. Match component identity as well as atom identity.
- Preserve the provided structures, isotopes, formal charges, stereochemistry, and component multiplicity on each side. A reaction may change these properties between sides; mapping labels must not change the structure already supplied for either side.
- Positive map identifiers are unique within each side. Shared identifiers must denote the same element and isotope. They are correspondence labels, not automatically biochemical C1, C2, etc.
- Do not splice incompatible assignments from different candidates. When symmetry permits equivalent non-carbon assignments, provide a complete representative mapping and identify the interchangeable atoms. Qualify model-only correspondences as unverified; do not claim they are evidence-supported. If a complete candidate cannot be justified or atoms cannot be paired because the input is incomplete, report the limitation rather than inventing precision or silently returning only carbon labels.

Run the validator with --mapped for a candidate. Use --scope all (the default) for all represented atoms, including explicit H. Use --scope heavy or --scope carbon only for an explicitly limited check. Read its warnings even when it exits successfully. The validator cannot establish catalytic mechanism, choose among symmetry-equivalent maps, or certify experimental correctness.

## Deliver a reproducible result

Use English and include:
1. Evidence status: evidence-supported, partially supported, or unresolved, with the scope of that status.
2. Reusable atom-mapped reaction SMILES when justified; label partial or representative assignments explicitly.
3. A table: Reactant | Reactant atom (element and position/map ID) | Product | Product atom (element and position/map ID) | Supporting evidence. Cover every mapped atom; equivalent atoms may be grouped explicitly. Define biochemical numbering independently of the reaction-local map identifiers.
4. Reaction identity, EC number where established, and supporting database identifiers and source links.
5. A concise mapping rationale, machine-check results, and unresolved ambiguities or input-balance issues.

When no unique assignment is supported, return what is established and the alternatives or missing evidence. Do not fabricate confidence percentages or describe the entire reaction as verified when only its carbon skeleton was checked.

