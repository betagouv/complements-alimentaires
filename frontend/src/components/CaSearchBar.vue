<template>
  <div class="flex items-end">
    <div class="grow">
      <DsfrInput
        v-model="model"
        @update:modelValue="(val) => val === '' && $emit('search')"
        @keydown.enter="$emit('search')"
        v-bind="$attrs"
      />
    </div>

    <DsfrButton
      :title="$attrs.label"
      class="max-h-10 mt-2 rounded-r"
      @click="$emit('search')"
      :iconOnly="true"
      icon="ri-search-line"
    >
      <span class="fr-sr-only">{{ $attrs.label }}</span>
    </DsfrButton>
  </div>
</template>

<script setup>
const model = defineModel()
defineEmits(["search"])
</script>
