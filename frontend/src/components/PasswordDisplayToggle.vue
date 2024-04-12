<template>
  <DsfrButton
    @click="toggleShowPassword"
    :label="(showPassword ? 'Cacher' : 'Afficher') + (manyPasswords ? ' les mots de passe' : '')"
    :icon="showPassword ? 'ri-eye-off-line' : 'ri-eye-line'"
    size="sm"
    tertiary
    noOutline
  />
</template>

<script setup>
const props = defineProps({ showPassword: Boolean, manyPasswords: { type: Boolean, default: false } })
const emit = defineEmits(["update:showPassword"])

const toggleShowPassword = () => {
  emit("update:showPassword", !props.showPassword)
}
</script>
