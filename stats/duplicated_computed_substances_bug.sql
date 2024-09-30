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
    total = declaration_to_dedup.computed_substances.all().values_list('substance_id', flat=True)
    nb_total = len(total)
    substances_id = list(total.distinct())
    nb_distinct = len(substances_id)
    print(f'->> déduplication de {declaration_to_dedup} : {nb_total - nb_distinct} sur {nb_total}')
    # conserver une seule version de chaque substance avec ses autres champs (active, quantity, unit)
    for subst_id in substances_id:
        all_objects_ids = list(declaration_to_dedup.computed_substances.filter(substance_id=subst_id).values_list("id", flat=True))
        nb_initial = len(all_objects_ids)
        # pop le premier pour le conserver
        all_objects_ids.pop(0)
        # supprimer les autres
        # declaration_to_dedup.computed_substances.filter(id__in=all_objects_ids).delete()
        print(f'suppression de {len(declaration_to_dedup.computed_substances.filter(id__in=all_objects_ids))} sur {nb_initial} pour la substance {Substance.objects.get(pk=subst_id)}')
        time.sleep(3)
