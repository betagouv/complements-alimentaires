<template>
  <div class="w-full pointer-events-none fixed bottom-4 z-1751">
    <TransitionGroup mode="out-in" name="list" tag="div" class="flex flex-col items-center space-y-3">
      <DsfrAlert
        v-for="message in messages"
        :key="message.id"
        class="pointer-events-auto mx-3 bg-(--grey-1000-50)"
        v-bind="message"
        @close="close(message.id)"
      />
    </TransitionGroup>
  </div>
</template>

<script setup>
// https://projets-ts-fabnum.netlify.app/client/toaster.html#le-composant-apptoaster
defineProps({ messages: { type: Array, default: () => [] } })
const emit = defineEmits(["close-message"])
const close = (id) => emit("close-message", id)
</script>

<style scoped>
@reference "../../styles/index.css";

.list-move, /* apply transition to moving elements */
.list-enter-active,
.list-leave-active {
  @apply transition-all ease-out duration-500;
}

.list-enter-from,
.list-leave-to {
  @apply opacity-0 translate-y-8;
}

/* ensure leaving items are taken out of layout flow so that moving
   animations can be calculated correctly. */
.list-leave-active {
  @apply fixed;
}
</style>
