<template>
  <OfficialLetterWrapper :letterDate="letterGenerationDate" :letterTitle="title">
    <p>La Direction générale de l'alimentation (DGAL) atteste que :</p>
    <p class="font-bold !text-center !text-base">{{ name }}</p>
    <p>
      a effectué, le {{ isoToPrettyDate(declarationDate, dateOptions) }}, la déclaration mentionnée à l’article 15 du
      décret n°2006-352 du 20 mars 2006 relatif aux compléments alimentaires pour le produit :
    </p>
    <div class="my-4 font-bold text-center mx-auto">
      <div>{{ caName }}</div>
      <div>{{ caGalenicForm }}</div>
      <div>{{ caCompany }}</div>
    </div>
    <p>
      Cette déclaration est enregistrée sous le numéro :
      <span class="font-bold">{{ caseNumber }}</span>
    </p>
    <p>
      La déclaration prévue à l’article 15 du décret n°2006-352 vise à informer l’administration de la mise sur le
      marché d’un complément alimentaire.
    </p>
    <p>
      Votre produit est enregistré sur la liste consultable à l’adresse suivante :
      <a :href="attestationUrl">{{ attestationUrl }}</a>
      . Il pourra faire l’objet de contrôles de l’administration.
    </p>
    <p class="font-bold">
      Cette attestation ne constitue donc pas une garantie de conformité aux dispositions en vigueur ni une autorisation
      de mise sur le marché.
    </p>
    <p>
      Conformément aux dispositions de l’article 17 du règlement (CE) n° 178/2002 établissant les principes généraux et
      les prescriptions générales de la législation alimentaire, il vous incombe de veiller à ce que le complément
      alimentaire que vous mettez sur le marché réponde à la définition des compléments alimentaires au sens de
      l’article 2 du décret n°2006-352, ainsi qu’aux prescriptions du droit alimentaire qui leur sont applicables,
      notamment en matière d’hygiène (R(CE) n°852/2004), d’information du consommateur (R(UE) n°1169/2011) et de
      nouveaux aliments (R(UE) n°2015/2283). À cet égard, vous devez être en mesure de prouver que les ingrédients mis
      en œuvre disposent d’un historique de consommation dans l’Union européenne avant le 15 mai 1997 ou, à défaut,
      qu’ils ont été autorisés au titre du règlement (UE) n°2015/2283.
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

// props
defineProps({
  title: { type: String, required: true },
  letterGenerationDate: { type: Date, required: true },
  name: { type: String, required: true },
  caName: { type: String, required: true },
  caGalenicForm: { type: String, required: true },
  caCompany: { type: String, required: true },
  declarationDate: { type: Date, required: true },
  caseNumber: { type: String, required: true },
  attestationUrl: { type: String, required: true },
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
