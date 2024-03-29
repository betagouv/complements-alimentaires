<template>
  <div class="fr-container my-8 flex flex-col">
    <EditPersonalInformationBlock />
    <hr class="mt-12 mb-2" />
    <ChangePasswordBlock />
    <hr class="mt-12 mb-2" />
    <DeleteAccountBlock />
  </div>
</template>

<script setup>
import EditPersonalInformationBlock from "./EditPersonalInformationBlock"
import ChangePasswordBlock from "./ChangePasswordBlock"
import DeleteAccountBlock from "./DeleteAccountBlock"
</script>
