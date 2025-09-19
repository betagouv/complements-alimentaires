<template>
  <DsfrAlert v-if="displayData" :type="displayData.type" :title="displayData.title">
    <p v-if="displayData.body">{{ displayData.body }}</p>
    <p v-if="displayData.expirationDate">
      <v-icon name="ri-error-warning-line"></v-icon>
      Sans retour de votre part, ce dossier expirera le {{ isoToPrettyDate(displayData.expirationDate) }}.
    </p>
    <div v-if="displayData.canDownloadCertificate">
      <DsfrButton icon="ri-file-text-line" class="mt-2" secondary>
        <a :href="`/declarations/${declaration.id}/certificate`" target="_blank" rel="noopener noreferrer">
          {{ displayData.downloadButtonText || "Télécharger l'attestation" }}
        </a>
      </DsfrButton>
      <a
        :href="`/declarations/${declaration.id}/certificate.html`"
        target="_blank"
        rel="noopener noreferrer"
        class="ml-4"
      >
        {{ displayData.downloadButtonText || "L'attestation" }} (vérsion HTML)
      </a>
    </div>
  </DsfrAlert>
</template>

<script setup>
import { computed } from "vue"
import { isoToPrettyDate } from "@/utils/date"
const props = defineProps({ declaration: Object, role: { type: String, default: "declarant" }, snapshots: Array })

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

const latestSnapshot = computed(
  () => [...(props.snapshots || [])].sort((a, b) => b.creationDate.localeCompare(a.creationDate))?.[0]
)
const canDownloadAbandonedCertificate = computed(() => latestSnapshot.value?.status === "OBJECTION")

const declarantDisplayData = computed(() => {
  switch (props.declaration.status) {
    case "DRAFT":
      return null
    case "AWAITING_INSTRUCTION":
      return {
        type: "info",
        title: "Votre dossier est en attente",
        canDownloadCertificate: true,
        downloadButtonText: "Accusé d'enregistrement",
      }
    case "ONGOING_INSTRUCTION":
      return {
        type: "info",
        title: "Votre dossier est en attente",
        canDownloadCertificate: true,
        downloadButtonText: "Accusé d'enregistrement",
      }
    case "AWAITING_VISA":
      return {
        type: "info",
        title: "Votre dossier est en attente",
        canDownloadCertificate: true,
        downloadButtonText: "Accusé d'enregistrement",
      }
    case "ONGOING_VISA":
      return {
        type: "info",
        title: "Votre dossier est en attente",
        canDownloadCertificate: true,
        downloadButtonText: "Accusé d'enregistrement",
      }
    case "OBJECTION":
      return {
        type: "warning",
        title: "Une objection a été émise sur cette déclaration",
        expirationDate: props.declaration?.expirationDate,
        body: blockingReasons.value,
        canDownloadCertificate: true,
        downloadButtonText: "Télécharger le courrier d'objection",
      }
    case "OBSERVATION":
      return {
        type: "warning",
        title: "Une observation a été émise sur cette déclaration",
        expirationDate: props.declaration?.expirationDate,
        body: blockingReasons.value,
        canDownloadCertificate: false,
      }
    case "AUTHORIZED":
      return { type: "success", title: "Attestation de déclaration", body: null, canDownloadCertificate: true }
    case "ABANDONED":
      return {
        type: "warning",
        title: "Ce dossier est abandonné",
        body: null,
        canDownloadCertificate: canDownloadAbandonedCertificate.value,
      }
    case "REJECTED":
      return {
        type: "warning",
        title: "Ce dossier a été réfusé",
        body: blockingReasons.value,
        canDownloadCertificate: true,
      }
    case "WITHDRAWN":
      return {
        type: "info",
        title: "Ce produit a été retiré du marché",
        canDownloadCertificate: true,
        body: latestSnapshot.value?.effectiveWithdrawalDate
          ? `Date effective de retrait du marché : ${isoToPrettyDate(latestSnapshot.value.effectiveWithdrawalDate)}`
          : null,
      }
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
        title: "Une objection a été émise sur cette déclaration",
        body: blockingReasons.value,
        canDownloadCertificate: true,
      }
    case "OBSERVATION":
      return {
        type: "warning",
        title: "Une observation a été émise sur cette déclaration",
        body: blockingReasons.value,
        canDownloadCertificate: false,
      }
    case "AUTHORIZED":
      return { type: "success", title: "Cette déclaration a été autorisée", body: null, canDownloadCertificate: true }
    case "ABANDONED":
      return {
        type: "warning",
        title: "Ce dossier est abandonné",
        body: null,
        canDownloadCertificate: canDownloadAbandonedCertificate.value,
      }
    case "REJECTED":
      return {
        type: "warning",
        title: "Ce dossier a été réfusé",
        body: blockingReasons.value,
        canDownloadCertificate: true,
      }
    case "WITHDRAWN":
      return {
        type: "info",
        title: "Ce produit a été retiré du marché",
        canDownloadCertificate: false,
        body: latestSnapshot.value?.effectiveWithdrawalDate
          ? `Date effective de retrait du marché : ${isoToPrettyDate(latestSnapshot.value.effectiveWithdrawalDate)}`
          : null,
      }
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
        title: "Une objection a été émise sur cette déclaration",
        body: blockingReasons.value,
        canDownloadCertificate: true,
      }
    case "OBSERVATION":
      return {
        type: "warning",
        title: "Une observation a été émise sur cette déclaration",
        body: blockingReasons.value,
        canDownloadCertificate: false,
      }
    case "AUTHORIZED":
      return { type: "success", title: "Cette déclaration a été autorisée", body: null, canDownloadCertificate: true }
    case "ABANDONED":
      return {
        type: "warning",
        title: "Ce dossier est abandonné",
        body: null,
        canDownloadCertificate: canDownloadAbandonedCertificate.value,
      }
    case "REJECTED":
      return {
        type: "warning",
        title: "Ce dossier a été réfusé",
        body: blockingReasons.value,
        canDownloadCertificate: true,
      }
    case "WITHDRAWN":
      return {
        type: "info",
        title: "Ce produit a été retiré du marché",
        canDownloadCertificate: false,
        body: latestSnapshot.value?.effectiveWithdrawalDate
          ? `Date effective de retrait du marché : ${isoToPrettyDate(latestSnapshot.value.effectiveWithdrawalDate)}`
          : null,
      }
    default:
      return null
  }
})

const blockingReasons = computed(
  () => props.declaration?.blockingReasons && "- " + props.declaration?.blockingReasons?.join(",\n- ")
)
</script>
