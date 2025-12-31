<template>
  <div class="bg-blue-france-950 py-2 flex items-center">
    <div class="fr-container">
      <div class="sm:flex justify-between">
        <div class="flex items-center gap-x-2.5 gap-y-1 flex-wrap">
          <div class="flex items-center gap-x-1">
            <v-icon class="text-blue-france-sun-113" name="ri-account-circle-line" />
            <div class="shrink-0 fr-notice__title text-blue-france-sun-113">Bienvenue, {{ name }}</div>
          </div>
          <div v-if="activeCompany" class="flex gap-x-1.5">
            <RoleTag v-for="role in roles" :key="role" :role="role" />
          </div>
        </div>
        <CompanyTag v-if="activeCompany && companies.length === 1" :name="activeCompany.socialName" />
        <div id="company-select-wrapper" v-else-if="companies.length > 1">
          <DsfrSelect
            :options="companiesSelectOptions"
            :modelValue="activeCompany?.id"
            @update:modelValue="(x) => emit('changeCompany', x)"
            label="Entreprise"
            class="-mt-5"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import RoleTag from "@/components/RoleTag.vue"
import CompanyTag from "@/components/CompanyTag.vue"
import { computed } from "vue"

const emit = defineEmits(["changeCompany"])
const props = defineProps({ name: String, activeCompany: Object, companies: Array })

const companiesSelectOptions = computed(() =>
  props.companies?.filter((c) => !c.representedBy).map((c) => ({ text: c.socialName, value: c.id }))
)

const roles = computed(() => {
  const activeCompanyEntries = props.companies?.filter((c) => c.id === props.activeCompany.id)
  const roles = activeCompanyEntries.flatMap((c) => c.roles).map((r) => r.name)

  return [...new Set(roles)]
})
</script>

<style>
@reference "../../styles/index.css";

#company-select-wrapper .fr-label {
  @apply invisible;
}
</style>
