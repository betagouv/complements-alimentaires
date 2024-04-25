<template>
  <div class="bg-blue-france-950 h-14 flex items-center">
    <div class="fr-container">
      <div class="flex justify-between">
        <div class="flex items-center gap-x-2.5 gap-y-1 flex-wrap">
          <div class="flex items-center gap-x-1">
            <v-icon class="text-blue-france-sun-113" name="ri-account-circle-line" />
            <div class="shrink-0 fr-notice__title text-blue-france-sun-113">Bienvenue, {{ name }}</div>
          </div>
          <div class="flex gap-x-1.5">
            <RoleTag v-for="role in company.roles" :key="role.name" :role="role" />
          </div>
        </div>
        <CompanyTag :name="company.socialName" />
      </div>
    </div>
  </div>
</template>

<script setup>
import RoleTag from "@/components/RoleTag.vue"
import CompanyTag from "@/components/CompanyTag.vue"

defineProps({ name: String, company: Object })
</script>
