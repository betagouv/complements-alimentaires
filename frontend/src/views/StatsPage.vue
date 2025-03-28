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
        <DsfrAccordion id="accordion-1" title="Gain de temps à l'instruction">
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
        <DsfrAccordion id="accordion-1" title="Qualité des déclarations déposées">
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
        <DsfrAccordion id="accordion-1" title="Utilisation de Compl'Alim par les professionnels">
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
      </DsfrAccordionsGroup>
    </div>
  </div>
</template>
<script setup>
import { ref, watch } from "vue"
import { useFetch } from "@vueuse/core"

const activeAccordion = ref(0)
const { response } = useFetch("/api/v1/stats/").json()
watch(response, () => console.log(response.value))
</script>
