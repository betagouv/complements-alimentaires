<template>
  <DsfrButton
    @click="toggleShowPassword"
    :icon="showPassword ? 'ri-eye-off-line' : 'ri-eye-line'"
    size="sm"
    tertiary
    noOutline
  >
    {{ showPassword ? "Cacher" : "Afficher" }}
    <span v-if="manyPasswords">les mots de passe</span>
    <span v-else class="fr-sr-only">le mot de passe</span>
  </DsfrButton>
</template>

<script setup>
const props = defineProps({ showPassword: Boolean, manyPasswords: { type: Boolean, default: false } })
const emit = defineEmits(["update:showPassword"])

const toggleShowPassword = () => {
  emit("update:showPassword", !props.showPassword)
}
</script>
