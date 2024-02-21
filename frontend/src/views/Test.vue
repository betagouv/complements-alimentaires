<template>
  <div class="p-10 space-x-10">
    <button @click="toto1">Toast 1</button>
    <button @click="toto2">Toast 2</button>
  </div>
</template>

<script setup>
import useToaster from "@/composables/use-toaster"

const toaster = useToaster()
const toto1 = () => {
  toaster.addMessage({
    title: "C'est nuuul",
    description: "Rien ne marche",
    type: "error",
  })
}
const toto2 = () => {
  toaster.addMessage({
    title: "Encore un titre au pif",
    description: "Description vraiment beaucoup plus longue pour voir si ça devrait couper ou pas vraiment !",
    type: "success",
  })
}
</script>
