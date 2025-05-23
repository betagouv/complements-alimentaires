<template>
  <div>
    <DsfrTable
      ref="table"
      class="w-full"
      title="Entreprises mandatées"
      :headers="headers"
      :rows="rows"
      :no-caption="true"
      :pagination="false"
    />
    <DsfrModal title="Veuillez confirmer" :opened="confirmationModalOpened" @close="closeRemovalModal">
      <p>Voulez-vous vraiment retirer ce mandat ?</p>
      <div class="flex gap-4">
        <DsfrButton secondary label="Non, revenir en arrière" @click="closeRemovalModal" />
        <DsfrButton icon="ri-close-fill" label="Oui, je veux le retirer" @click="removeMandate" />
      </div>
    </DsfrModal>
  </div>
</template>

<script setup>
import { computed, ref } from "vue"

const props = defineProps({ mandatedCompanies: { type: Array, default: () => [] } })
const emit = defineEmits(["remove"])

const confirmationModalOpened = ref(false)
const removalCompanyId = ref(null)

const orderedCompanies = computed(() =>
  [...props.mandatedCompanies].sort((a, b) => a.socialName.localeCompare(b.socialName))
)

const headers = ["Entreprise", "SIRET", "Numéro de TVA", ""]
const rows = computed(() =>
  orderedCompanies.value.map((x) => ({
    rowData: [
      x.socialName,
      x.siret || "—",
      x.vat || "—",
      {
        component: "dsfr-button",
        label: "Supprimer",
        secondary: true,
        size: "sm",
        icon: "ri-close-fill",
        onclick: () => openRemovalModal(x.id),
      },
    ],
  }))
)
const openRemovalModal = (companyId) => {
  removalCompanyId.value = companyId
  confirmationModalOpened.value = true
}

const closeRemovalModal = () => {
  removalCompanyId.value = null
  confirmationModalOpened.value = false
}

const removeMandate = () => {
  emit("remove", removalCompanyId.value)
  closeRemovalModal()
}
</script>

<style scoped>
@reference "../../styles/index.css";

.fr-table :deep(table) {
  @apply table!;
}
</style>
