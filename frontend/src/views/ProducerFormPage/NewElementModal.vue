<template>
  <DsfrButton label="Créer un nouvel ingrédient" secondary size="sm" @click="opened = true" ref="modalOrigin" />
  <DsfrModal :actions="actions" ref="modal" @close="close" :opened="opened" title="Nouvel ingrédient">
    <DsfrInputGroup :error-message="firstErrorMsg(v$, 'objectType')">
      <DsfrSelect
        label="Quel type d'ingrédient souhaitez-vous créer ?"
        v-model="model.objectType"
        :options="types"
        :required="true"
      />
    </DsfrInputGroup>

    <template v-if="model.objectType">
      <div v-if="model.objectType === 'plant'">
        <!-- Note: Sur téléicare on a aussi « Nom vernaculaire ». à voir si on veut l'intégrer -->
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'newName')">
          <DsfrInput label="Nom" v-model="model.newName" label-visible :required="true" />
        </DsfrInputGroup>
      </div>

      <div v-else-if="model.objectType === 'microorganism'">
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'newGenre')">
          <DsfrInput label="Genre" v-model="model.newGenre" label-visible :required="true" />
        </DsfrInputGroup>
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'newSpecies')">
          <DsfrInput label="Espèce" v-model="model.newSpecies" label-visible :required="true" />
        </DsfrInputGroup>
      </div>

      <div v-else>
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'newName')">
          <DsfrInput label="Libellé" v-model="model.newName" label-visible :required="true" />
        </DsfrInputGroup>
      </div>

      <DsfrInputGroup>
        <DsfrInput is-textarea v-model="model.newDescription" label-visible label="newDescription" />
      </DsfrInputGroup>
    </template>
  </DsfrModal>
</template>

<script setup>
import { ref, watch, computed } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { required, helpers } from "@vuelidate/validators"
import { firstErrorMsg } from "@/utils/forms"

const opened = ref(false)
const model = ref({})
const emit = defineEmits(["add"])

const addElement = () => {
  v$.value.$validate()
  if (v$.value.$error) return
  const objectType = model.value.objectType
  delete model.value.objectType
  emit("add", model.value, objectType, true)
  close()
}

const actions = [
  {
    label: "Ajouter",
    onClick: addElement,
  },
]

// Note : Sur téléicare on ne peux pas ajouter des substances directement
const types = [
  { value: "plant", text: "Plante" },
  { value: "microorganism", text: "Micro-organisme" },
  { value: "ingredient", text: "Ingredient" },
  // TODO : these items will be added once we have their equivalent in the DB
  // { value: "nutrient", text: "Nutriment" },
  // { value: "additive", text: "Additif" },
  // { value: "aroma", text: "Arôme" },
]

watch(
  () => model.value.objectType,
  () => {
    const keysToClear = Object.keys(model.value).filter((key) => key !== "objectType")
    keysToClear.forEach((key) => delete model.value[key])
    v$.value.$reset()
  }
)

const close = () => {
  model.value = {}
  opened.value = false
}

// Form validation

const rules = computed(() => {
  const formRules = {
    objectType: { required: helpers.withMessage("Veuillez remplir le type d'ingrédient", required) },
  }
  if (model.value.objectType === "microorganism") {
    formRules.newGenre = {
      required: helpers.withMessage("Veuillez renseigner le genre du micro-organisme à ajouter", required),
    }
    formRules.newSpecies = {
      required: helpers.withMessage("Veuillez renseigner l'espèce du micro-organisme à ajouter", required),
    }
  } else {
    formRules.newName = { required: helpers.withMessage("Veuillez renseigner le nom de l'ingrédient", required) }
  }
  return formRules
})

const v$ = useVuelidate(rules, model)
</script>

<style>
.fr-input-group {
  @apply mt-4;
}
</style>
