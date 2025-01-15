<template>
  <div>
    <div v-if="objectType === 'plant'" class="md:ml-12 block sm:flex gap-2 md:gap-4">
      <DsfrInputGroup class="max-w-sm" v-if="plantParts.length > 0">
        <DsfrSelect
          label="Partie utilisée"
          defaultUnselectedText=""
          v-model.number="model.usedPart"
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
          v-model.number="model.unit"
          defaultUnselectedText=""
          :required="true"
        />
      </DsfrInputGroup>
      <DsfrInputGroup class="max-w-sm">
        <DsfrSelect
          label="Préparation"
          :options="store.preparations?.map((preparation) => ({ text: preparation.name, value: preparation.id }))"
          v-model.number="model.preparation"
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
        <NumberField label="Qté par DJR" v-model="model.quantity" label-visible :required="true" />
      </DsfrInputGroup>
      <div class="mt-12" v-if="model.element?.unit">
        {{ model.element.unit }}
      </div>
      <div v-else>
        <DsfrInputGroup class="min-w-20 max-w-24">
          <DsfrSelect
            label="Unité"
            :options="store.units?.map((unit) => ({ text: unit.name, value: unit.id }))"
            v-model.number="model.unit"
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
          v-model.number="model.unit"
          defaultUnselectedText=""
          :required="true"
        />
      </DsfrInputGroup>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue"
import { useRootStore } from "@/stores/root"
import NumberField from "@/components/NumberField"

const model = defineModel()
const store = useRootStore()
const props = defineProps({ objectType: { type: String } })

const plantParts = computed(() => {
  const parts = model.value.element?.plantParts || store.plantParts
  return parts?.map((x) => ({ text: x.name, value: x.id }))
})
</script>
