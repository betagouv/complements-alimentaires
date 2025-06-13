<template>
  <div>
    <DsfrAlert
      v-if="replacedRequestsWithSubstances.length"
      type="warning"
      class="mb-4"
      title="Vérifiez les doses totales des substances"
    >
      <p>Les ingrédients suivants, ajoutés pour remplacer une demande, rajoutent des substances dans la composition.</p>
      <p>
        Veuillez vérifier que les doses totales des substances restent pertinentes. Si besoin, renvoyez la déclaration
        vers le déclarant pour les mettre à jour.
      </p>
      <ul>
        <li v-for="i in replacedRequestsWithSubstances" :key="`${i.type}-${i.id}`">
          {{ i.element.name }}
        </li>
      </ul>
    </DsfrAlert>
    <SubstancesTable v-model="payload" readonly />
  </div>
</template>

<script setup>
import { computed } from "vue"
import SubstancesTable from "@/components/SubstancesTable"

const payload = defineModel()

const replacedRequestsWithSubstances = computed(() => {
  const data = payload.value
  if (!data) return false
  const elements = data.declaredPlants
    .concat(data.declaredMicroorganisms)
    .concat(data.declaredSubstances)
    .concat(data.declaredIngredients)
  return elements?.filter((i) => i.requestStatus === "REPLACED" && i.element?.substances?.length)
})
</script>
