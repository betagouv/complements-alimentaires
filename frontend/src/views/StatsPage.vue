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
            Nous ciblons d'avoir une liste exhaustive d'ingrédients que les déclarants peuvent utiliser dans leur
            composition déclarée.
          </p>
          <p>
            Au cas où les professionnels ne peuvent pas retrouver un ingrédient, ils peuvent demander l'ajout d'un
            nouvel ingrédient. Les instructrices consultent ces demandes régulièrement pour decider si l'ingrédient doit
            être ajouté, remplacé par un ingrédient qui existe déjà, ou rejeté.
          </p>
          <p>
            Dans l'idéal, le nombre de demandes d'ajout est quasi nul : cela indique que notre base est exhaustive et
            facilement recherchable.
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
