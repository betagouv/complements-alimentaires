<template>
  <div>
    <DsfrAlert class="mb-4" small type="error" v-if="validationError">{{ validationError }}</DsfrAlert>
    <SectionTitle title="Étiquetage" sizeTag="h6" icon="ri-price-tag-2-fill" />
    <DsfrAlert
      v-if="containsAlcohol"
      class="mb-4"
      title="Votre complément alimentaire contient de l'alcool en tant qu'ingrédient"
      type="warning"
    >
      <p>
        Avez-vous bien pensé à porter l'avertissement "déconseillé aux enfants de moins de 12 ans, femmes enceintes et
        allaitantes" sur votre étiquetage ?
      </p>
    </DsfrAlert>
    <DsfrInputGroup>
      <DsfrFileUpload
        label="Veuillez nous transmettre l'étiquetage de votre produit (format PDF ou image)"
        :accept="['image/jpeg, image/gif, image/png, application/pdf']"
        hint="Taille maximale du fichier : 2 Mo"
        @change="addLabelFiles"
        v-model="selectedLabelFile"
        :required="true"
      />
    </DsfrInputGroup>

    <FileGrid :files="labelFiles" @remove="removeFile" hideTypeSelection />

    <SectionTitle title="Autres" class="mt-10!" sizeTag="h6" icon="ri-attachment-2" />

    <RequiresAnalysisReportNotice :declaration="payload" />

    <DsfrInputGroup>
      <DsfrFileUpload
        :label="otherAttachmentsLabel"
        :acceptTypes="acceptedTypes"
        hint="Taille maximale du fichier : 2 Mo"
        @change="addOtherFiles"
        v-model="selectedOtherFile"
        :required="needsEuProof"
      />
    </DsfrInputGroup>

    <FileGrid :files="otherFiles" @remove="removeFile" />
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import FileGrid from "./FileGrid"
import SectionTitle from "@/components/SectionTitle"
import RequiresAnalysisReportNotice from "@/components/RequiresAnalysisReportNotice"

const acceptedTypes = ["image/jpeg", "image/gif", "image/png", "application/pdf"]
const props = defineProps(["externalResults"])
const payload = defineModel()

const { preparations } = storeToRefs(useRootStore())

const needsEuProof = computed(() => {
  return []
    .concat(
      payload.value.declaredPlants,
      payload.value.declaredMicroorganisms,
      payload.value.declaredIngredients,
      payload.value.declaredSubstances
    )
    .filter((x) => x.new)
    .some((x) => x.authorizationMode === "EU")
})

const otherAttachmentsLabel = computed(() => {
  let label = ""
  if (needsEuProof.value)
    label +=
      "Merci de fournir la pièce jointe du texte qui permette de justifier de l’application du principe de reconnaissance mutuelle (obligation art 16.2°.c) du décret 2006-352.\n"
  label += "Vous pouvez nous transmettre tout autre document que vous jugez utile à l'examen de votre dossier."
  return label
})

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
    const formatIsValid = acceptedTypes.indexOf(files[i].type) > -1
    if (!formatIsValid) {
      window.alert(
        `Le format du fichier ${files[i].name} n'est pas supporté. Merci de joindre un fichier en JPG, GIF, PNG ou PDF.`
      )
      continue
    }
    const base64 = await toBase64(files[i])
    if (base64) {
      container.push({
        ...{
          file: base64,
          name: files[i].name,
        },
        ...defaultData,
      })
    } else {
      window.alert("Une erreur est survenue lors du téléversement du fichier. Merci de réessayer.")
    }
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

const containsAlcohol = computed(() => {
  const plantPreparationsUsed = payload.value.declaredPlants.map((plant) => plant.preparation)
  const preparationsInfo = preparations.value.filter((p) => plantPreparationsUsed.includes(p.id))
  return preparationsInfo.some((p) => p.containsAlcohol)
})
</script>
