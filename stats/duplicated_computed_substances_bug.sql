-- Extraction des adresses mail des concerné.e.s

select distinct
    data_user.email,
    (declaration_id)
from (
    select
        data_computedsubstance.declaration_id,
        data_computedsubstance.substance_id,
        count(*) as cnt
    from data_computedsubstance
    group by
        data_computedsubstance.declaration_id,
        data_computedsubstance.substance_id
    order by count(*) desc
) as duplicated_computed_substances
inner join
    data_declaration
    on duplicated_computed_substances.declaration_id = data_declaration.id
inner join data_user on data_user.id = author_id
where cnt > 1


-- Déduplication
-- declaration_to_dedup_ids = liste provenant de la requête SQL

import time
for declaration_to_dedup in Declaration.objects.filter(id__in=declaration_to_dedup_ids):
    print(f"------------>> déduplication de {declaration_to_dedup}")
    total = declaration_to_dedup.computed_substances.all().values_list('substance_id', flat=True)
    nb_total = len(total)
    substances_id = list(total.distinct())
    nb_distinct = len(substances_id)
    print(f'->> déduplication de {nb_total - nb_distinct} sur {nb_total} computed substances')
    # conserver une seule version de chaque substance avec ses autres champs (active, quantity, unit)
    for subst_id in substances_id:
        all_objects_ids = list(declaration_to_dedup.computed_substances.filter(substance_id=subst_id).values_list("id", flat=True))
        nb_initial = len(all_objects_ids)
        # pop le premier pour le conserver
        all_objects_ids.pop(0)
        # supprimer les autres
        print(f'suppression de {len(declaration_to_dedup.computed_substances.filter(id__in=all_objects_ids))} sur {nb_initial} pour la substance {Substance.objects.get(pk=subst_id)}')
        # delete() sur plus de 100 objets est très lent, on utilise _raw_delete à la place, qui n'effectue pas les signals post_save (update_article)
        # https://vladcalin.ro/djangos-delete-is-harmful/
        to_delete_qs = declaration_to_dedup.computed_substances.filter(id__in=all_objects_ids)
        to_delete_qs._raw_delete(to_delete_qs.db)
    time.sleep(1)
    total = declaration_to_dedup.declared_substances.all().values_list('substance_id', flat=True)
    nb_total = len(total)
    substances_id = list(total.distinct())
    nb_distinct = len(substances_id)
    print(f'->> déduplication de {nb_total - nb_distinct} sur {nb_total} declared substances')
    # conserver une seule version de chaque substance avec ses autres champs (active, quantity, unit)
    for subst_id in substances_id:
        # not a new substance
        if subst_id:
            all_objects_ids = list(declaration_to_dedup.declared_substances.filter(substance_id=subst_id).values_list("id", flat=True))
            nb_initial = len(all_objects_ids)
            # pop le premier pour le conserver
            all_objects_ids.pop(0)
            # supprimer les autres
            print(f'suppression de {len(declaration_to_dedup.declared_substances.filter(id__in=all_objects_ids))} sur {nb_initial} pour la substance {Substance.objects.get(pk=subst_id)}')
            declaration_to_dedup.declared_substances.filter(id__in=all_objects_ids).delete()

    time.sleep(1)
    total = declaration_to_dedup.declared_ingredients.all().values_list('ingredient_id', flat=True)
    nb_total = len(total)
    ingredients_id = list(total.distinct())
    nb_distinct = len(ingredients_id)
    print(f'->> déduplication de {nb_total - nb_distinct} sur {nb_total} ingredient')
    # conserver une seule version de chaque substance avec ses autres champs (active, quantity, unit)
    for ingr_id in ingredients_id:
        # not a new ingredient
        if ingr_id:
            all_objects_ids = list(declaration_to_dedup.declared_ingredients.filter(ingredient_id=ingr_id).values_list("id", flat=True))
            nb_initial = len(all_objects_ids)
            # pop le premier pour le conserver
            all_objects_ids.pop(0)
            # supprimer les autres
            print(f'suppression de {len(declaration_to_dedup.declared_ingredients.filter(id__in=all_objects_ids))} sur {nb_initial} pour lingredient {Ingredient.objects.get(pk=ingr_id)}')
            declaration_to_dedup.declared_ingredients.filter(id__in=all_objects_ids).delete()
