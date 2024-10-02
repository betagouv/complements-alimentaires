<template>
  <div class="flex flex-row justify-between border p-2">
    <span class="self-center">Votre déclaration est en brouillon</span>
    <DsfrButton size="sm" icon="ri-delete-bin-line" tertiary label="Supprimer mon brouillon" @click="open" />

    <DsfrModal :actions="actions" ref="modal" @close="close" :opened="opened" title="Supprimer mon brouillon">
      La suppression de votre déclaration n'est pas réversible. Êtes-vous sûr de vouloir procéder ?
    </DsfrModal>
  </div>
</template>

<script setup>
import { ref } from "vue"
const emit = defineEmits(["delete"])

const opened = ref(false)

const actions = [
  {
    label: "Supprimer",
    onClick: () => emit("delete"),
    secondary: true,
    icon: { name: "ri-delete-bin-line", fill: "#c9191e" },
  },
  {
    label: "Revenir en arrière",
    onClick: () => close(),
  },
]

const close = () => (opened.value = false)
const open = () => (opened.value = true)
</script>
