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

        <div><DsfrButton secondary @click="$emit('remove', model)">Enlever</DsfrButton></div>
      </div>
    </div>

    <div v-if="showFields">
      <hr class="mt-2" />
      <div v-if="objectType === 'plant'" class="md:ml-12 block sm:flex gap-2 md:gap-4">
        <DsfrInputGroup class="max-w-sm" v-if="plantParts.length > 0">
          <DsfrSelect
            label="Partie utilisée"
            defaultUnselectedText=""
            v-model="model.usedPart"
            :options="plantParts"
            :required="true"
          />
        </DsfrInputGroup>
        <DsfrInputGroup class="max-w-28">
          <NumberField label="Qté par DJR" v-model="model.quantity" label-visible :required="true" />
        </DsfrInputGroup>
        <DsfrInputGroup class="min-w-20 max-w-24">
          <DsfrSelect
            label="Unité"
            :options="store.units?.map((unit) => ({ text: unit.name, value: unit.id }))"
            v-model="model.unit"
            defaultUnselectedText=""
            :required="true"
          />
        </DsfrInputGroup>
        <DsfrInputGroup class="max-w-sm">
          <DsfrSelect
            label="Préparation"
            :options="store.preparations?.map((preparation) => ({ text: preparation.name, value: preparation.id }))"
            v-model="model.preparation"
            defaultUnselectedText=""
            :required="true"
          />
        </DsfrInputGroup>
      </div>
      <div v-else-if="objectType === 'microorganism'" class="ml-12 flex gap-4">
        <DsfrInputGroup class="max-w-sm">
          <DsfrInput label-visible label="Souche" v-model="model.strain" :required="true" />
        </DsfrInputGroup>
        <div class="mt-12">
          <DsfrCheckbox
            v-model="model.activated"
            :label="model.activated ? 'Activés' : 'Ces micro-organismes ont été inactivés'"
            hint="L'inactivation rend la réplication impossible"
          />
        </div>
        <div v-if="model.activated">
          <DsfrInputGroup>
            <NumberField label-visible v-model="model.quantity" label="Qté par DJR (en UFC)" :required="true" />
          </DsfrInputGroup>
        </div>
      </div>
      <div v-else-if="objectType === 'substance'" class="ml-12 flex gap-4">
        <DsfrInputGroup class="max-w-28">
          <DsfrInput label="Qté par DJR" v-model="model.quantity" label-visible :required="true" />
        </DsfrInputGroup>
        <div class="mt-12" v-if="model.element?.unit">
          {{ model.element.unit }}
        </div>
        <div v-else>
          <DsfrInputGroup class="min-w-20 max-w-24">
            <DsfrSelect
              label="Unité"
              :options="store.units?.map((unit) => ({ text: unit.name, value: unit.id }))"
              v-model="model.unit"
              defaultUnselectedText=""
              :required="true"
            />
          </DsfrInputGroup>
        </div>
      </div>
      <div v-else-if="objectType === 'form_of_supply' || objectType === 'active_ingredient'" class="ml-12 flex gap-4">
        <DsfrInputGroup>
          <NumberField label-visible v-model="model.quantity" label="Qté par DJR" :required="true" />
        </DsfrInputGroup>
        <DsfrInputGroup class="min-w-20 max-w-24">
          <DsfrSelect
            label="Unité"
            :options="store.units?.map((unit) => ({ text: unit.name, value: unit.id }))"
            v-model="model.unit"
            defaultUnselectedText=""
            :required="true"
          />
        </DsfrInputGroup>
      </div>
    </div>
  </div>
</template>

<script setup>
import NumberField from "@/components/NumberField"
import { useRootStore } from "@/stores/root"
import { computed, watch } from "vue"
import { getElementName } from "@/utils/elements"
import { getActivityReadonlyByType } from "@/utils/mappings"
import ElementCommentModal from "@/components/ElementCommentModal"

const model = defineModel()
const store = useRootStore()

defineEmits(["remove"])
const props = defineProps({ objectType: { type: String } })
const synonyms = computed(() => model.value.element?.synonyms?.map((x) => x.name)?.join(", "))

const plantParts = computed(() => {
  const parts = model.value.element?.plantParts || store.plantParts
  return parts?.map((x) => ({ text: x.name, value: x.id }))
})

const showFields = computed(() => {
  if (model.value.active && ["plant", "microorganism"].indexOf(props.objectType) >= 0) return true
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
watch(model.value.quantity, () => {
  if (model.value.element?.unit) {
    model.value.unit = model.value.element.unit
    console.log(model.value.element.name + model.value.unit)
    console.log(model.value)
  }
})
</script>
