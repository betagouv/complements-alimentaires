<template>
  <div>
    <div v-if="!snapshots" class="flex justify-center items-center min-h-60">
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
import { computed } from "vue"
import ProgressSpinner from "@/components/ProgressSpinner"
import SnapshotItem from "@/components/SnapshotItem"

const props = defineProps(["snapshots", "declarationId", "hideInstructionDetails"])

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
      "REVOKE_AUTHORIZATION",
    ]
    return props.snapshots?.filter((x) => allowedActions.indexOf(x.action) > -1)
  }
  return props.snapshots
})

const showOnRight = (snapshot) => {
  const rightSideStatus = ["OBSERVATION", "AUTHORIZED", "AWAITING_VISA", "OBJECTION", "AUTHORIZATION_REVOKED"]
  return rightSideStatus.indexOf(snapshot.status) > -1
}
</script>
