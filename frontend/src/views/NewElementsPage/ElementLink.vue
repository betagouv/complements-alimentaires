<template>
  <span>
    «
    <router-link
      :to="{ name: 'DeclaredElementPage', params: { type: element.type, id: element.id } }"
      class="text-blue-france-sun-113"
    >
      {{ elementName }}
    </router-link>
    »
  </span>
</template>

<script setup>
import { computed } from "vue"
import { getNewElementName } from "@/utils/elements"

const props = defineProps({ element: Object })

const elementName = computed(() => getNewElementName(props.element))
</script>
