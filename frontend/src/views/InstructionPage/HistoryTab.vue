<template>
  <div>
    <div v-if="isFetching" class="flex justify-center items-center min-h-60">
      <ProgressSpinner />
    </div>
    <div v-if="snapshots">
      <SnapshotItem v-for="snapshot in snapshots" :key="`snapshot-${snapshot.id}`" :snapshot="snapshot" />
    </div>
  </div>
</template>

<script setup>
import { useFetch } from "@vueuse/core"
import { onMounted } from "vue"
import { handleError } from "@/utils/error-handling"
import ProgressSpinner from "@/components/ProgressSpinner"
import SnapshotItem from "@/views/InstructionPage/SnapshotItem"

const props = defineProps(["declarationId"])

const {
  response,
  data: snapshots,
  execute,
  isFetching,
} = useFetch(() => `/api/v1/declarations/${props.declarationId}/snapshots/`, { immediate: false })
  .get()
  .json()

onMounted(async () => {
  await execute()
  handleError(response)
})
</script>
