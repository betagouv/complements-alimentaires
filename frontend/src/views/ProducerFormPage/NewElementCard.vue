<template>
  <div class="p-4 border shadow-md">
    <div class="flex">
      <div class="self-center font-bold capitalize">
        {{ name.toLowerCase() }}
      </div>
    </div>
    <hr class="mt-4 pb-1" />
    <DsfrInputGroup>
      <DsfrRadioButton
        name="authorizationMode"
        hint="Cet ingrédient est autorisé ou utilisable en France"
        v-model="model.authorizationMode"
        value="FR"
      >
        <template v-slot:label>
          <div>
            <img src="/static/images/flags/fr.svg" class="w-5 mr-1 -mt-1 inline rounded-sm" />
            Utilisable en France
          </div>
        </template>
      </DsfrRadioButton>

      <DsfrRadioButton
        name="authorizationMode"
        hint="Cet ingrédient n'est pas autorisée en France mais l'est dans un autre pays de l'UE ou EEE (déclaré au titre de l'article 16 du décret 2006-352)"
        v-model="model.authorizationMode"
        value="EU"
      >
        <template v-slot:label>
          <div>
            <img src="/static/images/flags/eu.svg" class="w-5 mr-1 -mt-1 inline rounded-sm" />
            Autorisé dans un État membre de l'UE ou EEE
          </div>
        </template>
      </DsfrRadioButton>
    </DsfrInputGroup>
    <div v-if="model.authorizationMode === 'FR'">
      <hr class="pb-1 -mt-3" />
      <div class="">
        <DsfrInputGroup>
          <DsfrRadioButtonSet
            v-model="model.frReason"
            name="frReason"
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
        <DsfrInputGroup class="col-span-12 md:col-span-3">
          <DsfrSelect
            label="Pays de référence"
            defaultUnselectedText=""
            v-model="model.euReferenceCountry"
            :options="countries.filter((x) => x.value !== 'FR')"
            :required="true"
          />
        </DsfrInputGroup>
        <div class="col-span-12 md:col-span-9">
          <DsfrInputGroup>
            <DsfrInput
              v-model="model.euLegalSource"
              label-visible
              label="Source réglementaire"
              is-textarea
              :required="true"
              hint="Veuillez préciser la référence exacte du texte réglementaire."
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
import { computed } from "vue"
import { countries } from "@/utils/mappings"
const model = defineModel()
const name = computed(() => model.value.newName || `${model.value.newGenre} ${model.value.newSpecies}`)
const additionReasons = [
  {
    label: "Usage établi",
    value: "TRADITIONAL_USAGE",
    hint: "Ingrédient bénéficiant d'un historique de consommation selon le catalogue Novel Food ou dont l'utilisation en alimentation humaine est bien établie (directive 2004/24/CE)",
  },
  {
    label: "Novel Food",
    value: "NOVEL_FOOD",
    hint: "L'ingrédient figure sur la liste de l'Union des nouveaux aliments conformément au règlement (UE) 2017/2470",
  },
  {
    label: "Ingrédient absent en base de données",
    value: "MISSING",
    hint: "L'ingrédient est autorisé en France mais ne figure pas dans la base de données",
  },
]
</script>
