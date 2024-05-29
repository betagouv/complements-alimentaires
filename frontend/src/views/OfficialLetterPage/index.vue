<template>
  <!-- VRAIE SYNTAXE À GARDER -->
  <!-- <component :is="getComponentFromName(letterName)" v-bind="childrenProps"></component> -->

  <!-- POUR LES TESTS -->
  <component :is="getComponentFromName('AccuseEnregistrement')" v-bind="exPropsAccuseEnregistrement" />
  <!-- <component :is="getComponentFromName('AttestationDeclarationArt15')" v-bind="exPropsAttestationDeclarationArt15" /> -->
  <!-- <component :is="getComponentFromName('AttestationDeclarationArt16')" v-bind="exPropsAttestationDeclarationArt16" /> -->
  <!-- <component :is="getComponentFromName('Refus')" v-bind="exPropsRefus" /> -->
</template>

<script setup>
import { defineAsyncComponent } from "vue"

// Récupère un component correspondant à une lettre officielle, à partir de son nom
const getComponentFromName = (name) => defineAsyncComponent(() => import(`./letters/${name}`))

// VRAIE SYNTAXE À GARDER
// defineProps({
//   letterName: { type: String, required: true }, // le nom de la lettre à utiliser
//   childrenProps: { type: Object, required: true }, // les props spéciques nécessaires à cette lettre
// })

// POUR LES TESTS
const exPropsAccuseEnregistrement = {
  title: "accusé d’enregistrement de déclaration d’un complément alimentaire",
  letterGenerationDate: new Date(2024, 5, 25),
  declarationDate: new Date(2024, 5, 25),
  caName: "L-Glutamine 2000",
  caGalenicForm: "Gélule",
  caCompany: "Nutrition Sportive Way",
  caseNumber: "2024-5-1273",
  transmissionEmail: "complement-alimentaire.dgal@agriculture.gouv.fr",
  dgalDocumentUrl: "https://agriculture.gouv.fr/quest-ce-quun-complement-alimentaire",
  attestationUrl: "https://url-a-definir", // TODO
  moreLegalInfoUrl: "https://agriculture.gouv.fr/quest-ce-quun-complement-alimentaire",
}

const exPropsAttestationDeclarationArt15 = {
  title: "attestation de déclaration d’un complément alimentaire",
  letterGenerationDate: new Date(2024, 5, 25),
  name: "Johanna Galibert",
  caName: "Ronce",
  caGalenicForm: "Flacon",
  caCompany: "Belar basa gemmothérapie",
  declarationDate: new Date(2024, 5, 25),
  caseNumber: "2024-5-1273",
  attestationUrl: "https://url-a-definir", // TODO
  moreLegalInfoUrl: "https://agriculture.gouv.fr/quest-ce-quun-complement-alimentaire",
}

const exPropsAttestationDeclarationArt16 = {
  title: "attestation de déclaration d’un complément alimentaire",
  letterGenerationDate: new Date(2024, 5, 25),
  name: "Johanna Galibert",
  caName: "Ronce",
  caGalenicForm: "Flacon",
  caCompany: "Belar basa gemmothérapie",
  declarationDate: new Date(2024, 5, 25),
  caseNumber: "2024-5-1273",
  moreLegalInfoUrl: "https://agriculture.gouv.fr/quest-ce-quun-complement-alimentaire",
}

const exPropsRefus = {
  recipientName: "ARIIX EUROPE B.V",
  recipientAddress: "President Kennedylaan 19\n2517 JK DEN HAAG",
  letterGenerationDate: new Date(2024, 6, 20),
  caName: "RENEW",
  caGalenicForm: "Poudre",
  caCompany: "Kiwi Baies",
  declarationDate: new Date(2024, 5, 25),
  caseNumber: "2024-5-1273",
  telerecoursUrl: "https://citoyens.telerecours.fr/#/authentication",
}
</script>
