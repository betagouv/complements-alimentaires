<template>
  <OfficialLetterWrapper :letterDate="letterGenerationDate" :letterTitle="title">
    <p>La Direction générale de l'alimentation (DGAL) atteste que :</p>
    <p class="font-bold !text-center !text-base">{{ name }}</p>
    <p>
      a effectué, le {{ isoToPrettyDate(declarationDate, dateOptions) }}, la déclaration mentionnée à l’article 16 du
      décret n°2006-352 du 20 mars 2006 relatif aux compléments alimentaires pour le produit :
    </p>
    <div class="my-4 font-bold text-center mx-auto">
      <div>{{ caName }}</div>
      <div>{{ caGalenicForm }}</div>
      <div>{{ caCompany }}</div>
    </div>
    <p>
      Cette déclaration, acceptée , est enregistrée sous le numéro :
      <span class="font-bold">{{ caseNumber }}</span>
    </p>
    <p>
      L’examen de la déclaration par les services du ministère de l’agriculture et de la souveraineté alimentaire prévu
      à l’article 16 du décret n°2006-352 porte sur les ingrédients du complément alimentaire ayant un effet
      nutritionnel ou physiologique. Cet examen n’a pas pour objectif de procéder à un contrôle de la conformité du
      produit à l’ensemble des dispositions qui lui sont applicables, notamment en matière d’hygiène ou d’information du
      consommateur.
    </p>
    <p class="font-bold">
      Cette attestation ne constitue donc pas une garantie de conformité aux dispositions en vigueur.
    </p>
    <p>
      Conformément aux dispositions de l’article 17 du règlement (CE) n° 178/2002 établissant les principes généraux et
      les prescriptions générales de la législation alimentaire, il vous incombe de veiller à ce que le complément
      alimentaire que vous mettez sur le marché réponde à la définition des compléments alimentaires au sens de
      l’article 2 du décret n°2006-352, ainsi qu’aux prescriptions du droit alimentaire qui lui sont applicables,
      notamment en matière d’hygiène (R(CE) n°852/2004) et d’information du consommateur (R(UE) n°1169/2011).
    </p>
    <p>
      Pour tout renseignement d’ordre général sur le cadre réglementaire applicable aux compléments alimentaires,
      rendez-vous sur le site de la DGAL à l’adresse suivante :
      <a :href="moreLegalInfoUrl">{{ moreLegalInfoUrl }}</a>
    </p>
  </OfficialLetterWrapper>
</template>

<script setup>
import OfficialLetterWrapper from "../OfficialLetterWrapper"
import { isoToPrettyDate } from "@/utils/date"

const dateOptions = {
  month: "short",
  day: "numeric",
  year: "numeric",
}

defineProps({
  title: { type: String, required: true },
  letterGenerationDate: { type: Date, required: true },
  name: { type: String, required: true },
  caName: { type: String, required: true },
  caGalenicForm: { type: String, required: true },
  caCompany: { type: String, required: true },
  declarationDate: { type: Date, required: true },
  caseNumber: { type: String, required: true },
  moreLegalInfoUrl: { type: String, required: true },
})
</script>

<style scoped>
p {
  @apply letter-p;
}

a {
  @apply letter-a;
}
</style>
