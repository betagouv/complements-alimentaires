<template>
  <div class="fr-container my-8 flex flex-col">
    <EditPersonalInformationBlock />
    <hr class="mt-8" />
    <ChangePasswordBlock />
    <hr class="mt-8" />
    <DeleteAccountBlock />
  </div>
</template>

<script setup>
import EditPersonalInformationBlock from "./EditPersonalInformationBlock"
import ChangePasswordBlock from "./ChangePasswordBlock"
import DeleteAccountBlock from "./DeleteAccountBlock"
</script>
