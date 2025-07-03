<template>
  <tr>
    <!-- Il faut générer programmatiquement les entêtes à cause du bug : https://github.com/dnum-mi/vue-dsfr/issues/1091 -->
    <th v-for="header in headers" :key="header.text" :class="header.active ? 'active' : ''">
      <div class="flex items-baseline">
        <span class="grow">{{ header.text }}</span>
        <div class="flex-none">
          <DsfrButton
            v-if="header.icon"
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
defineProps({ headers: Array })
</script>

<style scoped>
@reference "../styles/index.css";

th {
  @apply py-2!;
}
th .vicon {
  @apply ml-2!;
}

/* Ces styles sont appliqués pour les icônes des entêtes du DsfrTable si le filtre
est actif pour rendre un petit cercle à côté de l'icône. */
.th.active .header-icon {
  position: relative;
  display: inline-block;
}

.th.active .header-icon::after {
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
