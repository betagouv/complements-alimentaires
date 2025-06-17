<template>
  <div>
    <DsfrAlert
      class="mb-4"
      v-if="!assignedToLoggedUser && (isOngoingInstruction || isAwaitingInstruction)"
      type="info"
      :title="
        declaration.instructor
          ? `Cette déclaration est assignée à ${declaration.instructor.firstName} ${declaration.instructor.lastName}`
          : 'Cette déclaration n\'est pas encore assignée'
      "
    >
      <p>Vous pouvez vous assigner cette déclaration pour instruction</p>
      <DsfrButton
        class="mt-2"
        :label="declaration.instructor ? 'M\'assigner cette déclaration' : 'Instruire'"
        tertiary
        @click="isAwaitingInstruction ? emit('instruct') : emit('assign')"
      />
    </DsfrAlert>
    <DeclarationFromTeleicareAlert v-else-if="declaration.siccrfId" />
    <DeclarationAlert
      class="mb-6"
      v-else-if="!isOngoingInstruction"
      role="instructor"
      :declaration="declaration"
      :snapshots="snapshots"
    />
  </div>
</template>

<script setup>
import { computed } from "vue"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"
import DeclarationAlert from "@/components/DeclarationAlert"
import DeclarationFromTeleicareAlert from "@/components/History/DeclarationFromTeleicareAlert"

const declaration = defineModel()
defineProps(["snapshots"])

// « instruct » est utilisé pour passer la déclaration à ONGOING_INSTRUCTION
// « assign » c'est pour s'assigner une déclaration assignée à une autre instructrice
const emit = defineEmits(["instruct", "assign"])

const store = useRootStore()
const { loggedUser } = storeToRefs(store)

const assignedToLoggedUser = computed(() => declaration.value?.instructor?.id === loggedUser.value.id)
const isOngoingInstruction = computed(() => declaration.value?.status === "ONGOING_INSTRUCTION")
const isAwaitingInstruction = computed(() => declaration.value?.status === "AWAITING_INSTRUCTION")
</script>
