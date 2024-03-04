<template>
  <div class="p-4 border flex">
    <div>
      <v-icon scale="0.85" class="mr-2" :name="getTypeIcon(props.element.objectType)" />
    </div>
    <div class="grow">
      <div class="font-bold capitalize">
        {{ props.element.name.toLowerCase() }}
      </div>
      <div v-if="props.element.synonyms?.length">
        {{ props.element.synonyms.map((x) => x.name).join(", ") }}
      </div>
    </div>
    <div>
      <DsfrButton secondary @click="$emit('remove', element)">Enlever</DsfrButton>
    </div>
  </div>
</template>

<script setup>
import { getTypeIcon } from "@/utils/mappings"

const props = defineProps({
  element: String,
})
</script>
