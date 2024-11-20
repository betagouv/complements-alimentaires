<template>
  <div>
    <div v-if="isFetching" class="flex justify-center items-center min-h-60">
      <ProgressSpinner />
    </div>
    <div v-if="snapshots && snapshots.length" class="flex flex-col gap-6">
      <SnapshotItem
        v-for="snapshot in snapshots"
        :key="`snapshot-${snapshot.id}`"
        :snapshot="snapshot"
        :rightSide="showOnRight(snapshot)"
        :hideInstructionDetails="hideInstructionDetails"
      />
    </div>
    <div v-else>
      <p>Nous n'avons pas l'historique pour cette déclaration.</p>
    </div>
  </div>
</template>

<script setup>
import { useFetch } from "@vueuse/core"
import { onMounted, computed } from "vue"
import { handleError } from "@/utils/error-handling"
import ProgressSpinner from "@/components/ProgressSpinner"
import SnapshotItem from "@/components/SnapshotItem"

const props = defineProps(["declarationId", "hideInstructionDetails"])

const { response, data, execute, isFetching } = useFetch(
  () => `/api/v1/declarations/${props.declarationId}/snapshots/`,
  { immediate: false }
)
  .get()
  .json()

const snapshots = computed(() => {
  if (props.hideInstructionDetails) {
    const allowedActions = [
      "SUBMIT",
      "OBSERVE_NO_VISA",
      "AUTHORIZE_NO_VISA",
      "RESPOND_TO_OBSERVATION",
      "RESPOND_TO_OBJECTION",
      "APPROVE_VISA",
      "WITHDRAW",
      "ABANDON",
    ]
    return data.value?.filter((x) => allowedActions.indexOf(x.action) > -1)
  }
  return data.value
})

onMounted(async () => {
  await execute()
  handleError(response)
})

const showOnRight = (snapshot) => {
  const rightSideStatus = ["OBSERVATION", "AUTHORIZED", "AWAITING_VISA"]
  return rightSideStatus.indexOf(snapshot.status) > -1
}
</script>
