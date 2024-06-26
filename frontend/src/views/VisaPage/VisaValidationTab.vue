<template>
  <div>
    <div class="mb-4">
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
      Nope
    </div>
    <div v-if="decisionCategory">
      <hr />
      <h3>Décision</h3>
      <DsfrHighlight>
        <template v-slot:default>OK va bene</template>
      </DsfrHighlight>
      <hr />
      <DsfrInputGroup>
        <DsfrInput is-textarea label-visible label="Notes de l'expert (à destination de l'administration)" />
      </DsfrInputGroup>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue"
import { useFetch } from "@vueuse/core"
import { headers } from "@/utils/data-fetching"
import useToaster from "@/composables/use-toaster"
import { handleError } from "@/utils/error-handling"

const $externalResults = ref({})
const props = defineProps({ declaration: Object })

const emit = defineEmits(["reload-declaration"])

const decisionCategory = ref(null)
watch(decisionCategory, () => (proposal.value = decisionCategory.value === "approve" ? "approve" : null))

const proposal = ref(null)
const delayDays = ref(30)
const comment = ref("")

const needsVisa = ref(false)
const mandatoryVisaProposals = ["objection", "rejection"]
watch(proposal, (newProposal) => {
  if (mandatoryVisaProposals.indexOf(newProposal) > -1) needsVisa.value = true
})

const decisionCategories = computed(() => {
  return [
    {
      value: "approve",
      title: "Je valide la décision",
      icon: "ri-checkbox-circle-fill",
      description: `La déclaration assignée à ${props.declaration.instructor} peut passer en état ${props.declaration.postValidationStatus}`,
      color: "green",
    },
    {
      value: "modify",
      title: "Je ne suis pas d'accord avec la décision",
      icon: "ri-close-circle-fill",
      description: `La décision de ${props.declaration.instructor} n'est pas validée`,
      color: "red",
    },
  ]
})
</script>
