<template>
  <DsfrAlert
    v-if="element && alertType"
    :type="alertType"
    small
    closeable
    :closed="closed"
    @close="closed = true"
    class="mb-4"
  >
    <p v-if="element.requestStatus === 'INFORMATION'">
      Des informations complémentaires sont nécessaires pour la demande d'ajout de l'ingrédient
      <ElementLink :element="element" />
    </p>
    <p v-else-if="element.requestStatus === 'REJECTED'">
      La demande d'ajout de l'ingrédient
      <ElementLink :element="element" />
      a été refusée
    </p>
    <p v-else-if="element.requestStatus === 'REPLACED'">
      L'ingrédient ajouté
      <ElementLink :element="element" />
      a été remplacé par
      <ElementLink :element="{ id: element.element.id, type: element.type, newName: element.element.name }" />
      dans la déclaration
    </p>
  </DsfrAlert>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import { useRoute } from "vue-router"
import { useFetch } from "@vueuse/core"
import { getApiType } from "@/utils/mappings"
import ElementLink from "./ElementLink"

// retrouver le détail de l'element et l'action prise
const route = useRoute()
const recentAction = computed(() => {
  return {
    id: route.query.actionedId,
    type: route.query.actionedType,
  }
})

const url = computed(
  () =>
    recentAction.value.type &&
    `/api/v1/declared-elements/${getApiType(recentAction.value.type)}/${recentAction.value.id}`
)
const { data, execute } = useFetch(url, { immediate: false }).get().json()

const element = computed(() => data.value)

onMounted(() => {
  if (recentAction.value.id) {
    execute()
  }
})

// gerer l'alert
const alertType = computed(() => {
  return {
    INFORMATION: "warning",
    REJECTED: "error",
    REPLACED: "success",
  }[element.value.requestStatus]
})

const closed = ref(false)
</script>
