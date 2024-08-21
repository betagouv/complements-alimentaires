<template>
  <div>
    <DsfrAlert class="mb-4" small type="error" v-if="validationError">{{ validationError }}</DsfrAlert>
    <SectionTitle title="Étiquetage" sizeTag="h6" icon="ri-price-tag-2-fill" />
    <DsfrInputGroup>
      <DsfrFileUpload
        label="Merci d'ajouter au moins un fichier image ou PDF correspondant à l'étiquetage."
        :accept="['image/jpeg, image/gif, image/png, application/pdf']"
        hint="Taille maximale du fichier : 2 Mo"
        @change="addLabelFiles"
        v-model="selectedLabelFile"
      />
    </DsfrInputGroup>

    <FileGrid :files="labelFiles" @remove="removeFile" hideTypeSelection />

    <SectionTitle title="Autres" class="!mt-10" sizeTag="h6" icon="ri-attachment-2" />

    <DsfrInputGroup>
      <DsfrFileUpload
        label="Autres pièces que vous jugez nécessaires pour l'étude du dossier"
        :acceptTypes="['image/jpeg, image/gif, image/png, application/pdf']"
        hint="Taille maximale du fichier : 2 Mo"
        @change="addOtherFiles"
        v-model="selectedOtherFile"
      />
    </DsfrInputGroup>

    <FileGrid :files="otherFiles" @remove="removeFile" />
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import FileGrid from "./FileGrid"
import SectionTitle from "@/components/SectionTitle"

const props = defineProps(["externalResults"])
const payload = defineModel()

const validationError = computed(() => props.externalResults?.[0]?.attachments)

const selectedLabelFile = ref(null)
const selectedOtherFile = ref(null)

const addLabelFiles = async (files) => addFiles(files, payload.value.attachments, selectedLabelFile, { type: "LABEL" })
const addOtherFiles = async (files) => addFiles(files, payload.value.attachments, selectedOtherFile)
const addFiles = async (files, container, resetModel, defaultData) => {
  const maxSize = 1048576 * 2
  for (let i = 0; i < files.length; i++) {
    // Check size
    const sizeIsValid = parseInt(files[i].size) < maxSize
    if (!sizeIsValid) {
      window.alert(`Le fichier ${files[i].name} dépasse la taille limite de 2 Mo`)
      continue
    }
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

const labelFiles = computed(() => payload.value.attachments.filter((x) => x.type === "LABEL"))
const otherFiles = computed(() => payload.value.attachments.filter((x) => x.type !== "LABEL"))

const toBase64 = (file) => {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.readAsDataURL(file)
    reader.onload = () => resolve(reader.result)
    reader.onerror = reject
  })
}
</script>
