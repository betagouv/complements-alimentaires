<template>
  <div>
    <DsfrAlert type="error" v-if="shownErrors && shownErrors.length">
      <p class="mb-4">
        Veuillez corriger les erreurs indiquées ci-dessous avant de
        <router-link :to="routeForTab('Soumettre')">soumettre à nouveau</router-link>
        votre dossier.
      </p>

      <DsfrAccordionsGroup v-model="activeAccordion">
        <DsfrAccordion
          v-for="tabSection in shownErrors"
          :key="tabSection.tab"
          :title="`${tabSection.tab} (${tabSection.errors.length} erreur${tabSection.errors.length > 1 ? 's' : ''})`"
          :id="tabSection.tab"
        >
          <router-link :to="routeForTab(tabSection.tab)" v-if="tabSection.tab !== 'Autres'">
            Aller dans l'onglet « {{ tabSection.tab }} »
          </router-link>
          <ul>
            <li v-for="error in tabSection.errors" :key="error">
              {{ error }}
            </li>
          </ul>
        </DsfrAccordion>
      </DsfrAccordionsGroup>
    </DsfrAlert>
  </div>
</template>

<script setup>
import { computed, ref } from "vue"
const props = defineProps({ errors: Object, tabTitles: Array })
const activeAccordion = ref(-1)

const shownErrors = computed(() => {
  const fieldErrors = props.errors?.fieldErrors
  const nonFieldErrors = props.errors?.nonFieldErrors
  if (!fieldErrors && !nonFieldErrors) return []

  // Mapping des erreurs liées à des champs
  const errorObject = Object.keys(tabSections).map((key) => {
    return {
      tab: key,
      errors: fieldErrors.filter
        ? fieldErrors.filter((x) => tabSections[key]?.indexOf(Object.keys(x)[0]) > -1).map((x) => Object.values(x)?.[0])
        : [],
    }
  })

  // Gestion des erreurs non-liées à des champs particuliers
  // ------
  // L'erreur levée lors qu'il n'y a aucun ingrédient n'est pas lié à un champ
  // spécifique. Ici on l'ajout manuellement au tab « Composition »
  const compositionErrors = [
    "Le complément doit comporter au moins un ingrédient",
    "Merci de renseigner les informations manquantes des plantes ajoutées",
    "Merci de renseigner les informations manquantes des micro-organismes ajoutées",
    "Merci de renseigner les informations manquantes dans le tableau des substances",
  ]
  for (let i = 0; i < compositionErrors.length; i++)
    if (nonFieldErrors && nonFieldErrors.indexOf(compositionErrors[i]) > -1)
      errorObject.find((x) => x.tab === "Composition")?.errors?.push(compositionErrors[i])

  // Les autres erreurs non-liées à des champs vont dans l'apparté « Autres »
  if (nonFieldErrors && nonFieldErrors.length)
    errorObject
      .find((x) => x.tab === "Autres")
      ?.errors?.push(...nonFieldErrors.filter((x) => compositionErrors.indexOf(x) === -1))

  // On montre seulement les appartés qui ont au moins une erreur
  return errorObject.filter((x) => x.errors.length > 0)
})

const routeForTab = (tabTitle) => ({ query: { tab: props.tabTitles.map((x) => x.title).indexOf(tabTitle) } })

const tabSections = {
  Produit: [
    "company",
    "name",
    "brand",
    "gamme",
    "flavor",
    "description",
    "galenicFormulation",
    "otherGalenicFormulation",
    "unitQuantity",
    "unitMeasurement",
    "conditioning",
    "dailyRecommendedDose",
    "minimumDuration",
    "instructions",
    "warning",
    "populations",
    "conditionsNotRecommended",
    "effects",
    "otherEffects",
    "address",
    "additionalDetails",
    "postalCode",
    "city",
    "cedex",
    "country",
  ],
  Composition: [],
  "Pièces jointes": ["attachments"],
  "Nouveaux ingrédients": ["euReferenceCountry", "euLegalSource"],
  Autres: [],
}
</script>
