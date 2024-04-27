<template>
  <div>
    <SectionTitle title="Demandes en cours" icon="ri-chat-3-line" />
    <h6>Vos demandes reçues</h6>
    <div class="flex items-center">
      <v-icon class="size-4" name="ri-chat-3-line" />

      <div class="ml-2">
        <div>Toto LeGrandPélo</div>
        <div class="text-xs">le 11/02/2024 à 16h34</div>
      </div>

      <div class="ml-2 md:ml-8 flex flex-col gap-y-1">
        <div class="italic">« Je souhaiterais rejoindre cette entreprise en tant que gestionnaire »</div>
        <div class="flex gap-x-2">
          <DsfrButton label="Accepter" size="sm" icon="ri-check-fill" />
          <DsfrButton label="Refuser" secondary size="sm" icon="ri-close-fill" />
        </div>
      </div>

      <hr class="mt-4 -mb-2 border" />
    </div>
  </div>
</template>

<script setup>
import SectionTitle from "@/components/SectionTitle"
</script>
