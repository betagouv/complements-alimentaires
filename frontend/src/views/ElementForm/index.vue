<template>
  <div class="fr-container mb-8">
    <DsfrBreadcrumb class="mb-8" :links="breadcrumbLinks" />

    <h1>Modification élément</h1>

    <p>
      <v-icon :name="icon" />
      {{ typeName }}
    </p>

    <!-- TODO: tabs -->
    <FormWrapper class="mx-auto">
      <DsfrFieldset legend="Identité de l’ingrédient"></DsfrFieldset>
      <DsfrFieldset legend="Utilisation de l’ingrédient"></DsfrFieldset>
      <DsfrFieldset legend="Commentaire à destination du public"></DsfrFieldset>
      <div class="flex gap-x-2 mt-4">
        <!-- Question: cancel button? -->
        <DsfrButton label="Enregistrer ingrédient" @click="saveElement" :disabled="isFetching" />
        <DsfrButton label="Sauvegarder brouillon" @click="saveAsDraft" :disabled="isFetching" secondary />
      </div>
    </FormWrapper>
  </div>
</template>

<script setup>
import { /*ref, */ computed /*, watch*/ } from "vue"
import { getTypeIcon, getTypeInFrench, unSlugifyType /*, getApiType*/ } from "@/utils/mappings"
import FormWrapper from "@/components/FormWrapper"
// import { useRoute, useRouter } from "vue-router"
// import { useFetch } from "@vueuse/core"
// import { handleError } from "@/utils/error-handling"

const props = defineProps({ urlComponent: String })
const elementId = computed(() => props.urlComponent.split("--")[0])
const type = computed(() => unSlugifyType(props.urlComponent.split("--")[1]))
const icon = computed(() => getTypeIcon(type.value))
const typeName = computed(() => getTypeInFrench(type.value))

const breadcrumbLinks = computed(() => {
  const links = [{ to: { name: "DashboardPage" }, text: "Tableau de bord" }]
  links.push({ text: `Modification élément ${elementId.value}` })
  return links
})

const isFetching = false // TODO: set to true when fetching data or sending update, see CompanyForm

const saveElement = async () => {}
const saveAsDraft = async () => {}
</script>
