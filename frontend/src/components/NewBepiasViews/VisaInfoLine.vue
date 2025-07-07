<template>
  <div class="sm:flex border-b last:border-0 py-3 gap-4">
    <div class="sm:flex-[0_0_25%] font-bold">
      <v-icon class="mr-2" :name="icon" aria-hidden />
      <span>{{ title }}</span>
    </div>
    <div class="comment sm:flex-auto">
      <slot name="value">
        <p class="mb-0 line-through" v-if="strikethroughText">
          <del>{{ strikethroughText }}</del>
        </p>
        <p class="mb-0">{{ text }}</p>
      </slot>
    </div>
  </div>
</template>

<script setup>
defineProps(["icon", "title", "text", "strikethroughText"])
</script>
<style scoped>
@reference "../../styles/index.css";
.comment {
  white-space: pre-line;
}
.comment :deep(.fr-input-group) {
  @apply mt-0!;
}
del::before,
del::after {
  clip-path: inset(100%);
  clip: rect(1px, 1px, 1px, 1px);
  height: 1px;
  overflow: hidden;
  position: absolute;
  white-space: nowrap;
  width: 1px;
}

del::before {
  content: " [début de la suppression] ";
}

del::after {
  content: " [fin de la suppression] ";
}
</style>
