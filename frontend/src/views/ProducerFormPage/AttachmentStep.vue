<template>
  <h3 class="fr-h6">
    <v-icon class="mr-1" name="ri-price-tag-2-fill"></v-icon>
    Étiquetage
  </h3>

  <DsfrInputGroup>
    <DsfrFileUpload
      label="Merci d'ajouter au moins un fichier image ou PDF correspondant à l'étiquetage."
      :accept="['image/jpeg, image/gif, image/png, application/pdf']"
      @change="addLabelFiles"
      v-model="selectedLabelFile"
    />
  </DsfrInputGroup>

  <FileGrid :files="labelFiles" @remove="removeFile" hideTypeSelection />

  <h3 class="fr-h6 !mt-8">
    <v-icon class="mr-1" name="ri-attachment-2" />
    Autres
  </h3>

  <DsfrInputGroup>
    <DsfrFileUpload
      label="Autres pièces que vous jugez nécessaires pour l'étude du dossier"
      :acceptTypes="['image/jpeg, image/gif, image/png, application/pdf']"
      @change="addOtherFiles"
      v-model="selectedOtherFile"
    />
  </DsfrInputGroup>

  <FileGrid :files="otherFiles" @remove="removeFile" />
</template>

<script setup>
import { ref, computed } from "vue"
import FileGrid from "./FileGrid"

const payload = defineModel()
const selectedLabelFile = ref(null)
const selectedOtherFile = ref(null)

const addLabelFiles = async (files) =>
  addFiles(files, payload.value.attachments, selectedLabelFile, { type: "Étiquetage" })
const addOtherFiles = async (files) => addFiles(files, payload.value.attachments, selectedOtherFile)
const addFiles = async (files, container, resetModel, defaultData) => {
  for (let i = 0; i < files.length; i++) {
    const base64 = await toBase64(files[i])
    container.push({
      ...{
        file: base64,
        name: files[i].name,
      },
      ...defaultData,
    })
  }
  resetModel.value = null
}

const removeFile = (file) => {
  const index = payload.value.attachments.indexOf(file)
  payload.value.attachments.splice(index, 1)
}

const labelFiles = computed(() => payload.value.attachments.filter((x) => x.type === "Étiquetage"))
const otherFiles = computed(() => payload.value.attachments.filter((x) => x.type !== "Étiquetage"))

const toBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => resolve(reader.result)
    reader.onerror = reject
  })
}
</script>
