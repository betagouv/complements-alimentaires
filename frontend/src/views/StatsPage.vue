<template>
  <div>
    <div class="pt-10 bg-blue-france-975 relative min-h-[160px]">
      <div class="fr-container">
        <h1 class="mb-2">Mesures d'impact</h1>
        <p>Les indicateurs que nous utilisons pour quantifier l'impact du service Compl'Alim.</p>
      </div>
    </div>
    <div class="fr-container">
      <DsfrAccordionsGroup v-model="activeAccordion" class="my-8">
        <DsfrAccordion id="accordion-1" title="Fiabilité de la base de données ingrédients">
          <p>
            Notre objectif est de mettre à disposition une liste exhaustive d'ingrédients utilisables dans les
            compléments alimentaires.
          </p>
          <p>
            Compl'Alim permet aux professionnels de demander l'ajout d'ingrédients manquants. Le nombre de ces demandes
            constitue donc un indicateur de la complétude de notre base de données : un nombre faible indiquerait une
            base plus exhaustive.
          </p>
          <iframe
            src="https://compl-alim-metabase.cleverapps.io/public/question/804a05fa-eddd-410a-ad56-ad2b46f9f10d"
            frameborder="0"
            width="800"
            height="600"
            allowtransparency
          ></iframe>
        </DsfrAccordion>
        <DsfrAccordion id="accordion-2" title="Gain de temps à l'instruction">
          <h4>Statistiques de temps passé entre la soumission d'une déclaration et sa validation</h4>
          <p>
            L’instruction automatique de certaines déclarations permet au BEPIAS de concentrer ses efforts sur les cas
            les plus complexes. Le temps de validation est ainsi réduit et les déclarants sont plus satisfaits car ils
            peuvent mettre leurs produits sur le marché plus rapidement.
          </p>
          <p>
            Avec Compl'Alim, nous avons mis en place une aide à l'instruction pour le BEPIAS en octobre 2024. Nous
            améliorons en continu les outils et les méthodes d'évaluation pour réduire le temps d'instruction, en tenant
            compte des évolutions réglementaires et des retours d'utilisateurs.
          </p>
          <iframe
            src="https://compl-alim-metabase.cleverapps.io/public/question/572252e2-0d2a-4465-8ec4-c9f594508f15"
            frameborder="0"
            width="800"
            height="600"
            allowtransparency
          ></iframe>
          <br />
          <h4>Impact de l'instruction facilitée</h4>
          <p>
            Notre outil permet l'automatisation de l'instruction de certaines déclarations ARTICLE 15 sans risque. Ces
            déclarations n'étaient pas facilement identifiables auparavant et devaient nécessairement passer par le même
            processus d'instruction que les déclarations plus complexes.
          </p>
          <p>
            Le taux mensuel de ces déclarations "sans risque" constitue un indicateur du temps gagné à l'instruction.
          </p>
          <iframe
            src="https://compl-alim-metabase.cleverapps.io/public/question/c99b0f9a-77e2-470f-b2a6-98a8ac3a4a46"
            frameborder="0"
            width="800"
            height="600"
            allowtransparency
          ></iframe>
        </DsfrAccordion>
        <DsfrAccordion id="accordion-3" title="Qualité des déclarations déposées">
          <p>
            Notre objectif est de faciliter la déclaration de compléments alimentaires et la compréhension des
            différentes règlementations pour que les compléments alimentaires soient conformes.
          </p>
          <p>
            Le nombre de déclarations recevant une objection ou une observation de la part de nos services constitue
            donc un indicateur de la qualité des déclarations déposées.
          </p>
          <iframe
            src="https://compl-alim-metabase.cleverapps.io/public/question/00227f7a-b2fa-4efb-8982-891c66864e13"
            frameborder="0"
            width="800"
            height="600"
            allowtransparency
          ></iframe>
        </DsfrAccordion>
        <DsfrAccordion id="accordion-4" title="Utilisation de Compl'Alim par les professionnels">
          <p>Notre objectif est de faciliter la déclaration de compléments alimentaires pour les professionnels.</p>
          <p>
            L'évolution du nombre de professionnels déclarant leur premier complément alimentaire sur Compl'Alim donne
            une idée de la capacité du secteur économique du complément alimentaire à identifier Compl'Alim comme
            plateforme de référence. Ce graphique reprend le nombre de nouvelles entreprises déclarantes dès la mise en
            ligne de TeleIcare. Les données datant de TeleIcare (avant septembre 2024) sont encore à fiabiliser.
          </p>
          <iframe
            src="https://compl-alim-metabase.cleverapps.io/public/question/9c4cb4bc-c493-4539-9eb2-321663ad3d15"
            frameborder="0"
            width="800"
            height="600"
            allowtransparency
          ></iframe>
        </DsfrAccordion>
        <DsfrAccordion id="accordion-5" title="Nombre de consultations à la base ingrédients">
          <p>
            Nous mettons à disposition un moteur de recherche avec les données de notre base ingrédients. Une
            utilisation élevée de cette fonctionnalité se traduit en moins d'erreurs dans les déclarations par manque
            d'informations.
          </p>
          <bar-chart
            v-if="elementVisitChartInfo"
            :x="elementVisitChartInfo.x"
            :y="elementVisitChartInfo.y"
            name='["Consultations à la base ingrédients"]'
            unit-tooltip="visites"
            selected-palette="default"
          ></bar-chart>
        </DsfrAccordion>
      </DsfrAccordionsGroup>
    </div>
  </div>
</template>
<script setup>
import { ref, watch, computed } from "vue"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"

const activeAccordion = ref(0)
const { response, data } = useFetch("/api/v1/stats/").json()

watch(response, async () => response && handleError(response))

const elementVisitChartInfo = computed(() => {
  if (!data?.value?.elementVisitStats?.reportData) return null
  const keys = Object.keys(data.value.elementVisitStats.reportData) || []
  const values = Object.values(data.value.elementVisitStats.reportData).map((x) => x[0].nbHits)
  const x = JSON.stringify([keys])
  const y = JSON.stringify([values])
  return { x, y }
})
</script>
