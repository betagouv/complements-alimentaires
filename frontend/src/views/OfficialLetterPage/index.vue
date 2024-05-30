<template>
  <component :is="getComponentFromName(letterName)" v-bind="allProps" />
</template>

<script setup>
import { defineAsyncComponent } from "vue"
import { useRoute } from "vue-router"

// Récupère le composant lié à la lettre, ainsi que les props de component, directement dans les query parameters
const { letterName, ...allProps } = useRoute().query

// Récupère un component correspondant à une lettre officielle, à partir de son nom
const getComponentFromName = (name) => defineAsyncComponent(() => import(`./letters/${name}`))
</script>
