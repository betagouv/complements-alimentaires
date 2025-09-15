<template>
  <tr v-if="props.value" class="sm:flex border-b last:border-0 py-1 gap-4">
    <th scope="row" class="sm:flex-[0_0_30%] font-bold sm:text-right">{{ props.label }}</th>
    <td class="sm:flex-auto">{{ props.value }}</td>
  </tr>
</template>

<script setup>
const props = defineProps({ label: String, value: String })
</script>
