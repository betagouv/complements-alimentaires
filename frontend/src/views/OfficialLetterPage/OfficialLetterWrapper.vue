<template>
  <div>
    <div class="filigrane"></div>
    <div class="text-sm text-black">
      <!-- en-tête MASA + DGAL -->
      <div class="flex items-center justify-between">
        <img :src="require('@/assets/masa.png')" class="w-48" />
        <div class="text-lg font-bold leading-6 text-right">
          Direction générale
          <br />
          de l'alimentation
        </div>
      </div>

      <!-- en-tête BEPIAS + date -->
      <div class="mt-10 flex items-center justify-between">
        <div class="max-w-80">
          <div class="font-bold uppercase text-xs leading-4">
            <div>Direction générale de l'alimentation</div>
            <div>251 rue de Vaugirard</div>
            <div>75732 PARIS CEDEX 15</div>
          </div>
          <div class="text-xs">
            <div>BEPIAS (Bureau des Etablissements et Produits des Industries Alimentaires Spécialisées)</div>
            <div>
              Mél :
              <a :href="`mailto:${bepiasEmail}`">{{ bepiasEmail }}</a>
            </div>
          </div>
        </div>
        <div>Paris, le {{ isoToPrettyDate(letterDate, dateOptions) }}</div>
      </div>

      <!-- en-tête destinataire -->
      <div v-if="recipientName" class="flex justify-end">
        <div class="text-left">
          <div>{{ recipientName }}</div>
          <div class="whitespace-pre">{{ recipientAddress }}</div>
        </div>
      </div>

      <!-- Title principal -->
      <div class="mt-10 uppercase text-lg font-bold tracking-tighter">
        <div class="w-2/3 mx-auto text-center">{{ letterTitle }}</div>
      </div>

      <!-- Contenu (slot) -->
      <div class="mt-10">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup>
import { isoToPrettyDate } from "@/utils/date"

const bepiasEmail = "bepias.sdssa.dgal@agriculture.gouv.fr"

const dateOptions = {
  month: "short",
  day: "numeric",
  year: "numeric",
}

defineProps({
  letterDate: { type: Date, required: true },
  letterTitle: { type: String, required: false },
  recipientName: { type: String, required: false },
  recipientAddress: { type: String, required: false },
})
</script>

<style scoped>
a {
  @apply letter-a;
}

.filigrane {
  @apply bg-no-repeat bg-right absolute w-full h-full opacity-[2%];
  background-image: url("@/assets/marianne.svg");
  background-size: 50%;
}
</style>
