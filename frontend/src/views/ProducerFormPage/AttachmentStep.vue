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

  <div class="grid grid-cols-12 gap-3">
    <FilePreview
      class="col-span-12 sm:col-span-6 md:col-span-4"
      :file="file"
      v-for="file in payload.files.labels"
      :key="file.file"
      @remove="removeLabelFile"
      hideTypeSelection
    />
  </div>

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

  <div class="grid grid-cols-12 gap-3">
    <FilePreview
      class="col-span-12 sm:col-span-6 md:col-span-4"
      :file="file"
      v-for="file in payload.files.others"
      :key="file.file"
      @remove="removeOtherFile"
    />
  </div>
</template>

<script setup>
import { ref } from "vue"
import FilePreview from "./FilePreview"

const payload = defineModel()
const selectedLabelFile = ref(null)
const selectedOtherFile = ref(null)

const addLabelFiles = async (files) =>
  addFiles(files, payload.value.files.labels, selectedLabelFile, { type: "Étiquetage" })
const addOtherFiles = async (files) => addFiles(files, payload.value.files.others, selectedOtherFile)

const removeLabelFile = (file) => removeFile(file, payload.value.files.labels)
const removeOtherFile = (file) => removeFile(file, payload.value.files.others)

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

const removeFile = (file, container) => {
  const index = container.indexOf(file)
  container.splice(index, 1)
}

const toBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => resolve(reader.result)
    reader.onerror = reject
  })
}
</script>
