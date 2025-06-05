<template>
  <DsfrSideMenu :menuItems="menuItems" @toggleExpand="(s) => (expandedId = s)" />
</template>

<script setup>
import { ref, computed } from "vue"

// Ceci est un hack en attendant la résolution de https://github.com/dnum-mi/vue-dsfr/issues/1076
const expandedId = ref("1")
const menuItems = computed(() => [
  {
    id: "1",
    to: "#",
    active: true,
    text: "Instruction",
    expanded: expandedId.value === "1",
    menuItems: [
      {
        id: "11",
        to: "#",
        text: "Pièces jointes",
      },
      {
        id: "12",
        to: "#",
        text: "Composition du produit",
      },
      {
        id: "13",
        to: "#",
        text: "Dernier commentaire",
      },
      {
        id: "14",
        to: "#",
        text: "Résultat de l'instruction",
      },
      {
        id: "15",
        to: "#",
        text: "Notes pour l'administration",
      },
    ],
  },
  {
    id: "2",
    to: "#",
    text: "Identité produit et entreprise",
    expanded: expandedId.value === "2",
    menuItems: [
      {
        id: "21",
        to: "#",
        text: "Déclarant·e",
      },
      {
        id: "22",
        to: "#",
        text: "Informations sur le produit",
      },
      {
        id: "23",
        to: "#",
        text: "Identité de l’entreprise",
      },
    ],
  },
])
</script>

<style scoped></style>
