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
        <DsfrAccordion id="accordion-1" title="Complétude de la base de données ingrédients">
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
            src="https://compl-alim-metabase.cleverapps.io/public/question/eecd21f9-e9e4-4fa0-a39a-4f30ab3b6f13"
            frameborder="0"
            width="800"
            height="600"
            allowtransparency
          ></iframe>
        </DsfrAccordion>
        <DsfrAccordion id="accordion-2" title="Gain de temps à l'examen des déclarations">
          <p>
            L’examen des déclarations automatique de certaines déclarations permet aux services de la Direction Générale
            de l’Alimentation de concentrer ses efforts sur les cas les plus complexes. Le temps de validation est ainsi
            réduit et les déclarants sont plus satisfaits car ils peuvent mettre leurs produits sur le marché plus
            rapidement.
          </p>
          <p>
            Avec Compl'Alim, nous avons mis en place une aide à l'examen des déclarations pour les services de la
            Direction Générale de l’Alimentation en octobre 2024. Nous améliorons en continu les outils et les méthodes
            d'évaluation pour réduire le temps d'examen des déclarations, en tenant compte des évolutions réglementaires
            et des retours d'utilisateurs.
          </p>
          <iframe
            src="https://compl-alim-metabase.cleverapps.io/public/question/572252e2-0d2a-4465-8ec4-c9f594508f15"
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
            Le pourcentage de déclarations recevant une objection ou une observation de la part de nos services
            constitue donc un indicateur de la qualité des déclarations instruites.
          </p>
          <iframe
            src="https://compl-alim-metabase.cleverapps.io/public/question/ac8ce038-f7d9-4e9e-a90b-3268f114c00f"
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
            plateforme de référence.
          </p>
          <iframe
            src="https://compl-alim-metabase.cleverapps.io/public/question/891d6238-9f0d-40db-a97f-747b829b1902"
            frameborder="0"
            width="800"
            height="600"
            allowtransparency
          ></iframe>
        </DsfrAccordion>
        <DsfrAccordion id="accordion-4" title="Fiabilité de la base de données ingrédients">
          <p>
            Nous visons une base de données complète et fiable. Or, les retours signalant des imprécisions ou des
            erreurs indiquent que ce n'est pas encore le cas. Notre objectif est donc de réduire significativement le
            nombre de ces remontées.
          </p>
          <iframe
            src="https://compl-alim-metabase.cleverapps.io/public/question/1814a578-3978-45ce-a471-a29035f9615f"
            frameborder="0"
            width="800"
            height="600"
            allowtransparency
          ></iframe>
        </DsfrAccordion>
        <DsfrAccordion id="accordion-5" title="Utilisation de la base de données ingrédient">
          <p>
            Nous mettons à disposition une base de données ingrédients avec leur réglementation d'usage mis à jour
            régulièrement. Notre hypothèse est qu'une consultation élevée de cette base de donnée aura pour conséquence
            une réduction des erreurs dans les déclarations.
          </p>
          <h4 v-if="elementVisitChartInfo">Consultations à la base ingrédients</h4>
          <bar-chart
            v-if="elementVisitChartInfo"
            :x="elementVisitChartInfo.x"
            :y="elementVisitChartInfo.y"
            name='[" "]'
            unit-tooltip="visites"
            selected-palette="default"
          ></bar-chart>
        </DsfrAccordion>
        <DsfrAccordion
          id="accordion-6"
          title="Utilisation de la base de données des déclarations de compléments alimentaires"
        >
          <p>
            Nous mettons à disposition une base de données des compléments alimentaires déclarés auprès de la Direction
            générale de l’alimentation. Notre hypothèse est qu'une consultation élevée de cette base de données
            permettra de sensibiliser les distributeurs (avant de référencer un produit) et les consommateurs (avant
            d’acheter un produit).
          </p>
          <h4 v-if="declarationVisitChartInfo">Consultations au jeu de données de Compl'Alim</h4>
          <bar-chart
            v-if="declarationVisitChartInfo"
            :x="declarationVisitChartInfo.x"
            :y="declarationVisitChartInfo.y"
            name='[" "]'
            unit-tooltip="téléchargements"
            selected-palette="default"
          ></bar-chart>
          <p>
            <a
              href="https://www.data.gouv.fr/fr/datasets/declarations-de-complements-alimentaires"
              rel="noopener external"
              target="_blank"
              title="Le jeu de données data.gouv.fr publié par Compl'Alim - nouvelle fenêtre"
            >
              Le jeu de données data.gouv.fr publié par Compl'Alim
            </a>
          </p>
        </DsfrAccordion>
      </DsfrAccordionsGroup>
    </div>
  </div>
</template>
<script setup>
import { ref, watch, computed, onMounted } from "vue"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"

const activeAccordion = ref()
const { response, data } = useFetch("/api/v1/stats/").json()

watch(response, async () => response && handleError(response))

const formatReportData = (reportData, xKey) => {
  const keys = (Object.keys(reportData) || []).map(formatMonthLabel)
  const values = Object.values(reportData).map((x) => x[xKey])
  const x = JSON.stringify([keys])
  const y = JSON.stringify([values])
  return { x, y }
}

const elementVisitChartInfo = computed(() => {
  if (!data?.value?.elementVisitStats?.reportData) return null
  return formatReportData(data.value.elementVisitStats.reportData, "nbVisits")
})

const declarationVisitChartInfo = computed(() => {
  if (!data?.value?.declarationVisitStats?.reportData) return null
  return formatReportData(data.value.declarationVisitStats.reportData, "downloads")
})

const formatMonthLabel = (apiLabel) => {
  const [year, month] = apiLabel.split("-").map(Number)
  const date = new Date(year, month - 1)
  return new Intl.DateTimeFormat("fr-FR", { month: "long", year: "numeric" }).format(date)
}

onMounted(async () => {
  const script = document.createElement("script")
  script.type = "module"
  script.src = "/static/js/BarChart.js"
  document.body.appendChild(script)
  const style = document.createElement("link")
  style.rel = "stylesheet"
  style.src = "/static/css/BarChart.js"
  document.body.appendChild(style)
})
</script>
