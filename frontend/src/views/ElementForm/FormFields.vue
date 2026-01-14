<template>
  <FormWrapper :externalResults="$externalResults" class="mx-auto">
    <DsfrFieldset legend="Identité de l’ingrédient" legendClass="fr-h4 mb-0! pb-2!">
      <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-x-8">
        <div class="col-span-2 lg:col-span-4" v-if="formForType.name">
          <DsfrInputGroup :error-message="firstErrorMsg(v$, 'name')">
            <DsfrInput v-model="state.name" :label="formForType.name.label" required labelVisible />
          </DsfrInputGroup>
        </div>
        <div v-if="formForType.species" class="col-span-2">
          <DsfrInputGroup :error-message="firstErrorMsg(v$, 'species')">
            <DsfrInput v-model="state.species" label="Espèce du micro-organisme" labelVisible required />
          </DsfrInputGroup>
        </div>
        <div v-if="formForType.genus" class="col-span-2">
          <DsfrInputGroup :error-message="firstErrorMsg(v$, 'genus')">
            <DsfrInput v-model="state.genus" label="Genre" labelVisible required />
          </DsfrInputGroup>
        </div>
        <div class="col-span-2">
          <DsfrInputGroup>
            <DsfrSelect
              v-model.number="state.status"
              label="Autorisation de l’ingrédient"
              :options="statuses"
              hint="Une déclaration contenant un ingrédient non autorisé passera en article 16"
            />
          </DsfrInputGroup>
        </div>
        <div class="col-span-2" v-if="formForType.family && plantFamiliesDisplay">
          <DsfrInputGroup :error-message="firstErrorMsg(v$, 'family')">
            <DsfrSelect
              v-model.number="state.family"
              label="Famille de la plante"
              :options="plantFamiliesDisplay"
              labelKey="name"
              required
            />
          </DsfrInputGroup>
        </div>
        <div v-if="formForType.ingredientType" class="col-span-2">
          <DsfrInputGroup :error-message="firstErrorMsg(v$, 'ingredientType')">
            <DsfrSelect
              v-model.number="state.ingredientType"
              label="Type de l'ingrédient"
              :options="ingredientTypes"
              required
            />
          </DsfrInputGroup>
        </div>
        <div class="col-span-full mt-4" v-if="formForType.substanceTypes">
          <DsfrInputGroup :error-message="firstErrorMsg(v$, 'substanceTypes')">
            <DsfrCheckboxSet
              v-model="state.substanceTypes"
              :options="substanceTypeOptions"
              legend="Type(s) de la substance"
              required
            />
          </DsfrInputGroup>
        </div>

        <DsfrInputGroup v-if="formForType.einecNumber">
          <DsfrInput v-model="state.einecNumber" label="Numéro EINECS" labelVisible />
        </DsfrInputGroup>
        <DsfrInputGroup v-if="formForType.casNumber">
          <DsfrInput
            v-model="state.casNumber"
            label="Numéro CAS"
            labelVisible
            hint="Le format de n°CAS doit suivre XXXXXXX-XX-X"
          />
        </DsfrInputGroup>
        <DsfrToggleSwitch
          v-if="!state.ingredientType || state.ingredientType != aromaId"
          v-model="state.novelFood"
          label="Novel food"
          activeText="Oui"
          inactiveText="Non"
          label-left
          class="self-center mt-4 col-span-2 sm:col-span-1"
        />
      </div>
      <div class="grid md:grid-cols-2 md:gap-4">
        <div class="mb-4">
          <DsfrInput
            label="Description"
            v-model="state.description"
            :isTextarea="true"
            label-visible
            hint="Donne de l'information sur la source de l'ingrédient, son processus de fabrication, sa forme moléculaire, etc"
          />
        </div>
      </div>
      <DsfrFieldset legend="Synonymes" legendClass="fr-text--lg pb-0! mb-2! mt-4!">
        <div class="grid md:grid-cols-4" v-for="(q, idx) in state.synonyms" :key="`synoym-row-${idx}`">
          <DsfrInput class="col-span-2" v-model="q.name" />
          <DsfrSelect class="!ml-2" v-model="q.synonymType" :options="synonymTypes" />
        </div>
        <DsfrButton
          label="Ajouter un synonyme"
          @click="addNewSynonym"
          icon="ri-add-line"
          size="sm"
          class="mt-2"
          secondary
        />
      </DsfrFieldset>
      <div class="grid md:grid-cols-2 mt-4">
        <DsfrFieldset
          legend="Ressources reglementaires"
          hint="Les URLs doivent commencer par « https:// » ou « http:// »"
          legendClass="fr-text--lg pb-0! mb-2! mt-4!"
        >
          <DsfrInputGroup :errorMessage="regulatoryResourceLinksError" wrapperClass="mt-0 mb-0">
            <DsfrInput
              v-for="(_, idx) in state.regulatoryResourceLinks"
              :key="`link-${idx}`"
              v-model="state.regulatoryResourceLinks[idx]"
              class="mb-4"
            />
          </DsfrInputGroup>
          <DsfrButton
            label="Ajouter un lien"
            @click="
              () =>
                state.regulatoryResourceLinks
                  ? state.regulatoryResourceLinks.push('')
                  : (state.regulatoryResourceLinks = [''])
            "
            icon="ri-add-line"
            size="sm"
            :class="regulatoryResourceLinksError ? 'mt-6' : 'mt-2'"
            secondary
          />
        </DsfrFieldset>
      </div>
    </DsfrFieldset>

    <div class="my-8 sm:mt-0">
      <DsfrTable
        v-if="formForType.plantParts"
        title="Parties de plante"
        :headers="plantPartHeaders"
        class="mb-2! input-table"
      >
        <tr v-for="(q, idx) in state.plantParts" :key="`max-quantity-row-${idx}`">
          <td><DsfrSelect v-model="q.plantpart" :options="orderedPlantParts" /></td>
          <td><DsfrSelect v-model.number="q.status" :options="plantPartStatuses" /></td>
          <td><DsfrInput v-model.number="q.originDeclaration" /></td>
          <td>
            <DsfrButton
              label="Supprimer"
              @click="deletePlantPart(idx)"
              :icon="{ name: 'ri-delete-bin-line' }"
              icon-only
              tertiary
            />
          </td>
        </tr>
      </DsfrTable>
      <p v-else>Aucune partie de plante n'est spécifiée.</p>
      <p v-if="plantPartsError" class="text-red-marianne-425">{{ plantPartsError }}</p>
      <DsfrButton
        label="Ajouter une partie de plante"
        @click="addNewPlantPart"
        icon="ri-add-line"
        size="sm"
        class="mt-2"
        secondary
      />
    </div>
    <DsfrFieldset legend="Utilisation de l’ingrédient" legendClass="fr-h4 mb-0! pb-2!">
      <div v-if="formForType.substances" class="grid md:grid-cols-3 items-end my-4 md:my-2">
        <ElementAutocomplete
          autocomplete="nothing"
          label="Substances actives"
          label-visible
          class="max-w-md grow mb-3"
          hint="Tapez au moins trois caractères pour démarrer la recherche"
          :hideSearchButton="true"
          @selected="selectOption"
          type="substance"
          :searchAll="true"
          :required="false"
        />
        <div class="md:ml-4 md:my-7 md:col-span-2">
          <DsfrTag
            v-for="(substance, idx) in state.substances"
            :key="`substance-${substance.id}`"
            :label="substance.name"
            tagName="button"
            @click="state.substances.splice(idx, 1)"
            :aria-label="`Retirer ${substance.name}`"
            class="mx-1 fr-tag--dismiss"
          ></DsfrTag>
        </div>
      </div>
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 mb-6">
        <DsfrInputGroup>
          <DsfrToggleSwitch
            v-model="state.mustSpecifyQuantity"
            label="Spécification de quantité obligatoire ?"
            hint="La déclaration devra indiquer la quantité de cet ingrédient"
            activeText="Oui"
            inactiveText="Non"
            label-left
            class="self-center mt-4 col-span-2 sm:col-span-2"
          />
        </DsfrInputGroup>
      </div>
      <div class="max-w-32">
        <DsfrInputGroup v-if="isNewIngredient || !state.unit" :error-message="firstErrorMsg(v$, 'unit')">
          <DsfrSelect
            label="Unité"
            label-visible
            :options="store.units?.map((unit) => ({ text: unit.name, value: unit.id }))"
            v-model="state.unit"
            defaultUnselectedText="Unité"
            required
          />
        </DsfrInputGroup>
        <div v-else class="pt-4">
          <p class="mb-2">Unité</p>
          <p class="mb-0">{{ unitString }}</p>
        </div>
      </div>
      <div
        class="grid sm:grid-cols-3 gap-x-8"
        v-if="formForType.nutritionalReference && [1, 2].some((substType) => state.substanceTypes.includes(substType))"
      >
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'nutritionalReference')">
          <NumberField label="Apport nutritionnel de référence" label-visible v-model="state.nutritionalReference" />
        </DsfrInputGroup>
      </div>
      <div class="mt-8 sm:mt-0">
        <DsfrTable
          v-if="state.maxQuantities.length"
          title="Quantités maximales par population"
          :headers="maxQuantitiesHeaders"
          class="mb-2! input-table"
        >
          <tr v-for="(q, idx) in state.maxQuantities" :key="`max-quantity-row-${idx}`">
            <td><DsfrSelect v-model="q.population" :options="populationOptions" /></td>
            <td><DsfrInput v-model.number="q.maxQuantity" /></td>
            <td>
              <DsfrButton
                label="Supprimer"
                @click="deleteMaxQuantity(idx)"
                :icon="{ name: 'ri-delete-bin-line' }"
                icon-only
                tertiary
              />
            </td>
          </tr>
        </DsfrTable>
        <p v-else>Aucune quantité maximale n'est spécifiée.</p>
        <p v-if="maxQuantitiesError" class="text-red-marianne-425">{{ maxQuantitiesError }}</p>
        <DsfrButton
          label="Ajouter une dose max pour une population"
          @click="addNewMaxQuantity"
          icon="ri-add-line"
          size="sm"
          class="mt-2"
          secondary
        />
      </div>
    </DsfrFieldset>
    <DsfrFieldset
      legend="Avertissement"
      hint="Mentions d'avertissement devant figurer sur l'étiquette"
      legendClass="fr-h4 mb-0!"
      class="mb-0"
    >
      <div v-for="(q, idx) in state.warningsOnLabel" :key="`warning-${idx}`" class="grid md:grid-cols-8 md:gap-4 mb-4">
        <span class="col-span-7">
          <DsfrInput v-model="state.warningsOnLabel[idx]" />
        </span>
        <span>
          <DsfrButton
            label="Supprimer"
            @click="deleteWarning(idx)"
            :icon="{ name: 'ri-delete-bin-line' }"
            icon-only
            tertiary
            class="mt-2"
          />
        </span>
      </div>
      <DsfrButton
        label="Ajouter un avertissement"
        @click="() => (state.warningsOnLabel ? state.warningsOnLabel.push('') : (state.warningsOnLabel = ['']))"
        icon="ri-add-line"
        size="sm"
        class="mt-2"
        secondary
      />
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 mb-6">
        <DsfrToggleSwitch
          v-model="state.isRisky"
          label="Nécessite une instruction manuelle et vigilante ?"
          activeText="Oui"
          inactiveText="Non"
          label-left
          class="self-center mt-4 col-span-2 sm:col-span-2"
          hint="Une déclaration contenant cet ingrédient passera en article 15 vigilance"
        />
        <DsfrToggleSwitch
          v-model="state.requiresAnalysisReport"
          label="Nécessite un bulletin d'analyse ?"
          activeText="Oui"
          inactiveText="Non"
          label-left
          class="self-center mt-4 col-span-2 sm:col-span-2"
          hint="Lors d'une déclaration contenant cet ingrédient, un message incitera au dépot d'un bulletin d'analyse comme pièce-jointe"
        />
      </div>
    </DsfrFieldset>

    <DsfrFieldset legend="Commentaires" legendClass="fr-h4 mb-0!" class="mb-0">
      <div class="grid md:grid-cols-2 md:gap-4">
        <div class="mb-4">
          <DsfrInput
            label="Commentaire public"
            v-model="state.publicComments"
            :isTextarea="true"
            label-visible
            hint="Les indications de quantités max par population et d'avertissements spécifiques sont à renseigner plus haut"
          />
        </div>
        <div class="mb-4">
          <DsfrInput
            label="Commentaire privé"
            v-model="state.privateComments"
            :isTextarea="true"
            label-visible
            hint="Les liens vers des sources règlementaires sont à renseigner plus haut"
          />
        </div>
      </div>
      <div v-if="!isNewIngredient" class="grid md:grid-cols-2 md:gap-4">
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'publicChangeReason')">
          <DsfrInput
            v-model="state.publicChangeReason"
            label="Raison de changement (public)"
            hint="100 caractères max, sera affiché dans l'historique des ingrédients, dans le moteur de recherche"
            labelVisible
          />
        </DsfrInputGroup>
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'changeReason')">
          <DsfrInput
            v-model="state.changeReason"
            label="Raison de changement (privé)"
            hint="100 caractères max"
            labelVisible
          />
        </DsfrInputGroup>
      </div>
    </DsfrFieldset>
    <div class="grid sm:grid-cols-2 lg:grid-cols-3 mb-6">
      <div>
        <DsfrInputGroup :error-message="originDeclarationError">
          <DsfrInput
            v-model.number="state.originDeclaration"
            label="Première déclaration"
            hint="Si cet ingrédient a été créé suite à une demande, renseignez l'identifiant de la déclaration pour laisser cette déclaration en article 16"
            labelVisible
          />
        </DsfrInputGroup>
        <p v-if="state.originDeclaration" class="mt-4">
          <router-link
            :to="{ name: 'InstructionPage', params: { declarationId: state.originDeclaration } }"
            target="_blank"
          >
            Déclaration ayant demandé l'ajout de cet ingrédient
          </router-link>
        </p>
      </div>
    </div>
    <div class="grid sm:grid-cols-2 lg:grid-cols-3 mb-6">
      <DsfrToggleSwitch
        v-model="state.toBeEnteredInNextDecree"
        label="À rentrer dans le prochain décret&nbsp;?"
        activeText="Oui"
        inactiveText="Non"
        label-left
        class="self-center mt-4 col-span-2 sm:col-span-1"
      />
    </div>
    <DsfrAlert v-if="substanceAttachReminder" class="mb-8">
      <p>
        Vous avez indiquez que cette substance est apportée par un ou plusieurs ingrédients. N'oubliez pas la rattacher
        en modifiant l'ingrédient après avoir créé cette substance.
      </p>
    </DsfrAlert>
    <DsfrAlert v-if="element" class="mb-8">
      <p>Des modifications pourrait impacter les déclarations en cours qui utilisent cet ingrédient.</p>
      <p>
        <router-link
          :to="{
            name: 'AdvancedSearchPage',
            query: {
              composition: `${element.id}||${element.name}||${type}`,
              status: 'AWAITING_INSTRUCTION,ONGOING_INSTRUCTION,AWAITING_VISA,ONGOING_VISA,OBJECTION,OBSERVATION',
            },
          }"
          target="_blank"
        >
          Voir les déclarations en cours
        </router-link>
      </p>
    </DsfrAlert>
    <div class="flex flex-wrap gap-2 mt-4">
      <DsfrButton label="Enregistrer ingrédient" @click="saveElement" />
      <DsfrButton
        v-if="!isNewIngredient"
        tertiary
        size="small"
        icon="ri-delete-bin-line"
        label="Supprimer l'ingrédient"
        @click="deleteModalOpened = true"
      />
      <DsfrModal
        v-if="!isNewIngredient"
        :opened="deleteModalOpened"
        @close="deleteModalOpened = false"
        :title="`Supprimer ${element.name}`"
        :actions="deleteActions"
      >
        <template #default>
          <p>Voulez-vous supprimer l'ingrédient {{ element.name }} ?</p>
          <p>
            Cette action va marquer l'ingrédient comme obsolète et l'ingrédient sera toujours lié aux déclarations
            historiques.
          </p>
        </template>
      </DsfrModal>
    </div>
  </FormWrapper>
</template>

<script setup>
import { ref, computed, watch } from "vue"
import { getApiType, ingredientStatuses } from "@/utils/mappings"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import { useRouter } from "vue-router"
import { useFetch } from "@vueuse/core"
import { headers } from "@/utils/data-fetching"
import { handleError } from "@/utils/error-handling"
import { firstErrorMsg, errorRequiredField, errorNumeric, errorMaxStringLength } from "@/utils/forms"
import { getUnitString } from "@/utils/elements"
import { useVuelidate } from "@vuelidate/core"
import useToaster from "@/composables/use-toaster"
import FormWrapper from "@/components/FormWrapper"
import ElementAutocomplete from "@/components/ElementAutocomplete"
import NumberField from "@/components/NumberField"

const props = defineProps({ element: Object, type: String, urlComponent: String })

const isNewIngredient = computed(() => !props.element?.id)

const elementId = computed(() => props.element?.id)
const apiType = computed(() => props.type && getApiType(props.type))
const router = useRouter()

const createEmptySynonym = () => ({ name: "", synonymType: "" })
const createEmptyPlantPart = () => ({ plantpart: "", status: "", originDeclaration: "" })

const state = ref({
  substances: [],
  synonyms: [createEmptySynonym()],
  plantParts: [createEmptyPlantPart()],
  maxQuantities: [],
  toBeEnteredInNextDecree: true, // vrai pour les nouveaux ingrédients
  substanceTypes: [],
})

watch(
  () => props.element,
  () => {
    state.value = JSON.parse(JSON.stringify(props.element))
    state.value.status = statuses.find((s) => s.apiValue === state.value.status)?.value
    if (state.value.family) state.value.family = state.value.family.id
    if (state.value.plantParts) {
      state.value.plantParts.forEach((p) => {
        p.plantpart = p.id
        p.status = statuses.find((s) => s.apiValue === p.status)?.value
      })
    }
    if (state.value.objectType && apiType.value === "other-ingredient")
      state.value.ingredientType = ingredientTypes.find((t) => t.apiValue === state.value.objectType).value
    if (state.value.unitId) state.value.unit = state.value.unitId
    if (state.value.maxQuantities?.length)
      state.value.maxQuantities.forEach((q) => (q.population = q.population.id.toString()))
  }
)

const saveElement = async () => {
  v$.value.$reset()
  v$.value.$validate()
  validateMaxQuantities()
  if (v$.value.$error || maxQuantitiesError.value) {
    useToaster().addErrorMessage(
      "Merci de vérifier que les champs obligatoires, signalés par une astérix *, ont bien été remplis"
    )
    window.scrollTo(0, 0)
    return
  }

  const url = `/api/v1/${apiType.value}s/`
  const payload = JSON.parse(JSON.stringify(state.value))
  if (payload.substances?.length) {
    payload.substances = payload.substances.map((substance) => substance.id)
  }
  payload.synonyms = payload.synonyms.filter((s) => !!s.name)
  payload.regulatoryResourceLinks = payload.regulatoryResourceLinks?.filter((l) => !!l)
  if (payload.ingredientType && payload.ingredientType == aromaId) delete payload.novelFood
  if (formForType.value.plantParts) {
    payload.plantParts = state.value.plantParts.filter((p) => p.plantpart && p.status)
  }

  const { response } = isNewIngredient.value
    ? await useFetch(url, { headers: headers() }).post(payload).json()
    : await useFetch(url + elementId.value, { headers: headers() })
        .patch(payload)
        .json()
  $externalResults.value = await handleError(response)

  if (response.value.ok) {
    useToaster().addMessage({
      type: "success",
      id: "element-creation-success",
      description: `L'ingrédient a été ${isNewIngredient.value ? "créé" : "modifié"}`,
    })
    if (isNewIngredient.value) router.push({ name: "NewElementsPage" })
    else router.push({ name: "ElementPage", params: { urlComponent: props.urlComponent } })
  } else {
    const fieldErrors = $externalResults.value.fieldErrors
    if (fieldErrors && Object.keys(fieldErrors).length > 0) {
      if ($externalResults.value?.fieldErrors?.maxQuantities) {
        maxQuantitiesError.value = $externalResults.value.fieldErrors.maxQuantities[0]
      }
      if ($externalResults.value?.fieldErrors?.plantParts) {
        plantPartsError.value = $externalResults.value.fieldErrors.plantParts
          .filter((p) => !!p.originDeclaration)
          .map((p) => p.originDeclaration)
          .join(" ")
      }
      if ($externalResults.value?.fieldErrors?.regulatoryResourceLinks) {
        regulatoryResourceLinksError.value = "Merci de vérifier que tous les liens commencent par http:// ou https://"
      }
      if ($externalResults.value?.fieldErrors?.originDeclaration) {
        originDeclarationError.value =
          "Merci de vérifier que l'identifiant renseigné corresponde à une déclaration existante"
      }
      useToaster().addErrorMessage(
        "Merci de vérifier que les champs obligatoires, signalés par une astérix *, ont bien été remplis"
      )
      window.scrollTo(0, 0)
    }
  }
}
const addNewSynonym = async () => {
  state.value.synonyms.push(createEmptySynonym())
}

const addNewPlantPart = () => {
  state.value.plantParts.push(createEmptyPlantPart())
}

const formQuestions = {
  plant: {
    name: {
      label: "Nom de la plante",
    },
    family: true,
    function: true,
    // status: true for every type
    // novelFood is true for every type
    // synonymes are true for every type
    plantParts: true,
    substances: true,
    // population cible: true for everyone also not yet in our database
    // public notes true for every type
  },
  substance: {
    name: {
      label: "Nom de la substance",
    },
    einecNumber: true,
    casNumber: true,
    nutritionalReference: true,
    substanceTypes: true,
  },
  microorganism: {
    species: true,
    genus: true,
    function: true,
    substances: true,
  },
  ingredient: {
    name: {
      label: "Nom ingrédient",
    },
    ingredientType: true,
    function: true,
    substances: true,
  },
}
const formForType = computed(() => {
  return formQuestions[props.type] || (!isNewIngredient.value && formQuestions.ingredient)
})
const rules = computed(() => {
  const form = formForType.value
  return {
    name: form?.name ? errorRequiredField : {},
    species: form?.species ? errorRequiredField : {},
    genus: form?.genus ? errorRequiredField : {},
    ingredientType: form?.ingredientType ? errorRequiredField : {},
    substanceTypes: form?.substanceTypes ? errorRequiredField : {},
    family: form?.family ? errorRequiredField : {},
    unit: !props.element ? errorRequiredField : {},
    nutritionalReference: form?.nutritionalReference ? errorNumeric : {},
    changeReason: isNewIngredient.value ? {} : errorMaxStringLength(100),
    publicChangeReason: isNewIngredient.value ? {} : errorMaxStringLength(100),
  }
})
watch(formForType, () => v$.value.$reset())

const $externalResults = ref({})
const v$ = useVuelidate(rules, state, { $externalResults })

const store = useRootStore()
const { plantParts, plantFamilies, units, populations } = storeToRefs(store)
store.fetchDeclarationFieldsData()
store.fetchPlantFamilies()

const orderedPlantParts = computed(() => {
  const ordered = JSON.parse(JSON.stringify(plantParts.value)) || []
  ordered?.sort((a, b) => a.name.localeCompare(b.name))
  return ordered.map((o) => ({ value: o.id, text: o.name }))
})
const synonymTypes = [
  { value: "SCIENTIFIC_NAME", text: "Nom scientifique" },
  { value: "FRENCH_NAME", text: "Nom en français" },
  { value: "ENGLISH_NAME", text: "Nom en anglais" },
]

const ingredientTypes = [
  { value: 1, text: "Nutriment (Forme d'apport)", apiValue: "form_of_supply" },
  { value: 2, text: "Additif", apiValue: "additive" },
  { value: 3, text: "Arôme", apiValue: "aroma" },
  { value: 4, text: "Autre ingrédient actif", apiValue: "active_ingredient" },
  { value: 5, text: "Autre ingrédient", apiValue: "non_active_ingredient" },
]

const statuses = [
  { ...ingredientStatuses.AUTHORIZED, text: "✅ Autorisé" },
  { ...ingredientStatuses.NOT_AUTHORIZED, text: "🛑 Non autorisé" },
  { ...ingredientStatuses.NO_STATUS, text: "Sans objet" },
]

const plantPartStatuses = statuses.filter((s) => s.value !== 3)

const selectOption = async (result) => {
  state.value.substances.push(result)
}

const plantFamiliesDisplay = computed(() => {
  return plantFamilies.value
    ?.map((family) => ({ value: family.id, text: family.name }))
    .sort((a, b) => a.text.localeCompare(b.text))
})

const aromaId = 3

const unitString = computed(() => {
  return getUnitString(parseInt(state.value.unit, 10), units)
})

const populationOptions = computed(() => {
  return populations.value?.map((pop) => ({ text: pop.name, value: pop.id.toString() }))
})
const addNewMaxQuantity = () => {
  state.value.maxQuantities.push({})
}
const deleteMaxQuantity = (idx) => {
  state.value.maxQuantities.splice(idx, 1)
}
const deleteWarning = (idx) => {
  state.value.warningsOnLabel.splice(idx, 1)
}
const deletePlantPart = (idx) => {
  state.value.plantParts.splice(idx, 1)
}
const maxQuantitiesError = ref()
const validateMaxQuantities = () => {
  const hasMissingData = state.value.maxQuantities?.some(
    (q) => !q.population || (!q.maxQuantity && q.maxQuantity !== 0)
  )
  maxQuantitiesError.value = hasMissingData && "Veuillez compléter tous les champs ou supprimer les lignes vides"
}
const plantPartsError = ref()
const maxQuantitiesHeaders = computed(() => {
  return ["Population", `Quantité max (en ${unitString.value})`, ""]
})
const plantPartHeaders = computed(() => {
  return ["Partie", "Statut", "Première déclaration", ""]
})

const regulatoryResourceLinksError = ref()
const originDeclarationError = ref()

const substanceTypeOptions = computed(() => [
  {
    label: "Substance active à but nutritionnel ou physiologique",
    hint: "Cette substance peut être ajoutée directement comme ingrédient d'une déclaration",
    value: 4,
  },
  {
    label: "Vitamine",
    hint: "Cette substance est apportée par une forme d'apport",
    value: 1,
  },
  {
    label: "Minéral",
    hint: "Cette substance est apportée par une forme d'apport",
    value: 2,
  },
  {
    label: "Métabolite secondaire de plante" + (isNewIngredient.value ? "" : " (automatiquement assigné)"),
    hint: "Cette substance est apportée par une plante",
    value: 3,
    disabled: !isNewIngredient.value,
  },
])

const substanceAttachReminder = computed(() => {
  return isNewIngredient.value && state.value.substanceTypes?.some((st) => [1, 2, 3].includes(st))
})

const deleteModalOpened = ref(false)

const deleteActions = [
  {
    label: "Supprimer l'ingrédient",
    onClick: async () => {
      const url = `/api/v1/${apiType.value}s/`
      const { response } = await useFetch(url + elementId.value, { headers: headers() })
        .patch({ isObsolete: true })
        .json()
      $externalResults.value = await handleError(response)

      if (response.value.ok) {
        useToaster().addMessage({
          type: "success",
          id: "element-deletion-success",
          description: "L'ingrédient a été supprimé",
        })
        router.push({ name: "ElementPage", params: { urlComponent: props.urlComponent } })
      }
    },
  },
  {
    label: "Garder l'ingredient",
    onClick: () => {
      deleteModalOpened.value = false
    },
    secondary: true,
  },
]
</script>

<style scoped>
.input-table :deep(caption.caption) {
  /* la taille du fr-h5 */
  font-size: 1.375rem;
}
</style>
