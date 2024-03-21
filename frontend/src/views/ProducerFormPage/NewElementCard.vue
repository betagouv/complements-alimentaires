<template>
  <div class="p-4 border shadow-md">
    <div class="flex">
      <div :class="`mr-4 self-center justify-center rounded-full icon icon-${model.element.objectType} size-8 flex`">
        <v-icon class="self-center" fill="white" :name="getTypeIcon(model.element.objectType)" />
      </div>
      <div class="self-center font-bold capitalize">
        {{ model.element.name.toLowerCase() }}
        <span class="uppercase text-gray-400 text-sm ml-2">{{ getType(model.element.objectType) }}</span>
      </div>
    </div>
    <hr class="mt-4 pb-1" />
    <DsfrInputGroup>
      <DsfrRadioButton
        name="authorisationMode"
        hint="Cet ingrédient est autorisé ou utilisable en France"
        v-model="model.element.authorisationMode"
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
        name="authorisationMode"
        hint="Cet ingrédient n'est pas autorisée en France mais l'est dans un autre pays de l'UE (déclaré au titre de l'article 16 du décret 2006-352)"
        v-model="model.element.authorisationMode"
        value="EU"
      >
        <template v-slot:label>
          <div>
            <img src="/static/images/flags/eu.svg" class="w-5 mr-1 -mt-1 inline rounded-sm" />
            Autorisé dans un État membre de l'UE
          </div>
        </template>
      </DsfrRadioButton>
    </DsfrInputGroup>
    <div v-if="model.element.authorisationMode === 'FR'">
      <hr class="pb-1 -mt-3" />
      <div class="">
        <DsfrInputGroup>
          <DsfrRadioButtonSet
            v-model="model.element.frReason"
            name="frReason"
            legend="Raison de l'ajout manuel"
            :options="additionReasons"
          ></DsfrRadioButtonSet>
        </DsfrInputGroup>
        <DsfrInputGroup v-if="model.element.frReason === 'missing'">
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
    <div v-if="model.element.authorisationMode === 'EU'">
      <hr class="pb-1 -mt-3" />
      <div class="grid grid-cols-12 gap-4">
        <DsfrInputGroup class="col-span-12 md:col-span-3">
          <DsfrSelect
            label="Pays de référence"
            defaultUnselectedText=""
            v-model="model.referenceCountry"
            :options="countries"
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
              hint="Veuillez préciser la référence exacte du texte réglementaire."
            />
          </DsfrInputGroup>
          <DsfrInputGroup>
            <DsfrInput
              v-model="model.euApplicableRestrictions"
              label-visible
              label="Restrictions applicables"
              is-textarea
              :required="true"
              hint="Saisissez ici toutes les informations relatives aux restrictions et qui seraient susceptibles de permettre à l'administration de traiter votre demande. Eviter, si possible, toute information directement ou indirectement nominative."
            />
          </DsfrInputGroup>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { getTypeIcon, getType } from "@/utils/mappings"
const model = defineModel()
const countries = [
  { text: "Allemagne", value: "DE" },
  { text: "Autriche", value: "AT" },
  { text: "Belgique", value: "BE" },
  { text: "Bulgarie", value: "BG" },
  { text: "Chypre", value: "CY" },
  { text: "Croatie", value: "HR" },
  { text: "Danemark", value: "DK" },
  { text: "Espagne", value: "ES" },
  { text: "Estonie", value: "EE" },
  { text: "Finlande", value: "FI" },
  { text: "Grèce", value: "GR" },
  { text: "Hongrie", value: "HU" },
  { text: "Irlande", value: "IE" },
  { text: "Irlande du Nord", value: "IEN" },
  { text: "Islande", value: "IS" },
  { text: "Italie", value: "IT" },
  { text: "Lettonie", value: "LV" },
  { text: "Liechtenstein", value: "LI" },
  { text: "Lituanie", value: "LT" },
  { text: "Luxembourg", value: "LU" },
  { text: "Malte", value: "MT" },
  { text: "Norvège", value: "NO" },
  { text: "Pays-Bas", value: "NL" },
  { text: "Pologne", value: "PL" },
  { text: "Portugal", value: "PT" },
  { text: "République Tchèque", value: "CZ" },
  { text: "Roumanie", value: "RO" },
  { text: "Slovaquie", value: "SK" },
  { text: "Slovénie", value: "SI" },
  { text: "Suède", value: "SE" },
]
const additionReasons = [
  {
    label: "Usage traditionnel",
    value: "traditional-usage",
    hint: "Demande d’autorisation simplifiée pour un ingŕedient à usage traditionnel (directive 2004/24/CE)",
  },
  {
    label: "Novel Food",
    value: "novel-food",
    hint: "L'ingrédient fait partie de la liste novel food",
  },
  {
    label: "Ingrédient absent en base de données",
    value: "missing",
    hint: "L'ingrédient est autorisé en France mais ne figure pas dans la base de données",
  },
]
</script>
