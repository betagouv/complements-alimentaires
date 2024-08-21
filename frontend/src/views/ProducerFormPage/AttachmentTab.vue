<template>
  <div>
    <SectionTitle title="Étiquetage" sizeTag="h6" icon="ri-price-tag-2-fill" />
    <DsfrInputGroup>
      <DsfrFileUpload
        label="Veuillez nous transmettre l'étiquetage de votre produit (format PDF ou image)"
        :accept="['image/jpeg, image/gif, image/png, application/pdf']"
        @change="addLabelFiles"
        v-model="selectedLabelFile"
        :required="true"
      />
    </DsfrInputGroup>

    <FileGrid :files="labelFiles" @remove="removeFile" hideTypeSelection />

    <SectionTitle title="Autres" class="!mt-10" sizeTag="h6" icon="ri-attachment-2" />

    <DsfrInputGroup>
      <DsfrFileUpload
        label="Vous pouvez nous transmettre tout autre document que vous jugez utile à l'examen de votre dossier"
        :acceptTypes="['image/jpeg, image/gif, image/png, application/pdf']"
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

const payload = defineModel()
const selectedLabelFile = ref(null)
const selectedOtherFile = ref(null)

const addLabelFiles = async (files) => addFiles(files, payload.value.attachments, selectedLabelFile, { type: "LABEL" })
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
