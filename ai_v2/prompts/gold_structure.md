Tu reçois le commentaire écrit par un instructeur de la DGAL quand il a bloqué une déclaration de complément alimentaire, avec les motifs de blocage cochés. Structure-le en constats.

Catégories :
- `undeclared_ingredient` : un ingrédient présent sur l'étiquette n'est pas déclaré (y compris la plante source d'une substance, l'alcool, un excipient, un arôme).
- `missing_mention` : il manque une mention obligatoire générale (ne pas dépasser la dose, tenir hors de portée des enfants, substitut d'un régime varié, dénomination, DJR, liste d'ingrédients…).
- `missing_specific_warning` : il manque un avertissement lié à un ingrédient (femmes enceintes, anticoagulants, allergie Astéracées, alcool chez les moins de 12 ans…).
- `quantities_missing_on_label` : les quantités des actifs par DJR ne figurent pas sur l'étiquette (article 12-I).
- `dose_inconsistency` : les quantités de l'étiquette ne correspondent pas à celles déclarées.
- `dose_over_max` : une dose dépasse une dose maximale.
- `label_other_product` : l'étiquette ne correspond pas au produit déclaré.
- `djr_or_galenic_inconsistency` : la DJR, la forme galénique ou le volume diffèrent entre le dossier et l'étiquette, ou la DJR doit être exprimée autrement (gouttes en ml).
- `claims` : allégations interdites ou thérapeutiques.
- `other_label` : un autre problème d'étiquetage.
- `not_label` : un problème qui ne se voit pas sur l'étiquette (structure de la déclaration, justificatifs, analyses manquantes, type d'élément mal choisi…).

`label_related` est vrai si au moins un constat est d'une catégorie autre que `not_label`.

`should_block` est vrai si un contrôle automatique comparant l'étiquette à la déclaration aurait eu raison de refuser la validation automatique de ce dossier tel quel.

`elements` liste les noms cités (ingrédients, substances, mentions), tels qu'écrits.
