<template>
  <!-- v-slot:content v-if="!declaration.siccrfId" -->
  <div class="text-left sm:mb-0 sm:flex sm:gap-8">
    <DsfrInputGroup>
      <DsfrInput
        :disabled="disableInstructionNotes"
        v-model="privateNotesInstruction"
        is-textarea
        label-visible
        label="Notes de l'instruction"
        @update:modelValue="saveInstructionComment"
      />
    </DsfrInputGroup>
    <DsfrInputGroup>
      <DsfrInput
        :disabled="disableVisaNotes"
        v-model="privateNotesVisa"
        is-textarea
        label-visible
        label="Notes du visa"
        @update:modelValue="saveVisaComment"
      />
    </DsfrInputGroup>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useFetch, useDebounceFn } from "@vueuse/core"
import { headers } from "@/utils/data-fetching"
import { handleError } from "@/utils/error-handling"

const declaration = defineModel()
defineProps({ disableInstructionNotes: Boolean, disableVisaNotes: Boolean })

const privateNotesInstruction = ref(declaration.value?.privateNotesInstruction || "")
const privateNotesVisa = ref(declaration.value?.privateNotesVisa || "")

const saveInstructionComment = async () => saveComment({ privateNotesInstruction: privateNotesInstruction.value })
const saveVisaComment = async () => saveComment({ privateNotesVisa: privateNotesVisa.value })

const saveComment = useDebounceFn(async (payload) => {
  const url = `/api/v1/declarations/${declaration.value?.id}`
  const { response } = await useFetch(() => url, { headers: headers() })
    .patch(payload)
    .json()
  handleError(response)
}, 600)
</script>
