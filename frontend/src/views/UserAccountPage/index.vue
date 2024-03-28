<template>
  <div class="fr-container my-8 flex flex-col gap-8">
    <EditPersonalInformationBlock />
    <ChangePasswordBlock />
    <DeleteAccountBlock />
  </div>
</template>

<script setup>
import EditPersonalInformationBlock from "./EditPersonalInformationBlock"
import ChangePasswordBlock from "./ChangePasswordBlock"
import DeleteAccountBlock from "./DeleteAccountBlock"
</script>
