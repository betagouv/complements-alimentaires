<template>
  <div v-if="user">
    <p>{{ user.firstName }} {{ user.lastName }}</p>
    <p>
      Adresse email :
      <a :href="`mailto:${user.email}`" target="_blank">{{ user.email }}</a>
    </p>
  </div>
  <p v-else>
    Cette déclaration n'a pas de déclarant ou déclarante assignée. Le compte a probablement été supprimé depuis.
  </p>
</template>
<script setup>
defineProps({ user: Object })
</script>

<style scoped>
@reference "../styles/index.css";
p {
  @apply mb-2!;
}
</style>
