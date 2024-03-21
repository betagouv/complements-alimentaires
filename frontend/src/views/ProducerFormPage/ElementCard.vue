<template>
  <div class="p-4 border shadow-md">
    <div class="sm:flex">
      <div class="flex">
        <div :class="`mr-4 self-center justify-center rounded-full icon icon-${model.element.objectType} size-8 flex`">
          <v-icon class="self-center" fill="white" :name="getTypeIcon(model.element.objectType)" />
        </div>
        <div class="self-center">
          <div class="font-bold capitalize">
            {{ model.element.name.toLowerCase() }}
            <span class="uppercase text-gray-400 text-sm ml-2">{{ getType(model.element.objectType) }}</span>
          </div>
          <div v-if="model.element.synonyms?.length">
            {{ model.element.synonyms.map((x) => x.name).join(", ") }}
          </div>
          <div v-if="model.element.new" class="self-center mt-1">
            <DsfrBadge label="Nouvel ingrédient" type="info" />
          </div>
        </div>
      </div>
      <div class="flex grow">
        <div class="grow pl-4 ml-6 sm:border-l self-center">
          <DsfrCheckbox
            class="!my-2"
            v-model="model.element.active"
            :label="model.element.active ? 'Actif' : 'Non actif'"
          />
        </div>
        <div><DsfrButton secondary @click="$emit('remove', element)">Enlever</DsfrButton></div>
      </div>
    </div>
    <div v-if="showFields">
      <hr class="mt-2" />
      <div v-if="model.element.objectType === 'plant'" class="md:ml-12 block sm:flex gap-2 md:gap-4">
        <DsfrInputGroup class="max-w-sm" v-if="plantParts.length > 0">
          <DsfrSelect
            label="Partie utilisée"
            defaultUnselectedText=""
            v-model="model.plantPart"
            :options="plantParts"
            :required="true"
          />
        </DsfrInputGroup>
        <DsfrInputGroup class="max-w-28">
          <DsfrInput label="Qté par DJR" v-model="model.quantity" label-visible :required="true" />
        </DsfrInputGroup>
        <DsfrInputGroup class="min-w-20 max-w-24">
          <DsfrSelect
            label="Unité"
            :options="store.units?.map((unit) => unit.name)"
            v-model="model.unit"
            defaultUnselectedText=""
            :required="true"
          />
        </DsfrInputGroup>
        <DsfrInputGroup class="max-w-sm">
          <DsfrSelect
            label="Préparation"
            :options="preparations"
            v-model="model.preparation"
            defaultUnselectedText=""
            :required="true"
          />
        </DsfrInputGroup>
      </div>
      <div v-else-if="model.element.objectType === 'microorganism'" class="ml-12 flex gap-4">
        <DsfrInputGroup class="max-w-sm">
          <DsfrInput label-visible label="Souche" v-model="model.strain" :required="true" />
        </DsfrInputGroup>
        <DsfrInputGroup>
          <DsfrInput label-visible v-model="model.cfu_quantity" label="Qté par DJR (en CFU)" :required="true" />
        </DsfrInputGroup>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRootStore } from "@/stores/root"
import { computed, defineModel } from "vue"
import { getTypeIcon, getType } from "@/utils/mappings"

const model = defineModel()
const store = useRootStore()
defineEmits(["remove"])

const plantParts = computed(() => {
  const parts = model.value.element.plantParts || store.plantParts
  return parts.map((x) => ({ text: x.name, value: x.id }))
})
const showFields = computed(
  () =>
    model.value.element.active &&
    (model.value.element.objectType === "plant" || model.value.element.objectType === "microorganism")
)

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
