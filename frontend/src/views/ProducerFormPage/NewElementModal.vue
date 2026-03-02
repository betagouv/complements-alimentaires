<template>
  <DsfrButton
    label="Créer un nouvel ingrédient"
    secondary
    size="sm"
    @click="opened = true"
    ref="modalOrigin"
    class="mr-2"
  />
  <DsfrTooltip class="whitespace-pre-wrap" :content="simpleDescription">
    <span class="fr-sr-only">Infobulle création d'un nouvel ingrédient</span>
  </DsfrTooltip>
  <DsfrModal :actions="actions" ref="modal" @close="close" :opened="opened" title="Nouvel ingrédient">
    <DsfrAlert
      type="info"
      title="Avant de créer un nouvel ingrédient"
      :description="model.objectType == 'plant' ? simpleDescription + ' ' + plantDescription : simpleDescription"
      title-tag="h2"
      :small="true"
    />
    <DsfrInputGroup :error-message="firstErrorMsg(v$, 'objectType')">
      <DsfrSelect
        label="Quel type d'ingrédient souhaitez-vous créer ?"
        v-model="model.objectType"
        :options="addableTypes"
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
        <DsfrInput is-textarea v-model="model.newDescription" label-visible label="Description" />
      </DsfrInputGroup>
    </template>
  </DsfrModal>
</template>

<script setup>
import { ref, watch, computed } from "vue"
import { useVuelidate } from "@vuelidate/core"
import { required, helpers } from "@vuelidate/validators"
import { firstErrorMsg } from "@/utils/forms"
import { typesMapping } from "@/utils/mappings"

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
    label: "Ajouter le nouvel ingrédient à la composition",
    onClick: addElement,
  },
]

const addableTypes = computed(() =>
  Object.keys(typesMapping)
    // Note : Sur téléicare on ne peux pas ajouter des substances directement
    // Le type "ingredient" est voué à être déprécié, donc on ne permet pas d'en ajouter
    .filter((key) => !["ingredient", "aroma", "plant_part"].includes(key))
    .map((key) => ({ text: typesMapping[key], value: key }))
)

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
const simpleDescription = "Avant de créer un nouvel ingrédient, vérifiez qu'il n'existe pas déjà sous un autre nom."
const plantDescription =
  "Les plantes doivent être recherchées par leur nom scientifique, sans précision sur la préparation ou la partie utilisée."
</script>

<style>
@reference "../../styles/index.css";

.fr-input-group {
  @apply mt-4;
}
</style>
