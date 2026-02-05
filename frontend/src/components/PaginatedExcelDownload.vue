<template>
  <DsfrModal title="Exporter votre recherche" :opened="exportModalOpened" @close="exportModalOpened = false">
    <p>
      Votre recherche dépasse le seuil des {{ maxLines }} lignes. Vous pouvez télécharger la totalité de votre recherche
      en fichiers séparés.
    </p>
    <ul>
      <li v-for="(link, index) in paginatedExcelLinks" :key="`download-links-${index}`">
        <a :href="link.url" download="true" class="fr-link fr-link--download">
          Télécharger
          {{ link.label }}
          <span class="fr-link__detail">XLSX</span>
        </a>
      </li>
    </ul>
  </DsfrModal>
</template>

<script setup>
import { computed } from "vue"

const exportModalOpened = defineModel()

const props = defineProps({ baseUrl: String, maxLines: Number, totalLines: Number })

const paginatedExcelLinks = computed(() => {
  if (!props.totalLines) return []

  const links = []
  const numFiles = Math.ceil(props.totalLines / props.maxLines)

  for (let i = 0; i < numFiles; i++) {
    const offset = i * props.maxLines
    const limit = props.maxLines
    const pageNumber = i + 1
    const startRange = offset + 1
    const endRange = Math.min(offset + props.maxLines, props.totalLines)

    // Create the URL with pagination parameters
    const url = `${props.baseUrl}&limit=${limit}&offset=${offset}`

    links.push({
      url: url,
      label: `lignes ${startRange} à ${endRange} (${pageNumber}/${numFiles})`,
    })
  }

  return links
})
</script>
