<template>
  <div class="p-4 border shadow-md">
    <div class="flex">
      <div :class="`mr-4 self-center justify-center rounded-full icon-${modelValue.element.objectType} h-8 w-8 flex`">
        <v-icon class="self-center" fill="white" :name="getTypeIcon(modelValue.element.objectType)" />
      </div>
      <div class="grow self-center">
        <div class="font-bold capitalize">
          {{ modelValue.element.name.toLowerCase() }}
          <span class="uppercase text-gray-400 text-sm ml-2">{{ getType(modelValue.element.objectType) }}</span>
        </div>
        <div v-if="modelValue.element.synonyms?.length">
          {{ modelValue.element.synonyms.map((x) => x.name).join(", ") }}
        </div>
      </div>
      <div>
        <DsfrButton secondary @click="$emit('remove', element)">Enlever</DsfrButton>
      </div>
    </div>
    <hr
      class="mt-2"
      v-if="modelValue.element.objectType !== 'substance' && modelValue.element.objectType !== 'ingredient'"
    />
    <div v-if="modelValue.element.objectType === 'plant'" class="md:ml-12 block sm:flex gap-2 md:gap-4">
      <DsfrInputGroup class="max-w-sm" v-if="plantParts.length > 0">
        <DsfrSelect
          label="Partie utilisée"
          defaultUnselectedText=""
          v-model="modelValue.plantPart"
          :options="plantParts"
          :required="true"
        />
      </DsfrInputGroup>
      <DsfrInputGroup class="max-w-28">
        <DsfrInput label="Qté par DJR" v-model="modelValue.quantity" label-visible :required="true" />
      </DsfrInputGroup>
      <DsfrInputGroup class="min-w-20 max-w-24">
        <DsfrSelect
          label="Unité"
          :options="units"
          v-model="modelValue.unit"
          defaultUnselectedText=""
          :required="true"
        />
      </DsfrInputGroup>
      <DsfrInputGroup class="max-w-sm">
        <DsfrSelect
          label="Préparation"
          :options="preparations"
          v-model="modelValue.preparation"
          defaultUnselectedText=""
          :required="true"
        />
      </DsfrInputGroup>
    </div>
    <div v-else-if="modelValue.element.objectType === 'microorganism'" class="ml-12 flex gap-4">
      <DsfrInputGroup class="max-w-sm">
        <DsfrInput label-visible label="Souche" v-model="modelValue.strain" :required="true" />
      </DsfrInputGroup>
      <DsfrInputGroup>
        <DsfrInput label-visible v-model="modelValue.cfu_quantity" label="Qté par DJR (en CFU)" :required="true" />
      </DsfrInputGroup>
    </div>
  </div>
</template>

<script setup>
import { computed, defineModel } from "vue"
import { getTypeIcon, getType } from "@/utils/mappings"

const modelValue = defineModel()

const plantParts = computed(() => modelValue.value.element.plantParts.map((x) => ({ text: x.name, value: x.id })))

// TODO: complete it and pass it to utils
const units = [
  {
    text: "g",
    value: "g",
  },
  {
    text: "mg",
    value: "mg",
  },
  {
    text: "l",
    value: "l",
  },
]
// TODO: vérifier qu'on ait ces infos en base ou accepter de les avoir en front only
const preparations = [
  "Alcoolature",
  "Autre extrait fluide",
  "Autre extrait sec",
  "Autre macérât",
  "Baume",
  "Distillation",
  "Extrait au CO2 supercritique",
  "Extrait fluide alcoolique",
  "Extrait fluide aqueux",
  "Extrait fluide hydroalcoolique",
  "Extrait fluide hydroglycériné",
  "Extrait mou",
  "Extrait sec alcoolique",
  "Extrait sec aqueux",
  "Extrait sec hydroalcoolique",
  "Extrait sec hydroglycériné",
  "Hydrolât (eau florale)",
  "Macérât alcoolique",
  "Macérât aqueux",
  "Macérât huileux",
  "Macérât hydroalcoolique",
  "Macérât hydroglycériné",
  "Oléorésine et gomme-oléorésine",
  "Poudre (de plantes séchées ou broyées)",
  "Pression à froid",
  "Teinture",
]
</script>

<style scoped>
.icon-plant {
  @apply bg-ca-plant;
}
.icon-microorganism {
  @apply bg-ca-microorganism;
}
.icon-substance {
  @apply bg-ca-substance;
}
.icon-ingredient {
  @apply bg-ca-ingredient;
}
</style>
