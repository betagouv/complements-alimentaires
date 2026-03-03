<template>
  <div>
    <h2 class="uppercase text-sm mb-0">{{ title }}</h2>
    <div class="mt-3 grid grid-col-3 border-gray-100">
      <div class="divide-y divide-gray-100">
        <dl
          v-for="(line, index) in dataLines"
          :key="line.title"
          class="grid grid-cols-3 py-5 whitespace-pre-line items-center pl-0"
          :class="index % 2 === 0 ? 'bg-blue-france-975' : ''"
        >
          <dt class="font-medium pl-2 sm:pl-4">{{ line.title }}</dt>
          <dd class="text-gray-700">{{ line.val }}</dd>
        </dl>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({ title: String, dataLines: Object })
</script>
