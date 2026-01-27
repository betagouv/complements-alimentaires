<template>
  <div class="flex justify-between items-center border p-2">
    <DsfrModal
      :actions="[{ label: 'Valider', onClick: changeArticle }]"
      @close="articleModalOpened = false"
      :opened="articleModalOpened"
      title="Changer l'article"
      v-if="allowChange"
    >
      <p>Vous pouvez changer l'article de cette déclaration en le sélectionnant ci-dessous.</p>
      <DsfrInputGroup>
        <DsfrRadioButtonSet v-model="newArticle" name="Article" legend="" :options="options"></DsfrRadioButtonSet>
      </DsfrInputGroup>
    </DsfrModal>

    <DsfrBadge type="warning" label="Article inconnu" v-if="!payload.article" />
    <DsfrBadge no-icon v-else :label="articleOptionsWith15Subtypes.find((x) => x.value === payload.article)?.text" />
    <DsfrButton
      size="sm"
      tertiary
      :label="!!payload.article ? 'Changer l\'article' : 'Renseigner l\'article'"
      @click="articleModalOpened = true"
      v-if="allowChange"
    />
  </div>
</template>

<script setup>
import { useFetch } from "@vueuse/core"
import { headers } from "@/utils/data-fetching"
import { ref, onMounted } from "vue"
import { articleOptions, articleOptionsWith15Subtypes } from "@/utils/mappings"
import useToaster from "@/composables/use-toaster"
const articleModalOpened = ref(false)

const newArticle = ref()
onMounted(() => (newArticle.value = payload.value.article))

const payload = defineModel()

const props = defineProps({ hideArticle15Subtypes: Boolean, allowChange: Boolean })

// Aujourd'hui les subtypes (WARNING, et HIGH_RISK_POPULATION) doivent être cachés aux déclarants,
// Mais le DeclarationSummary de la page déclarants n'affiche pas le composant ArticleInfoRow aujourd'hui
// TODO: lorsqu'il l'affichera il faudra désactiver la possibilité de modifier l'article
const options = props.hideArticle15Subtypes
  ? articleOptions.map((x) => ({ value: x.value, label: x.text }))
  : articleOptionsWith15Subtypes.map((x) => ({ value: x.value, label: x.text }))

const changeArticle = async () => {
  if (newArticle.value === payload.value.article) {
    articleModalOpened.value = false
    return
  }
  const url = `/api/v1/declarations/${payload.value.id}/update-article/`
  const body = { article: newArticle.value }
  const { response, data } = await useFetch(url, { headers: headers() }).post(body).json()
  if (response.value.status >= 300 || response.value.status < 200) {
    useToaster().addErrorMessage("Une erreur s'est produite, merci de ressayer plus tard")
    return
  }
  payload.value = data.value
  useToaster().addMessage({
    type: "success",
    id: "article-update-success",
    description: "L'article de cette déclaration à été mis à jour",
  })
  articleModalOpened.value = false
}
</script>
