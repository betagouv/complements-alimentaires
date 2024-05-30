<template>
  <div>
    <div class="font-bold uppercase text-sm">{{ title }}</div>
    <div class="mt-3 grid grid-col-3 border-gray-100">
      <div class="divide-y divide-gray-100">
        <div
          v-for="(line, index) in dataLines"
          :key="line.title"
          class="grid grid-cols-3 py-5 whitespace-pre-line items-center"
          :class="index % 2 === 0 ? 'bg-blue-france-975' : ''"
        >
          <dt class="font-medium pl-2 sm:pl-4">{{ line.title }}</dt>
          <dd class="text-gray-700">{{ line.val }}</dd>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ title: String, dataLines: Object })
</script>
