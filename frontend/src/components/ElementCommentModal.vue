<template>
  <div class="flex border w-8 aspect-square rounded-full content-center justify-center">
    <DsfrModal :title="elementName" size="lg" :opened="infoModalOpened" @close="infoModalOpened = false">
      <div v-if="element?.publicComments">
        <p class="font-bold mb-2">Commentaires</p>
        <p>{{ element?.publicComments }}</p>
      </div>
      <div v-if="element?.privateComments && !hidePrivateComments">
        <p class="font-bold mb-2">Commentaires privés</p>
        <p>{{ element?.privateComments }}</p>
      </div>
      <!-- TODO -->
      <div v-if="maxQuantity">
        <p class="font-bold mb-2">Quantité maximale autorisée</p>
        <p>{{ maxQuantity }} {{ element?.unit }}</p>
      </div>
      <div v-if="constitutingSubstances && constitutingSubstances.length">
        <p class="font-bold mb-2">Substances</p>
        <ul>
          <li v-for="substance in constitutingSubstances" :key="`Substance-${substance.id}`">
            <p class="capitalize font-bold mb-1">{{ getElementName({ element: substance }) }}</p>
            <p class="mb-2" v-if="substance.maxQuantity">
              Quantité maximale autorisée : {{ substance.maxQuantity }} {{ substance?.unit }}
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

const maxQuantity = computed(() => element.value?.maxQuantity)
const constitutingSubstances = computed(() => element.value?.substances)

const tooltipContent = computed(() => {
  let content = ""
  if (element.value?.publicComments) content += `Commentaires :\n\n${element.value?.publicComments}`
  if (element.value?.privateComments && !props.hidePrivateComments)
    content += `\n\nCommentaires privés :\n\n${element.value?.privateComments}`
  return content || "Pas de commentaires"
})

const infoModalOpened = ref(false)
const hasInformationToShow = computed(
  () =>
    element.value?.publicComments ||
    (element.value?.privateComments && !props.hidePrivateComments) ||
    maxQuantity.value ||
    constitutingSubstances.value?.length
)
</script>

<style scoped>
/* Il est nécessaire de surcharger certains styles di DSFRTooltip car un element a[href] est ajouté */
div :deep(.tooltip-comments) {
  @apply !bg-none;
  @apply !flex;
  @apply !w-full;
  @apply !justify-center;
}
</style>
