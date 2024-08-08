<template>
  <DsfrAlert v-if="displayData" :type="displayData.type" :title="displayData.title">
    <p v-if="displayData.body">{{ displayData.body }}</p>
    <DsfrButton v-if="displayData.canDownloadCertificate" icon="ri-file-text-line" class="mt-2" secondary>
      <a :href="`/declarations/${declaration.id}/certificate`" target="_blank" rel="noopener noreferrer">
        Télécharger l'attestation
      </a>
    </DsfrButton>
  </DsfrAlert>
</template>

<script setup>
import { computed } from "vue"
const props = defineProps({ declaration: Object, role: { type: String, default: "declarant" } })

const displayData = computed(() => {
  switch (props.role) {
    case "declarant":
      return declarantDisplayData.value
    case "instructor":
      return instructorDisplayData.value
    case "visor":
      return visorDisplayData.value
    default:
      console.error(`Role ${props.role} not supported`)
      return null
  }
})

const declarantDisplayData = computed(() => {
  switch (props.declaration.status) {
    case "DRAFT":
      return null
    case "AWAITING_INSTRUCTION":
      return {
        type: "info",
        title: "Accusé d'enregistrement",
        body: "Votre dossier sera traité dans les meilleurs délais",
        canDownloadCertificate: true,
      }
    case "ONGOING_INSTRUCTION":
      return {
        type: "info",
        title: "Accusé d'enregistrement",
        body: "Votre dossier sera traité dans les meilleurs délais",
        canDownloadCertificate: true,
      }
    case "AWAITING_VISA":
      return {
        type: "info",
        title: "Accusé d'enregistrement",
        body: "Votre dossier sera traité dans les meilleurs délais",
        canDownloadCertificate: true,
      }
    case "ONGOING_VISA":
      return {
        type: "info",
        title: "Accusé d'enregistrement",
        body: "Votre dossier sera traité dans les meilleurs délais",
        canDownloadCertificate: true,
      }
    case "OBJECTION":
      return {
        type: "warning",
        title: "Une objection a été emise sur cette déclaration",
        body: blockingReasons.value,
        canDownloadCertificate: false,
      }
    case "OBSERVATION":
      return {
        type: "warning",
        title: "Une observation a été emise sur cette déclaration",
        body: blockingReasons.value,
        canDownloadCertificate: false,
      }
    case "AUTHORIZED":
      return { type: "success", title: "Attestation de déclaration", body: null, canDownloadCertificate: true }
    case "ABANDONED":
      return { type: "warning", title: "Ce dossier est abandonné", body: null, canDownloadCertificate: false }
    case "REJECTED":
      return {
        type: "warning",
        title: "Ce dossier a été réfusé",
        body: blockingReasons.value,
        canDownloadCertificate: true,
      }
    case "WITHDRAWN":
      return { type: "info", title: "Ce produit a été retiré du marché", canDownloadCertificate: true }
    default:
      return null
  }
})

const instructorDisplayData = computed(() => {
  switch (props.declaration.status) {
    case "DRAFT":
      return null
    case "AWAITING_INSTRUCTION":
      return {
        type: "info",
        title: "Déclaration en attente d'instruction",
        canDownloadCertificate: false,
      }
    case "ONGOING_INSTRUCTION":
      return null
    case "AWAITING_VISA":
      return {
        type: "info",
        title: "Déclaration en attente de visa / signature",
        canDownloadCertificate: false,
      }
    case "ONGOING_VISA":
      return {
        type: "info",
        title: "Déclaration en cours de visa / signature",
        canDownloadCertificate: false,
      }
    case "OBJECTION":
      return {
        type: "info",
        title: "Une objection a été emise sur cette déclaration",
        body: blockingReasons.value,
        canDownloadCertificate: false,
      }
    case "OBSERVATION":
      return {
        type: "warning",
        title: "Une observation a été emise sur cette déclaration",
        body: blockingReasons.value,
        canDownloadCertificate: false,
      }
    case "AUTHORIZED":
      return { type: "success", title: "Cette déclaration a été autorisée", body: null, canDownloadCertificate: true }
    case "ABANDONED":
      return { type: "warning", title: "Ce dossier est abandonné", body: null, canDownloadCertificate: false }
    case "REJECTED":
      return {
        type: "warning",
        title: "Ce dossier a été réfusé",
        body: blockingReasons.value,
        canDownloadCertificate: true,
      }
    case "WITHDRAWN":
      return { type: "info", title: "Ce produit a été retiré du marché", canDownloadCertificate: false }
    default:
      return null
  }
})

const visorDisplayData = computed(() => {
  switch (props.declaration.status) {
    case "DRAFT":
      return null
    case "AWAITING_INSTRUCTION":
      return {
        type: "info",
        title: "Déclaration en attente d'instruction",
        canDownloadCertificate: false,
      }
    case "ONGOING_INSTRUCTION":
      return {
        type: "info",
        title: "Déclaration en cours d'instruction",
        canDownloadCertificate: false,
      }
    case "AWAITING_VISA":
      return {
        type: "info",
        title: "Déclaration en attente de visa / signature",
        canDownloadCertificate: false,
      }
    case "ONGOING_VISA":
      return null
    case "OBJECTION":
      return {
        type: "info",
        title: "Une objection a été emise sur cette déclaration",
        body: blockingReasons.value,
        canDownloadCertificate: false,
      }
    case "OBSERVATION":
      return {
        type: "warning",
        title: "Une observation a été emise sur cette déclaration",
        body: blockingReasons.value,
        canDownloadCertificate: false,
      }
    case "AUTHORIZED":
      return { type: "success", title: "Cette déclaration a été autorisée", body: null, canDownloadCertificate: true }
    case "ABANDONED":
      return { type: "warning", title: "Ce dossier est abandonné", body: null, canDownloadCertificate: false }
    case "REJECTED":
      return {
        type: "warning",
        title: "Ce dossier a été réfusé",
        body: blockingReasons.value,
        canDownloadCertificate: true,
      }
    case "WITHDRAWN":
      return { type: "info", title: "Ce produit a été retiré du marché", canDownloadCertificate: false }
    default:
      return null
  }
})

const blockingReasons = computed(
  () => props.declaration?.blockingReasons && "- " + props.declaration?.blockingReasons?.join(",\n- ")
)
</script>
