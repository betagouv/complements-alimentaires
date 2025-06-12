<template>
  <DsfrSideMenu :menuItems="menuItems" />
</template>

<script setup>
import { computed } from "vue"
import { useRoute } from "vue-router"

// Note:
// Il y a des hacks en attendant la résolution de https://github.com/dnum-mi/vue-dsfr/issues/1076
// Par exemple, la gestion de `expanded` ne devrait pas se faire avec le route
// Aussi, on cache l'icône (dans les styles scoped) pour ne pas faire penser aux gens
// qu'on peut collapse les sections.
const declaration = defineModel()
const route = useRoute()
const makeRoute = (name) => ({ name, params: { declarationId: declaration.value.id } })
const appendHash = (route, hash) => ({ ...{ hash }, ...route })

const isInInstruction = computed(() => route.name === "InstructionSection")
const isInIdentity = computed(() => route.name === "IdentitySection")
const isInHistory = computed(() => route.name === "HistorySection")

const instructionRoute = computed(() => makeRoute("InstructionSection"))
const identityRoute = computed(() => makeRoute("IdentitySection"))
const historyRoute = computed(() => makeRoute("HistorySection"))

const menuItems = computed(() => [
  {
    to: instructionRoute.value,
    active: isInInstruction.value,
    text: "Instruction",
    expanded: isInInstruction.value,
    menuItems: isInInstruction.value
      ? [
          {
            to: appendHash(instructionRoute.value, "#pieces-jointes"),
            text: "Pièces jointes",
          },
          {
            to: appendHash(instructionRoute.value, "#dernier-commentaire"),
            text: "Dernier commentaire",
          },
          {
            to: appendHash(instructionRoute.value, "#composition-produit"),
            text: "Composition du produit",
          },
          {
            to: appendHash(instructionRoute.value, "#resultat-instruction"),
            text: "Résultat de l'instruction",
          },
          {
            to: appendHash(instructionRoute.value, "#notes"),
            text: "Notes pour l'administration",
          },
        ]
      : null,
  },
  {
    to: identityRoute.value,
    text: "Identité produit et entreprise",
    expanded: isInIdentity.value,
    active: isInIdentity.value,
    menuItems: isInIdentity.value
      ? [
          {
            to: appendHash(identityRoute.value, "#declarant-e"),
            text: "Déclarant·e",
          },
          {
            to: appendHash(identityRoute.value, "#produit"),
            text: "Informations sur le produit",
          },
          {
            to: appendHash(identityRoute.value, "#entreprise"),
            text: "Identité de l’entreprise",
          },
        ]
      : null,
  },
  {
    to: historyRoute.value,
    text: "Historique",
    active: isInHistory.value,
  },
])
</script>
