<template>
  <li class="border-l-2 border-b pl-4 py-2">
    <DsfrAlert v-if="treatedRequest" :type="treatedRequest.type" small class="mb-2">
      <p>{{ treatedRequest.label }}</p>
      <p v-if="showRequestComment">
        <i>{{ model.requestPrivateNotes }}</i>
      </p>
    </DsfrAlert>
    <div class="md:flex justify-between">
      <div>
        <div class="flex content-center">
          <ElementCommentModal v-model="model" class="mr-2" />
          <div class="self-center">
            <p class="capitalize font-bold mb-0">
              {{ getElementName(model).toLowerCase() }}
            </p>
          </div>

          <ElementStatusBadge
            :text="model.element.status"
            v-if="showElementAuthorization && model.element?.status === 'non autorisé'"
            class="self-center ml-2"
          />

          <DsfrBadge v-if="novelFood" label="Novel Food" type="new" class="self-center ml-2" small />
          <DsfrBadge v-if="isRequest" label="Nouvel ingrédient" type="info" class="self-center ml-2" small />
          <DsfrBadge
            v-else-if="isPartRequest"
            label="Nouvelle partie de plante"
            type="info"
            class="self-center ml-2"
            small
          />
          <DsfrBadge
            v-if="treatedRequest"
            label="Demande traitée"
            class="self-center ml-2 purple-glycine"
            noIcon
            small
          />
          <DsfrBadge v-if="!model.active" label="Non-actif" type="none" class="self-center ml-2" small />
        </div>
        <p class="my-2" v-if="model.active">
          {{ elementInfo }}
        </p>
      </div>

      <div v-if="showRequestInspectionLink" class="content-center">
        <router-link
          :to="{ name: 'DeclaredElementPage', params: { type: props.objectType, id: model.id } }"
          class="fr-btn fr-btn--sm fr-btn--secondary"
        >
          <v-icon name="ri-file-add-line" class="mr-2"></v-icon>
          Contrôler la demande d’ajout
        </router-link>
      </div>
    </div>
  </li>
</template>

<script setup>
import { computed } from "vue"
import { getElementName } from "@/utils/elements"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import ElementCommentModal from "@/components/ElementCommentModal"
import ElementStatusBadge from "@/components/ElementStatusBadge"

const { plantParts, units, preparations, loggedUser } = storeToRefs(useRootStore())

const isInstructor = computed(() => loggedUser.value?.globalRoles.some((x) => x.name === "InstructionRole"))

const model = defineModel()
const props = defineProps({ objectType: { type: String }, showElementAuthorization: { type: Boolean } })

const plantPartName = computed(() => plantParts.value?.find((x) => x.id === model.value.usedPart)?.name || "Aucune")
const unitName = computed(() => units.value?.find((x) => x.id === model.value.unit)?.name || "")
const preparationName = computed(
  () => preparations.value?.find((x) => x.id === parseInt(model.value.preparation))?.name || ""
)
const novelFood = computed(() => {
  return model.value.element?.novelFood
})

const elementInfo = computed(() => {
  if (props.objectType === "microorganism") {
    const strain_label = `Souche : « ${model.value.strain} »`
    const quantity_label = model.value.quantity ? `Qté par DJR (en UFC) : ${model.value.quantity}` : null
    return [strain_label, quantity_label].filter(Boolean).join(` | `)
  }
  if (props.objectType === "plant") {
    const used_part_label = `Partie utilisée : « ${plantPartName.value} »`
    const quantity_label = model.value.quantity ? `Qté par DJR : ${model.value.quantity} ${unitName.value}` : null
    const preparation_label = model.value.preparation ? `Préparation : ${preparationName.value}` : null

    return [used_part_label, quantity_label, preparation_label].filter(Boolean).join(` | `)
  }

  if (
    props.objectType === "form_of_supply" ||
    props.objectType === "active_ingredient" ||
    props.objectType === "substance"
  )
    return model.value.quantity ? `Qté par DJR: ${model.value.quantity} ${unitName.value}` : null
  return ""
})

const isRequest = computed(() => model.value.new || model.value.requestStatus === "REPLACED")
const isPartRequest = computed(() => model.value.newPart)

const showRequestInspectionLink = computed(() => (isRequest.value || isPartRequest.value) && isInstructor.value)

const showRequestComment = computed(
  () =>
    model.value.requestPrivateNotes &&
    (model.value.requestStatus === "INFORMATION" || model.value.requestStatus === "REJECTED")
)

const treatedRequest = computed(() => {
  return {
    INFORMATION: {
      label: "Des informations complémentaires sont nécessaires concernant la demande d'ajout d'ingrédient",
      type: "warning",
    },
    REJECTED: {
      label: "La demande d'ajout d'ingrédient a été refusée",
      type: "error",
    },
    REPLACED: {
      label: "Demande initiale remplacée dans la composition",
      type: "info",
    },
  }[model.value.requestStatus]
})
</script>

<style scoped>
.purple-glycine.fr-badge :deep() {
  color: var(--purple-glycine-sun-319-moon-630);
  background-color: var(--purple-glycine-950-100);
}
</style>
