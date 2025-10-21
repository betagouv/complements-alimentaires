<template>
  <div class="p-4 border shadow-md">
    <div class="flex">
      <div class="self-center font-bold capitalize">
        {{ getElementName(model).toLowerCase() }}
      </div>
      <div v-if="objectType === 'plant_part'" class="self-center ml-2">
        {{ plantPartName }}
      </div>
      <span v-if="plantPartStatus === 'inconnu'" class="self-center mt-1 ml-2">
        <DsfrBadge label="Nouvelle partie de plante" type="info" />
      </span>
      <span v-else-if="plantPartStatus === 'non autorisé'" class="self-center mt-1 ml-2">
        <DsfrBadge label="Partie de plante non autorisée" type="warning" />
      </span>
    </div>
    <hr class="mt-4 pb-1" />
    <DsfrInputGroup>
      <DsfrRadioButton
        :name="`authorizationMode-${uid}`"
        :hint="textForType.frHint"
        v-model="model.authorizationMode"
        value="FR"
      >
        <template v-slot:label>
          <div>
            <img src="/static/images/flags/fr.svg" class="w-5 mr-1 -mt-1 inline rounded-sm" alt="" />
            {{ getAuthorizationModeInFrench("FR") }}
          </div>
        </template>
      </DsfrRadioButton>

      <DsfrRadioButton
        :name="`authorizationMode-${uid}`"
        :hint="textForType.euHint"
        v-model="model.authorizationMode"
        value="EU"
      >
        <template v-slot:label>
          <div>
            <img src="/static/images/flags/eu.svg" class="w-5 mr-1 -mt-1 inline rounded-sm" alt="" />
            {{ getAuthorizationModeInFrench("EU") }}
          </div>
        </template>
      </DsfrRadioButton>
    </DsfrInputGroup>
    <div v-if="model.authorizationMode === 'FR'">
      <hr class="pb-1 -mt-3" />
      <div>
        <DsfrInputGroup>
          <DsfrRadioButtonSet
            v-model="model.frReason"
            :name="`frReason-${uid}`"
            legend="Raison de l'ajout manuel"
            :options="additionReasons"
          ></DsfrRadioButtonSet>
        </DsfrInputGroup>
        <DsfrInputGroup v-if="model.frReason === 'missing'">
          <DsfrInput
            v-model="model.frDetails"
            label-visible
            label="Information additionnelle"
            is-textarea
            hint="Veuillez saissir des informations susceptibles de permettre à l'administration de traiter votre demande"
          />
        </DsfrInputGroup>
      </div>
    </div>
    <div v-if="model.authorizationMode === 'EU'">
      <hr class="pb-1 -mt-3" />
      <div class="grid grid-cols-12 gap-4">
        <div class="col-span-12 md:col-span-3">
          <DsfrInputGroup>
            <CountryField
              label="Pays de référence"
              :exclude="['FR']"
              defaultUnselectedText=""
              v-model="model.euReferenceCountry"
              :required="true"
            />
          </DsfrInputGroup>
        </div>

        <div class="col-span-12 md:col-span-9">
          <DsfrInputGroup>
            <DsfrInput
              v-model="model.euLegalSource"
              label-visible
              label="Lien de la source réglementaire"
              is-textarea
              :required="true"
              hint="Veuillez préciser l'URL du texte réglementaire."
            />
          </DsfrInputGroup>
          <DsfrInputGroup>
            <DsfrInput
              v-model="model.euDetails"
              label-visible
              label="Information additionnelle"
              is-textarea
              hint="Saisissez ici toutes les informations qui seraient susceptibles de permettre à l'administration de traiter votre demande. Eviter, si possible, toute information directement ou indirectement nominative."
            />
          </DsfrInputGroup>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, watch } from "vue"
import { useRootStore } from "@/stores/root"
import CountryField from "@/components/fields/CountryField"
import { getElementName } from "@/utils/elements"
import { getAuthorizationModeInFrench } from "@/utils/mappings"
import { getCurrentInstance } from "vue"

const model = defineModel()
const { uid } = getCurrentInstance()
const store = useRootStore()

const props = defineProps(["objectType"])

const additionReasons = computed(() => [
  {
    label: "Usage établi",
    value: "TRADITIONAL_USAGE",
    hint: textForType.value.traditionalHint,
  },
  {
    label: "Novel Food",
    value: "NOVEL_FOOD",
    hint: textForType.value.novelHint,
  },
  {
    label: "Ingrédient absent en base de données",
    value: "MISSING",
    hint: textForType.value.missingHint,
  },
])

const textForType = computed(() => {
  if (props.objectType === "plant_part") {
    return {
      frHint: "Cette partie de plante est autorisée ou utilisable en France",
      euHint:
        "Cette partie de plante n'est pas autorisée en France mais l'est dans un autre pays de l'UE ou EEE (déclaré au titre de l'article 16 du décret 2006-352)",
      traditionalHint:
        "Partie de plante bénéficiante d'un historique de consommation selon le catalogue Novel Food ou dont l'utilisation en alimentation humaine est bien établie",
      novelHint:
        "La partie de plante figure sur la liste de l'Union des nouveaux aliments conformément au règlement (UE) 2017/2470",
      missingHint: "La partie de plante est autorisée en France mais ne figure pas dans la base de données",
    }
  }
  return {
    frHint: "Cet ingrédient est autorisé ou utilisable en France",
    euHint:
      "Cet ingrédient n'est pas autorisé en France mais l'est dans un autre pays de l'UE ou EEE (déclaré au titre de l'article 16 du décret 2006-352)",
    traditionalHint:
      "Ingrédient bénéficiant d'un historique de consommation selon le catalogue Novel Food ou dont l'utilisation en alimentation humaine est bien établie",
    novelHint:
      "L'ingrédient figure sur la liste de l'Union des nouveaux aliments conformément au règlement (UE) 2017/2470",
    missingHint: "L'ingrédient est autorisé en France mais ne figure pas dans la base de données",
  }
})

const plantPartName = computed(() => {
  if (!model.value.usedPart || !store.plantParts) return ""
  return store.plantParts.find((p) => p.id === model.value.usedPart)?.name
})

const plantPartStatus = computed(() => {
  if (model.value.usedPart && model.value.element?.plantParts?.length) {
    const associatedPart = model.value.element.plantParts.find((p) => p.id === model.value.usedPart)
    return associatedPart?.status || "inconnu"
  }
  return ""
})

watch(
  () => model.value.authorizationMode,
  () => {
    if (model.value.authorizationMode === "EU" && model.value.euReferenceCountry === "FR")
      model.value.euReferenceCountry = ""
    if (model.value.authorizationMode === "FR") model.value.euReferenceCountry = "FR"
  }
)
</script>
