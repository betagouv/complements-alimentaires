<template>
  <div class="toaster-container">
    <TransitionGroup mode="out-in" name="list" tag="div" class="toasters">
      <div v-for="message in messages" :key="message.id">
        <DsfrAlert class="app-alert !w-auto" v-bind="message" @close="close(message.id)" />
      </div>
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
.toaster-container {
  pointer-events: none;
  position: fixed;
  bottom: 1rem;
  width: 100%;
  z-index: 1750; /* To be on top of .fr-modal which has z-index: 1750 */
}
.toasters {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.app-alert {
  background-color: var(--grey-1000-50);
  width: 90%;
  pointer-events: all;
}

.list-move, /* apply transition to moving elements */
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

/* ensure leaving items are taken out of layout flow so that moving
   animations can be calculated correctly. */
.list-leave-active {
  position: fixed;
}
</style>
