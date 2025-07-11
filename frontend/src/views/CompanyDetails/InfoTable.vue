<template>
  <table>
    <tr v-for="item in items" :key="item.body" class="m-2 p-2">
      <th>{{ item.title }}</th>
      <th>
        <div v-for="(line, index) in item.body" :key="`infotable${line}${index}`">{{ line }}</div>
      </th>
    </tr>
  </table>
</template>

<script setup>
defineProps({ items: Array })
</script>

<style scoped>
@reference "../../styles/index.css";

th {
  @apply border-collapse;
  @apply py-1;
  @apply px-2;
  @apply border;
  @apply border-white;
  @apply text-left;
  @apply font-normal;
}

th:first-child {
  @apply bg-[#f6f6f6];
  @apply font-bold;
}
</style>
