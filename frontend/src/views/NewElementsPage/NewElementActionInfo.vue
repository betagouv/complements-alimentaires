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
    <p>
      La demande d'ajout d'ingrédient
      <router-link
        :to="{ name: 'DeclaredElementPage', params: { type: recentAction.type, id: recentAction.id } }"
        class="text-blue-france-sun-113"
      >
        {{ elementName }}
      </router-link>
      :
      <span v-if="element.requestStatus === 'INFORMATION'">Des informations complémentaires sont nécessaires.</span>
      <span v-else-if="element.requestStatus === 'REJECTED'">La demande a été refusé.</span>
      <span v-else-if="element.requestStatus === 'REPLACED'">
        Remplacée par
        <router-link :to="elementLink">{{ element.element.name }}</router-link>
        dans la composition de la déclaration.
      </span>
    </p>
  </DsfrAlert>
</template>

<script setup>
import { computed, onMounted, ref } from "vue"
import { useRoute } from "vue-router"
import { useFetch } from "@vueuse/core"
import { getApiType } from "@/utils/mappings"
import { getNewElementName } from "@/utils/elements"

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

const elementName = computed(() => getNewElementName(element.value))
</script>
