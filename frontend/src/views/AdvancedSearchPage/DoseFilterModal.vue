<template>
  <div>
    <DsfrModal size="lg" title="Filtrer par dose" :opened="opened" @close="opened = false" :actions="modalActions">
      <div class="min-h-96">
        <div class="flex gap-4 items-end">
          <ElementAutocomplete
            v-model="ingredientSearchTerm"
            label="Ingrédient"
            label-visible
            class="w-3/4"
            hint="Cherchez l'ingrédient pour lequel vous souhaitez filtrer par dose."
            @selected="addIngredient"
            :hideSearchButton="true"
            :chooseFirstAsDefault="false"
          />
        </div>
        <div v-if="selectedIngredient">
          <hr class="mt-6 pb-2" />
          <div class="flex gap-4 mt-4 mb-8 items-end">
            <div class="w-2/4 flex border items-center rounded p-2">
              <div
                :class="`flex mr-2 self-center justify-center rounded-full icon icon-${selectedIngredient.objectType} size-6`"
              >
                <v-icon
                  fill="white"
                  class="self-center"
                  :name="getTypeIcon(selectedIngredient.objectType)"
                  scale="0.8"
                ></v-icon>
              </div>
              <div>
                <p class="!mb-0 fr-text--sm font-bold">
                  {{ selectedIngredient.name }}
                </p>
                <p class="!mb-0 fr-text--sm italic">{{ getTypeInFrench(selectedIngredient.objectType) }}</p>
              </div>
            </div>
            <div>
              <DsfrSelect
                v-if="ingredientIsPlant"
                label="Partie de plante"
                defaultUnselectedText="Toutes"
                v-model="selectedPart"
                :options="plantPartOptions"
              />
            </div>
          </div>
          <div class="flex gap-4">
            <div class="w-5/12">
              <DsfrSelect
                label="Opération"
                :options="operationOptions"
                v-model="selectedOperation"
                defaultUnselectedText=""
                :required="true"
              />
            </div>
            <div class="mb-4 w-2/12">
              <NumberField
                :label="showDoubleQuantity ? 'Quantité A' : 'Quantité'"
                v-model="quantity"
                label-visible
                :required="true"
              />
            </div>
            <div class="mb-4 w-2/12" v-if="showDoubleQuantity">
              <NumberField label="Quantité B" v-model="upperLimitQuantity" label-visible :required="true" />
            </div>
            <div class="w-3/12">
              <DsfrSelect
                label="Unité"
                :options="unitOptions"
                v-model="selectedUnit"
                defaultUnselectedText=""
                :required="true"
              />
            </div>
          </div>
        </div>
      </div>
    </DsfrModal>
    <p class="mb-2" v-if="filterString">HAI</p>
    <p class="mb-2 italic" v-else>Aucun filtrage par dose n'est appliqué.</p>
    <DsfrButton
      tertiary
      @click="opened = true"
      size="small"
      :icon="filterString ? 'ri-edit-line' : 'ri-add-line'"
      :label="filterString ? 'Modifier le filtre' : 'Ajouter un filtre dose'"
    />
  </div>
</template>

<script setup>
/*
Le String résultant codifie le filtre par dose.
"<type d'élément>||<ID de l'élément>||<opération>||<quantité>||<ID de l'unité>"

« opération » peut être : >, ≥, <, ≤, =, ≬

Dans le cas des plantes, le string change pour inclure la partie de plante (facultative):
"plant||<ID de la plante>|<ID de la partie>||<opération>||<quantité>||<ID de l'unité>"

Dans le cas de l'opération "entre a et b" (≬), les deux quantités sont séparés de |
"<type d'élément>||<ID de l'élément>||≬||<quantité A>|<quantité B>||<ID de l'unité>"
*/
import NumberField from "@/components/NumberField"
import { ref, computed } from "vue"
import ElementAutocomplete from "@/components/ElementAutocomplete.vue"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import { getTypeIcon, getTypeInFrench } from "@/utils/mappings"

const OPERATION = { GT: ">", GTE: "≥", LT: "<", LTE: "≤", EQ: "=", BT: "≬" }

const props = defineProps({ filterString: { type: String, default: "" } })

const ingredientSearchTerm = ref()

const selectedIngredient = ref()
const selectedPart = ref() // Utilisé seulement dans le cas des plantes
const selectedOperation = ref()
const quantity = ref()
const upperLimitQuantity = ref() // Utilisé seulement dans l'opération ≬ "entre a et b"
const selectedUnit = ref()

const { units, plantParts } = storeToRefs(useRootStore())

const ingredientIsPlant = computed(() => selectedIngredient.value?.objectType === "plant")

const addIngredient = (ingredient) => {
  selectedIngredient.value = ingredient
  if (!ingredientIsPlant.value) selectedPart.value = null
}

const showDoubleQuantity = computed(() => selectedOperation.value === OPERATION.BT)

// Options pour les DsfrSelect
const plantPartOptions = computed(() => plantParts.value?.map((x) => ({ text: x.name, value: x.id })))
const unitOptions = computed(() => units.value?.map((x) => ({ text: x.name, value: x.id })))
const operationOptions = [
  { text: "Dose supérieure à (>)", value: OPERATION.GT },
  { text: "Dose supérieure ou égale à (≥)", value: OPERATION.GTE },
  { text: "Dose inférieure à (<)", value: OPERATION.LT },
  { text: "Dose inférieure ou égale à (≤)", value: OPERATION.LTE },
  { text: "Dose égale à (=)", value: OPERATION.EQ },
  { text: "Dose entre deux valeurs", value: OPERATION.BT },
]

// Gestion de la modale
const opened = ref(false)
const modalActions = [
  {
    label: "Confirmer",
    onClick: () => console.log("emit something"),
  },
  {
    label: "Annuler",
    secondary: true,
    onClick: () => (opened.value = false),
  },
]
</script>
