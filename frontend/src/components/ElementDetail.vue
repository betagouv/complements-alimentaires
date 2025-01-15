<template>
  <div>
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
          :options="store.preparations?.map((preparation) => ({ text: preparation.name, value: preparation.id }))"
          v-model.number="model.preparation"
          defaultUnselectedText=""
          :required="true"
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
</template>

<script setup>
import { computed } from "vue"
import { useRootStore } from "@/stores/root"
import NumberField from "@/components/NumberField"

const model = defineModel()
const store = useRootStore()
store.fetchDeclarationFieldsData()
const props = defineProps({ objectType: { type: String } })

const plantParts = computed(() => {
  const parts = model.value.element?.plantParts || store.plantParts
  return parts?.map((x) => ({ text: x.name, value: x.id })) || []
})
</script>
