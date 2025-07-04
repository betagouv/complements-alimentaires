<template>
  <div class="flex border w-8 aspect-square rounded-full content-center justify-center">
    <DsfrModal :title="elementName" size="lg" :opened="infoModalOpened" @close="infoModalOpened = false">
      <div v-if="element?.publicComments">
        <h2 class="fr-h6 mb-2!">Commentaires</h2>
        <p>{{ element?.publicComments }}</p>
      </div>
      <div v-if="element?.privateComments && !hidePrivateComments">
        <h2 class="fr-h6 mb-2!">Commentaires privés</h2>
        <p>{{ element?.privateComments }}</p>
      </div>
      <div v-if="hasMaxQuantities">
        <ElementDoses :maxQuantities="maxQuantities" :unit="element?.unit" />
      </div>
      <div v-if="constitutingSubstances && constitutingSubstances.length">
        <h2 class="fr-h6 mb-2!">Substances</h2>
        <ul>
          <li v-for="substance in constitutingSubstances" :key="`Substance-${substance.id}`">
            <p class="capitalize font-bold mb-1">{{ getElementName({ element: substance }) }}</p>
            <p class="mb-2" v-if="substance.maxQuantities && substance.maxQuantities.length">
              Quantités maximales autorisées : {{ stringifyMaxQuantities(substance.maxQuantities, substance.unit) }}
            </p>
          </li>
        </ul>
      </div>
    </DsfrModal>
    <DsfrTooltip ref="tooltip" :onHover="true" :content="tooltipContent" class="tooltip-comments">
      <button @click="infoModalOpened = true" :disabled="!hasInformationToShow">
        <v-icon
          :name="hasInformationToShow ? 'ri-chat-4-line' : 'ri-chat-off-line'"
          :color="hasInformationToShow ? 'rgb(0, 0, 145)' : '#AAA'"
        ></v-icon>
      </button>
    </DsfrTooltip>
  </div>
</template>

<script setup>
import { computed, ref, useTemplateRef, onMounted } from "vue"
import { getElementName } from "@/utils/elements"
import ElementDoses from "@/components/ElementDoses.vue"

const model = defineModel()
const tooltip = useTemplateRef("tooltip")

// Enlève le comportement par défaut de scroller vers le haut lors du click du DsfrTootlip
// en ajoutant un preventDefault du click
onMounted(() => tooltip.value?.$el?.nextElementSibling?.addEventListener?.("click", (e) => e.preventDefault()))

// Le backend sérialise les  commentaires privés seulement si l'utilisateur.ice
// fait partie de l'administartion. Néanmoins, il y a des contextes où on ne
// souhaite pas les afficher même pour eux (par ex. la déclaration)
const props = defineProps(["hidePrivateComments"])

const element = computed(() => model.value.element || model.value.substance)
const elementName = computed(() => {
  const name = getElementName(model.value)
  return name ? name.charAt(0).toUpperCase() + name.slice(1) : ""
})

const maxQuantities = computed(() => element.value?.maxQuantities)
const hasMaxQuantities = computed(() => maxQuantities.value?.length > 0)
const stringifyMaxQuantities = (maxQuantities, unit) =>
  maxQuantities.map((q) => `${q.population?.name} : ${q.maxQuantity?.toLocaleString("fr-FR")} ${unit}`).join(", ")
const maxQuantitiesString = computed(() => stringifyMaxQuantities(maxQuantities.value, element.value?.unit))

const constitutingSubstances = computed(() => element.value?.substances)

const tooltipContent = computed(() => {
  let content = ""
  if (hasMaxQuantities.value) content += `Quantités maximales : ${maxQuantitiesString.value}. `
  if (element.value?.publicComments) content += `Commentaires : ${element.value?.publicComments}. `
  if (element.value?.privateComments && !props.hidePrivateComments)
    content += `Commentaires privés : ${element.value?.privateComments}. `
  content = content || "Pas de commentaires. "

  if (constitutingSubstances.value && constitutingSubstances.value.length)
    content += "Cliquez pour plus d'informations sur les substances contenues."

  return content
})

const infoModalOpened = ref(false)
const hasInformationToShow = computed(
  () =>
    element.value?.publicComments ||
    (element.value?.privateComments && !props.hidePrivateComments) ||
    hasMaxQuantities.value ||
    constitutingSubstances.value?.length
)
</script>

<style scoped>
@reference "../styles/index.css";

/* Il est nécessaire de surcharger certains styles di DSFRTooltip car un element a[href] est ajouté */
div :deep(.tooltip-comments) {
  @apply bg-none!;
  @apply flex!;
  @apply w-full!;
  @apply justify-center!;
}
</style>
