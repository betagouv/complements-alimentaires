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
      </DsfrAccordionsGroup>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"

const activeAccordion = ref(0)
</script>
