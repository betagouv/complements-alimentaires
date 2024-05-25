<template>
  <div>
    <RoleBarBlock :name="loggedUser.firstName" :company="company" />
    <div class="fr-container my-8">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import RoleBarBlock from "@/components/RoleBarBlock"
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"

const store = useRootStore()
const { loggedUser, company } = storeToRefs(store)
</script>
