<template>
  <div class="p-4 border shadow-md">
    <div class="sm:flex">
      <div class="flex">
        <div class="self-center">
          <div class="font-bold capitalize">
            {{ getElementName(model).toLowerCase() }}
          </div>
          <div v-if="synonyms">
            {{ synonyms }}
          </div>
          <div v-if="model.new" class="self-center mt-1">
            <DsfrBadge label="Nouvel ingrédient" type="info" />
          </div>
          <div v-else-if="plantPartStatus === 'inconnu'" class="self-center mt-1">
            <DsfrBadge label="Nouvelle partie de plante" type="info" />
          </div>
          <div v-else-if="plantPartStatus === 'non autorisé'" class="self-center mt-1">
            <DsfrBadge label="Partie de plante non autorisée" type="warning" />
          </div>
        </div>
        <div class="content-center ml-6 pl-4 sm:border-l">
          <ElementCommentModal v-model="model" :hidePrivateComments="true" />
        </div>
      </div>

      <div class="flex grow">
        <div class="grow sm:pl-4 sm:ml-4 pt-4 sm:border-l self-center">
          <DsfrCheckbox
            :disabled="getActivityReadonlyByType(objectType)"
            v-model="model.active"
            :label="model.active ? 'Actif' : 'Non actif'"
          />
        </div>

        <div v-if="props.canRemove">
          <DsfrButton secondary @click="$emit('remove', model)">
            Enlever
            <span class="fr-sr-only">« {{ getElementName(model).toLowerCase() }} »</span>
          </DsfrButton>
        </div>
      </div>
    </div>

    <div v-if="showFields">
      <hr class="mt-2" />
      <div v-if="objectType === 'plant'" class="md:flex gap-2 md:gap-4 items-end">
        <div class="mb-4 md:max-w-sm" v-if="plantParts.length > 0">
          <DsfrSelect
            label="Partie utilisée"
            defaultUnselectedText=""
            v-model.number="model.usedPart"
            :options="plantParts"
            :required="true"
          />
        </div>
        <div class="mb-4 md:max-w-28">
          <NumberField label="Qté par DJR" v-model="model.quantity" label-visible :required="true" />
        </div>
        <div class="mb-4 min-w-20 md:max-w-24">
          <DsfrSelect
            label="Unité"
            :options="store.units?.map((unit) => ({ text: unit.name, value: unit.id }))"
            v-model.number="model.unit"
            defaultUnselectedText=""
            :required="true"
          />
        </div>
        <div class="mb-4 md:max-w-sm">
          <DsfrSelect
            label="Préparation"
            :options="preparations"
            v-model.number="model.preparation"
            defaultUnselectedText=""
            :required="model.active"
          />
        </div>
      </div>
      <div v-else-if="objectType === 'microorganism'" class="md:flex gap-4 items-end">
        <div class="mb-4 md:max-w-sm">
          <DsfrInput label-visible label="Souche" v-model="model.strain" :required="true" />
        </div>
        <div class="md:max-w-sm">
          <DsfrCheckbox
            v-model="model.activated"
            :label="model.activated ? 'Activés' : 'Ces micro-organismes ont été inactivés'"
            hint="L'inactivation rend la réplication impossible"
          />
        </div>
        <div v-if="model.activated" class="mb-4">
          <NumberField label-visible v-model="model.quantity" label="Qté par DJR (en UFC)" :required="true" />
        </div>
      </div>
      <div v-else-if="objectType === 'substance'" class="md:flex gap-4 items-end">
        <div class="mb-4">
          <NumberField label="Qté par DJR" v-model="model.quantity" label-visible :required="true" />
        </div>
        <div v-if="model.element?.unit" class="mb-4">
          {{ model.element.unit }}
        </div>
        <div v-else class="mb-4 min-w-20 md:max-w-24">
          <DsfrSelect
            label="Unité"
            :options="store.units?.map((unit) => ({ text: unit.name, value: unit.id }))"
            v-model.number="model.unit"
            defaultUnselectedText=""
            :required="true"
          />
        </div>
      </div>
      <div v-else-if="objectType === 'form_of_supply' || objectType === 'active_ingredient'" class="md:flex gap-4">
        <div class="mb-4">
          <NumberField label-visible v-model="model.quantity" label="Qté par DJR" :required="true" />
        </div>
        <div class="mb-4 min-w-20 md:max-w-24">
          <DsfrSelect
            label="Unité"
            :options="store.units?.map((unit) => ({ text: unit.name, value: unit.id }))"
            v-model.number="model.unit"
            defaultUnselectedText=""
            :required="true"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import NumberField from "@/components/NumberField"
import { useRootStore } from "@/stores/root"
import { computed, watch, ref, onMounted } from "vue"
import { getElementName } from "@/utils/elements"
import { getActivityReadonlyByType, ingredientStatuses } from "@/utils/mappings"
import ElementCommentModal from "@/components/ElementCommentModal"

const model = defineModel()
const store = useRootStore()

defineEmits(["remove"])
const props = defineProps({
  objectType: { type: String },
  canRemove: { type: Boolean, default: true },
  canAddNewPlantPart: { type: Boolean },
})
const synonyms = computed(() => model.value.element?.synonyms?.map((x) => x.name)?.join(", "))

const plantParts = computed(() => {
  const elementParts = model.value.element?.plantParts || []
  const authorizedParts = elementParts
    .filter((p) => p.status === ingredientStatuses.AUTHORIZED.apiValue)
    .sort((a, b) => a.name.localeCompare(b.name))
  const unauthorizedParts = elementParts
    .filter((p) => p.status === ingredientStatuses.NOT_AUTHORIZED.apiValue)
    .sort((a, b) => a.name.localeCompare(b.name))
  let parts = authorizedParts
  if (props.canAddNewPlantPart || !elementParts.length) {
    if (parts.length) {
      parts.unshift({ text: "Parties autorisées", disabled: true })
      if (unauthorizedParts.length) {
        parts.push({ text: "Parties non autorisées", disabled: true })
        parts = parts.concat(unauthorizedParts)
      }
      parts.push({ text: "Toutes les parties", disabled: true })
    }
    const allParts = [].concat(store.plantParts).sort((a, b) => a.name.localeCompare(b.name))
    parts = parts.concat(allParts)
  }
  return parts.map((x) => {
    return x.text ? x : { text: x.name, value: x.id }
  })
})

const preparations = computed(() => {
  const p = [].concat(store.preparations).sort((a, b) => a.name.localeCompare(b.name))
  return p.map((preparation) => ({ text: preparation.name, value: preparation.id }))
})

const showFields = computed(() => {
  if (props.objectType === "plant") return true
  if (model.value.active && props.objectType === "microorganism") return true
  if (
    model.value.active &&
    ["active_ingredient", "form_of_supply", "substance"].indexOf(props.objectType) >= 0 &&
    !model.value.element?.substances?.length
  )
    // TODO: à terme les form_of_supply auront forcément des substances liées donc cette condition ne sera plus nécessaire
    // TODO: à terme le type active_ingredient n'existera plus, seulement le type ingrédient et la propriété active
    return true
  return false
})

// Reset de l'unité si le microorganism est inactivé
watch(
  () => model.value.activated,
  (activatedField) => {
    if (activatedField == false) {
      model.value.quantity = null
    }
  }
)

const plantPartStatus = ref("")
const setPartStatus = (part) => {
  plantPartStatus.value = ""
  if (part && model.value.element?.plantParts?.length) {
    const associatedPart = model.value.element.plantParts.find((p) => p.id === part)
    plantPartStatus.value = associatedPart?.status || "inconnu"
  }
}
watch(() => model.value.usedPart, setPartStatus)
onMounted(() => setPartStatus(model.value.usedPart))
</script>
