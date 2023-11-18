<template>
  <div class="grid grid-cols-12">
    <div class="col-span-12 md:col-span-7 md:pr-10">
      <h3>S'abonner à l'info-lettre de veille réglementaire</h3>
      <div>Recevez tous les mois une actualisation réglementaire, des nouvelles de la plateforme teleicare....</div>
    </div>
    <div class="col-span-12 md:col-span-5 my-6 md:my-0">
      <div class="flex">
        <DsfrInput v-model="email" :placeholder="placeholder" />
        <DsfrButton label="Valider" @click="onClick" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"

const email = ref("")
const placeholder = "Votre email"

function onClick() {
  console.log("clicked")
}
</script>
