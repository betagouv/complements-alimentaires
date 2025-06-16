<template>
  <div>
    <DsfrAlert
      class="mb-4"
      v-if="!assignedToLoggedUser"
      type="info"
      :title="
        isAwaitingInstruction
          ? 'Cette déclaration n\'est pas encore assignée'
          : `Cette déclaration est assignée à ${declaration.instructor.firstName} ${declaration.instructor.lastName}`
      "
    >
      <p>Vous pouvez vous assigner cette déclaration pour instruction</p>
      <DsfrButton
        class="mt-2"
        :label="isAwaitingInstruction ? 'Instruire' : 'M\'assigner cette déclaration'"
        tertiary
        @click="isAwaitingInstruction ? emit('instruct') : emit('assign')"
      />
    </DsfrAlert>
    <DeclarationAlert
      class="mb-6"
      v-else-if="!canInstruct"
      role="instructor"
      :declaration="declaration"
      :snapshots="snapshots"
    />
    <DeclarationFromTeleicareAlert v-else-if="declaration.siccrfId" />
  </div>
</template>

<script setup>
import { computed } from "vue"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import DeclarationAlert from "@/components/DeclarationAlert"
import DeclarationFromTeleicareAlert from "@/components/History/DeclarationFromTeleicareAlert"

const declaration = defineModel()

// « instruct » est utilisé pour passer la déclaration à ONGOING_INSTRUCTION
// « assign » c'est pour s'assigner une déclaration assignée à une autre instructrice
const emit = defineEmits(["instruct", "assign"])

const store = useRootStore()
const { loggedUser } = storeToRefs(store)

const assignedToLoggedUser = computed(() => declaration.value?.instructor?.id === loggedUser.value.id)
const canInstruct = computed(() => declaration.value?.status === "ONGOING_INSTRUCTION")
const isAwaitingInstruction = computed(() => declaration.value?.status === "AWAITING_INSTRUCTION")
</script>
