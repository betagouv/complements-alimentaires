<template>
  <div>
    <DsfrInputGroup>
      <div class="grid grid-cols-2 gap-6">
        <DsfrRadioButton
          v-for="category in decisionCategories"
          :key="category.value"
          v-model="decisionCategory"
          :value="category.value"
          name="decisionCategory"
          class="col-span-2 sm:col-span-1 !mb-0"
        >
          <template v-slot:label>
            <div class="font-bold">
              <v-icon :color="category.color" :name="category.icon" aria-hidden />
              {{ category.title }}
            </div>
            <p class="fr-text--sm !mb-0">
              {{ category.description }}
            </p>
          </template>
        </DsfrRadioButton>
      </div>
    </DsfrInputGroup>
  </div>
  <div v-if="decisionCategory === 'modify'" class="reject-reasons">
    <hr />
    <div class="mb-8" v-for="reason in rejectReasons" :key="reason.title">
      <p class="font-bold">{{ reason.title }}</p>
      <DsfrInputGroup v-for="item in reason.items" :key="item">
        <DsfrCheckbox :label="item" />
      </DsfrInputGroup>
    </div>
  </div>
  <div v-if="decisionCategory">
    <hr />
    <h3>Décision</h3>
    <DsfrHighlight>
      <template v-slot:default>
        <div class="sm:flex gap-4">
          <div class="grow max-w-96">
            <DsfrInputGroup>
              <DsfrSelect label="Proposition" v-model="proposal" :options="proposalOptions"></DsfrSelect>
            </DsfrInputGroup>
          </div>
          <div class="visa-checkbox content-end">
            <DsfrInputGroup>
              <DsfrCheckbox label="À viser" />
            </DsfrInputGroup>
          </div>
          <div class="content-end" v-if="decisionCategory != 'approve'">
            <DsfrInputGroup>
              <DsfrInput v-model="delayDays" label="Délai de réponse (jours)" label-visible />
            </DsfrInputGroup>
          </div>
        </div>
        <DsfrInputGroup>
          <DsfrInput
            is-textarea
            label-visible
            label="Motivation de la décision (à destination du professionel)"
            v-if="decisionCategory != 'approve'"
          />
        </DsfrInputGroup>
      </template>
    </DsfrHighlight>
    <hr />
    <DsfrInputGroup>
      <DsfrInput is-textarea label-visible label="Notes de l'expert (à destination de l'administration)" />
    </DsfrInputGroup>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue"

const decisionCategory = ref(null)
watch(decisionCategory, () => (proposal.value = decisionCategory.value === "approve" ? "approve" : null))

const proposal = ref(null)
const delayDays = ref(30)

const decisionCategories = [
  {
    value: "approve",
    title: "Bon pour autorisation",
    icon: "ri-checkbox-circle-fill",
    description: "La déclaration ne pose pas de problème et peut être autorisé en l'état.",
    color: "green",
  },
  {
    value: "modify",
    title: "Des changements sont nécessaires",
    icon: "ri-close-circle-fill",
    description: "La déclaration nécessite des ajustements et ne peut pas être autorisée.",
    color: "red",
  },
]

const rejectReasons = [
  {
    title: "Le produit ne répond pas à la définition du complément alimentaire",
    items: [
      "Forme assimilable à un aliment courant",
      "Recommendations d'emploi incompatibles",
      "Composition (source concentrée, ...)",
      "Autre",
    ],
  },
  {
    title: "Le produit répond à la définition du médicament",
    items: ["Par fonction", "Par présentation", "Sevrage tabagique"],
  },
  {
    title: "Les procédures ne sont pas respectées",
    items: [
      "Présence d'un Novel Food",
      "Présence d'une forme d'apport en nutriments non autorisée",
      "Demande en article 18 attendue",
    ],
  },
  {
    title: "Le dossier n'est pas recevable",
    items: ["Incohérences entre le dossier et l'étiquetage", "Informations manquantes", "Autre"],
  },
  {
    title: "Le complément alimentaire n'est pas acceptable",
    items: [
      "Absence de preuve de reconnaissance mutuelle",
      "Existence d'un risque",
      "Absence d'étiquetage",
      "Absence de preuve",
      "Incohérence entre le dossier et l'étiquetage",
      "Autres données manquantes",
    ],
  },
]

const proposalOptions = computed(() => {
  if (decisionCategory.value === "approve") return [{ text: "Autorisation", value: "autorisation" }]

  return [
    { text: "Objection", value: "objection" },
    { text: "Observation", value: "observation" },
    { text: "Refus", value: "rejection" },
  ]
})
</script>

<style scoped>
.reject-reasons:deep(.fr-input-group) {
  @apply !mb-0;
}
.visa-checkbox:deep(.fr-fieldset__element) {
  @apply !mb-1;
}
</style>
