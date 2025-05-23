<template>
  <div class="flex flex-row justify-between border p-2">
    <span class="self-center">{{ helperText }}</span>
    <DsfrButton
      class="text-red-marianne-425!"
      size="sm"
      icon="ri-delete-bin-line"
      tertiary
      :label="buttonLabel"
      @click="open"
    />

    <DsfrModal :actions="actions" ref="modal" @close="close" :opened="opened" :title="buttonLabel">
      {{ modalText }}
    </DsfrModal>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
const emit = defineEmits(["delete"])

const opened = ref(false)

const props = defineProps({
  buttonLabel: { type: String, default: "Supprimer cette déclaration" },
  helperText: { type: String, default: "" },
  modalText: { type: String, default: "" },
  actionButtonLabel: { type: String, default: "Supprimer" },
})

const actions = computed(() => [
  {
    label: props.actionButtonLabel,
    onClick: () => emit("delete"),
    secondary: true,
    icon: { name: "ri-delete-bin-line", fill: "#c9191e" },
  },
  {
    label: "Revenir en arrière",
    onClick: () => close(),
  },
])

const close = () => (opened.value = false)
const open = () => (opened.value = true)
</script>
