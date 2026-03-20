<template>
  <DsfrButton @click="duplicate" size="sm" class="fr-btn--tertiary">
    Dupliquer
    <span class="fr-sr-only">{{ declaration.name }}</span>
  </DsfrButton>
</template>

<script setup>
import { useRouter } from "vue-router"

const props = defineProps(["declaration"])
const router = useRouter()

const duplicate = () => {
  router.push({ name: "NewDeclaration", query: { duplicate: props.declaration.id } })
}
</script>
