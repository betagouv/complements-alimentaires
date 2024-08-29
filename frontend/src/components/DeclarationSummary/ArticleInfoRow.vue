<template>
  <div class="flex justify-between items-center border-2 p-2">
    <DsfrModal
      :actions="[{ label: 'Valider' }]"
      @close="articleModalOpened = false"
      :opened="articleModalOpened"
      title="Changer l'article"
    >
      <p>Vous pouvez changer l'article de cette déclaration en le sélectionnant ci-dessous.</p>
      <DsfrInputGroup>
        <DsfrRadioButtonSet v-model="payload.article" name="Article" legend="" :options="options"></DsfrRadioButtonSet>
      </DsfrInputGroup>
    </DsfrModal>

    <div v-if="!payload.article">Article inconnu</div>
    <DsfrBadge no-icon v-else :label="articleOptions.find((x) => x.value === payload.article)?.text" />
    <DsfrButton size="sm" tertiary label="Changer l'article" @click="articleModalOpened = true" />
  </div>
</template>

<script setup>
import { ref } from "vue"
import { articleOptions } from "@/utils/mappings"
const articleModalOpened = ref(false)

const omitOptions = ["ART_17", "ART_15_WARNING"]
const options = articleOptions
  .filter((x) => omitOptions.indexOf(x.value) === -1)
  .map((x) => ({ value: x.value, label: x.text }))

const payload = defineModel()
</script>
