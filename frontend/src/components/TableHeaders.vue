<template>
  <tr>
    <!-- Il faut générer programmatiquement les entêtes à cause du bug : https://github.com/dnum-mi/vue-dsfr/issues/1091 -->
    <th
      v-for="header in headers"
      :key="header.text"
      :class="header.active || currentSort === header.sortParam ? 'active' : ''"
    >
      <div class="flex items-baseline">
        <div class="grow">
          <span>{{ header.text }}</span>
          <DsfrTooltip v-if="header.tooltipContent" :content="header.tooltipContent" />
        </div>
        <div class="flex-none">
          <DsfrButton
            v-if="header.sortParam"
            tertiary
            :icon="getSortIcon(header.sortParam)"
            @click="() => sortBy(header.sortParam, header.sortCallback)"
            :aria-label="header.ariaLabel"
            class="p-0 header-icon aspect-square justify-center"
          />
          <DsfrButton
            v-else-if="header.icon"
            :icon="header.icon"
            tertiary
            @click="header.onClick"
            class="p-0 header-icon aspect-square justify-center"
            :aria-label="header.ariaLabel"
          />
        </div>
      </div>
    </th>
  </tr>
</template>

<script setup>
import { ref } from "vue"
import { useRoute } from "vue-router"
const route = useRoute()
defineProps({ headers: Array })

const currentSort = ref(route.query.triage ? route.query.triage.substring(1) : undefined)
const sortDirection = ref(route.query.triage ? route.query.triage.substring(0, 1) : undefined)

const getSortIcon = (sortParam) =>
  currentSort.value === sortParam
    ? sortDirection.value === "+"
      ? "ri-sort-desc"
      : "ri-sort-asc"
    : "ri-arrow-up-down-line"

const sortBy = (sortParam, sortCallback) => {
  if (currentSort.value === sortParam) {
    if (!sortDirection.value) sortDirection.value = "+"
    else if (sortDirection.value === "+") sortDirection.value = "-"
    else sortDirection.value = currentSort.value = "" // Si on a cliqué trois fois on désactive le triage
  } else {
    sortDirection.value = "+"
    currentSort.value = sortParam
  }
  sortCallback(`${sortDirection.value}${currentSort.value}`)
}
</script>

<style scoped>
@reference "../styles/index.css";

th {
  @apply py-2!;
}
th :deep(.vicon) {
  @apply ml-2!;
}

/* Ces styles sont appliqués pour les icônes des entêtes du DsfrTable si le filtre
est actif pour rendre un petit cercle à côté de l'icône. */
.active :deep(.header-icon) {
  position: relative;
  display: inline-block;
}

.active :deep(.header-icon::after) {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  width: 10px;
  height: 10px;
  background-color: #d64d00;
  border-radius: 50%;
  transform: translate(50%, -50%);
}
</style>
