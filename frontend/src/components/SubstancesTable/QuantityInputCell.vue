<template>
  <div v-if="payload">
    <div v-if="readonly">
      <div>
        {{ payload.computedSubstances[rowIndex].quantity }}
      </div>
      <div
        :class="{
          'text-red-marianne-425! font-bold': getMaxQuantityExceeded(payload, payload.computedSubstances[rowIndex]),
        }"
      >
        {{ getMaxQuantityExceeded(payload, payload.computedSubstances[rowIndex]) }}
      </div>
      <p v-if="amountInfoText[rowIndex]" class="amount-info-text">
        <v-icon name="ri-information-fill"></v-icon>
        {{ amountInfoText }}
      </p>
    </div>

    <!-- Champ input -->
    <div v-else class="-mt-1 pb-1">
      <DsfrInputGroup>
        <NumberField
          v-model="payload.computedSubstances[rowIndex].quantity"
          label="Quantité par DJR"
          :required="payload.computedSubstances[rowIndex].substance.mustSpecifyQuantity"
          :descriptionId="`substance-info-${rowIndex}`"
        />
        <div class="text-neutral-500! mt-1" v-if="payload.computedSubstances[rowIndex].substance.mustSpecifyQuantity">
          * champ obligatoire
        </div>
        <p
          v-if="amountInfoText[rowIndex]"
          role="alert"
          aria-live="polite"
          :id="`substance-info-${rowIndex}`"
          class="amount-info-text"
        >
          <v-icon name="ri-information-fill"></v-icon>
          {{ amountInfoText }}
        </p>
      </DsfrInputGroup>
    </div>
  </div>
</template>

<script setup>
import NumberField from "@/components/NumberField"

const payload = defineModel()
defineProps({ amountInfoText: String, readonly: Boolean, rowIndex: Number })

// cette logique devrait reflechir la logique de `_has_max_quantity_exceeded`
// substance ici est une substance déclarée ou calculée
const getMaxQuantityExceeded = (declaration, substance) => {
  if (!declaration.hasMaxQuantityExceeded) return
  const exceededSubstances = declaration.declaredSubstancesWithMaxQuantityExceeded.concat(
    declaration.computedSubstancesWithMaxQuantityExceeded
  )
  // si la substance n'est pas identifiée par le back, arrête
  if (exceededSubstances.indexOf(substance.id) === -1) return

  if (!payload.value.populations?.length) {
    // si il y a aucune population cible, on sait que le max excédé c'est pour pop generale
    return "Maximum excédé : " + substance.substance.maxQuantity + " pour Population générale"
  }

  let maxQuantitiesExceeded = substance.substance.maxQuantities
    .filter((q) => substance.quantity > q.maxQuantity)
    .filter((q) => payload.value.populations.indexOf(parseInt(q.population?.id)) != -1)
  if (!maxQuantitiesExceeded.length)
    maxQuantitiesExceeded = substance.substance.maxQuantities.filter(
      (q) => q.population?.name === "Population générale"
    )
  const intro = maxQuantitiesExceeded.length > 1 ? "Maximums excédés : " : "Maximum excédé : "
  return intro + maxQuantitiesExceeded.map((p) => `${p.maxQuantity} pour ${p.population?.name}`).join(", ")
}
</script>

<style scoped>
@reference "../../styles/index.css";

p.amount-info-text {
  @apply mt-2;
  @apply text-sm;
  @apply border;
  @apply rounded;
  @apply p-1;
}
</style>
