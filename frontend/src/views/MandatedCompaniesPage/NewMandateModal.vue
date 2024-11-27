<template>
  <div>
    <DsfrButton label="Ajouter un nouveau mandat" icon="ri-key-line" @click="opened = true" />
    <DsfrModal
      :actions="actions"
      ref="modal"
      @close="opened = false"
      :opened="opened"
      title="Ajouter un nouveau mandat"
      icon="ri-add-circle-line"
    >
      <p>
        Merci de renseigner soit le numéro SIRET soit le numéro de TVA de l'entreprise que vous souhaitez mandater pour
        vos déclarations.
      </p>
      <hr class="pb-1" />
      <DsfrInputGroup>
        <DsfrInput
          v-model="siret"
          label="Numéro SIRET"
          labelVisible
          spellcheck="false"
          autocomplete="off"
          class="max-w-md"
        />
      </DsfrInputGroup>
      <div class="flex items-baseline">
        <hr class="grow p-1" />
        <p class="px-2 mb-0 italic">Ou</p>
        <hr class="grow p-1" />
      </div>
      <DsfrInputGroup>
        <DsfrInput
          v-model="vat"
          label="Numéro de TVA intracommunautaire"
          labelVisible
          spellcheck="false"
          autocomplete="off"
          class="max-w-md"
        />
      </DsfrInputGroup>
      <hr class="pb-1" />
    </DsfrModal>
  </div>
</template>

<script setup>
import { ref } from "vue"

const emit = defineEmits(["confirm"])
const opened = ref(false)
const siret = ref("")
const vat = ref("")

const confirmMandate = () => {
  if (!siret.value && !vat.value)
    window.alert("Merci de renseigner soit le numéro SIRET soit le numéro de TVA pour créer le mandat.")
  else emit("confirm", siret.value, vat.value)
  siret.value = ""
  vat.value = ""
  opened.value = false
}

const actions = [
  {
    label: "Confirmer le mandat",
    onClick: confirmMandate,
    icon: "ri-key-line",
  },
  {
    label: "Revenir en arrière",
    onClick: () => (opened.value = false),
    secondary: true,
  },
]
</script>
