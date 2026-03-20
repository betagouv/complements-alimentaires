<template>
  <div class="flex border w-8 aspect-square rounded-full content-center justify-center">
    <DsfrModal :title="elementName" size="lg" :opened="infoModalOpened" @close="infoModalOpened = false">
      <div v-if="element?.publicComments">
        <h2 class="fr-h6 mb-2!">Commentaires</h2>
        <p class="whitespace-pre-line">{{ element?.publicComments }}</p>
      </div>
      <div v-if="element?.privateComments && !hidePrivateComments">
        <h2 class="fr-h6 mb-2!">Commentaires privés</h2>
        <p class="whitespace-pre-line">{{ element?.privateComments }}</p>
      </div>
      <div v-if="hasMaxQuantities">
        <ElementDoses :maxQuantities="maxQuantities" :unit="element?.unit" />
      </div>
      <div v-if="warningsOnLabel && warningsOnLabel.length">
        <h2 class="fr-h6 mb-2!">Avertissements</h2>
        <ul>
          <li v-for="(warning, idx) in warningsOnLabel" :key="`warning-${idx}`">
            <p class="mb-2">{{ warning }}</p>
          </li>
        </ul>
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
    <button
      @click="infoModalOpened = true"
      :disabled="!hasInformationToShow"
      @focus="onMouseOverTooltip"
      @blur="onMouseLeaveTooltip"
      @mouseover="onMouseOverTooltip"
      @mouseleave="onMouseLeaveTooltip"
      ref="source"
      :aria-describedby="tooltipContentId"
    >
      <v-icon
        :name="hasInformationToShow ? 'ri-chat-4-line' : 'ri-chat-off-line'"
        :color="hasInformationToShow ? 'rgb(0, 0, 145)' : '#AAA'"
      ></v-icon>
      <span class="fr-sr-only">Commentaires sur l'ingrédient {{ elementName }}</span>
    </button>
    <span
      :id="tooltipContentId"
      class="fr-tooltip fr-placement"
      :class="tooltipClass"
      :style="tooltipStyle"
      role="tooltip"
      ref="tooltip"
      @mouseover="isMouseOverContent = true"
      @mouseleave="onMouseLeaveTooltipContent"
    >
      {{ tooltipContent }}
    </span>
  </div>
</template>

<script setup>
import { computed, ref, useTemplateRef, watch } from "vue"
import { getElementName } from "@/utils/elements"
import { getRandomHtmlId } from "@/utils/random"
import ElementDoses from "@/components/ElementDoses.vue"

const model = defineModel()

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

const warningsOnLabel = computed(() => element.value?.warningsOnLabel)

const constitutingSubstances = computed(() => element.value?.substances)

const tooltipContentId = getRandomHtmlId("tooltip-content")

const tooltipContent = computed(() => {
  if (!hasInformationToShow.value) return "Pas d'informations supplementaires."
  let content = ""
  if (hasMaxQuantities.value) content += `Quantités maximales : ${maxQuantitiesString.value}. `
  if (warningsOnLabel.value && warningsOnLabel.value.length) content += "Cet ingrédient contient des avertissements. "
  if (element.value?.publicComments) content += `Commentaires : ${element.value?.publicComments}. `
  if (element.value?.privateComments && !props.hidePrivateComments)
    content += `Commentaires privés : ${element.value?.privateComments}. `

  if (constitutingSubstances.value && constitutingSubstances.value.length)
    content += "Cet ingrédient contient des substances."

  return content
})

const infoModalOpened = ref(false)
const hasInformationToShow = computed(
  () =>
    element.value?.publicComments ||
    (element.value?.privateComments && !props.hidePrivateComments) ||
    hasMaxQuantities.value ||
    warningsOnLabel.value ||
    constitutingSubstances.value?.length
)

// gérer le style du tooltip en reprenant le code de DsfrTooltip
// notre vérsion va au-delà de la version VueDsfr du jour :
// - option de mettre un tooltip sur un autre element interactif (bouton modal dans ce cas)
// - RGAA 10.13.2 : pouvoir survoler le contenu du tooltip
// - RGAA 10.13.1 : pouvoir masquer le tooltip avec esc sans bouger le souris
const showTooltip = ref(false)

const source = useTemplateRef("source")
const tooltip = useTemplateRef("tooltip")

const translateX = ref("0px")
const translateY = ref("0px")
const arrowX = ref("0px")
const top = ref(false)
const opacity = ref(0)

async function computePosition() {
  if (typeof document === "undefined") {
    return
  }
  if (typeof window === "undefined") {
    return
  }
  if (!showTooltip.value) {
    return
  }

  await new Promise((resolve) => setTimeout(resolve, 100))
  const sourceTop = source.value?.getBoundingClientRect().top
  const sourceHeight = source.value?.offsetHeight
  const sourceWidth = source.value?.offsetWidth
  const sourceLeft = source.value?.getBoundingClientRect().left
  const tooltipHeight = tooltip.value?.offsetHeight
  const tooltipWidth = tooltip.value?.offsetWidth
  const tooltipTop = tooltip.value?.offsetTop
  const tooltipLeft = tooltip.value?.offsetLeft

  const isTooltipAtBottom = sourceTop + sourceHeight + tooltipHeight >= window.innerHeight
  top.value = isTooltipAtBottom

  const isTooltipOnRightSide = sourceLeft + sourceWidth / 2 + tooltipWidth / 2 >= document.documentElement.offsetWidth
  const isTooltipOnLeftSide = sourceLeft + sourceWidth / 2 - tooltipWidth / 2 < 0

  translateY.value = isTooltipAtBottom
    ? `${sourceTop - tooltipTop - tooltipHeight + 8}px`
    : `${sourceTop - tooltipTop + sourceHeight - 8}px`
  opacity.value = 1
  translateX.value = isTooltipOnRightSide
    ? `${sourceLeft - tooltipLeft + sourceWidth - tooltipWidth - 4}px`
    : isTooltipOnLeftSide
      ? `${sourceLeft - tooltipLeft + 4}px`
      : `${sourceLeft - tooltipLeft + sourceWidth / 2 - tooltipWidth / 2}px`

  arrowX.value = isTooltipOnRightSide
    ? `${tooltipWidth / 2 - sourceWidth / 2 + 4}px`
    : isTooltipOnLeftSide
      ? `${-(tooltipWidth / 2) + sourceWidth / 2 - 4}px`
      : "0px"
}

watch(showTooltip, computePosition, { immediate: true })

const tooltipStyle = computed(
  () =>
    `transform: translate(${translateX.value}, ${translateY.value}); --arrow-x: ${arrowX.value}; opacity: ${opacity.value};'`
)
const tooltipClass = computed(() => ({
  "fr-tooltip--shown": showTooltip.value,
  "fr-placement--top": top.value,
  "fr-placement--bottom": !top.value,
}))

const isMouseOverContent = ref(false)
const isMouseOverTooltip = ref(false)

const onMouseOverTooltip = () => {
  showTooltip.value = true
  isMouseOverTooltip.value = true
}

const onMouseLeaveTooltip = () => {
  isMouseOverTooltip.value = false
  setTimeout(() => {
    if (!isMouseOverContent.value) showTooltip.value = false
  }, 100)
}

const onMouseLeaveTooltipContent = () => {
  isMouseOverContent.value = false
  setTimeout(() => {
    if (!isMouseOverTooltip.value) showTooltip.value = false
  }, 100)
}

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") showTooltip.value = false
})
</script>
