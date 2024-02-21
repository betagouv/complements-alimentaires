<template>
  <div class="p-10">
    <button @click="toto">CLICK</button>
  </div>
</template>

<script setup>
import useToaster from "@/composables/use-toaster"

const toaster = useToaster()
const toto = () => {
  toaster.addMessage({
    title: "Message 1",
    description: "Description 1",
    type: "info",
    closeable: true,
    titleTag: "h3",
    timeout: 6000, // ...qui disparaîtra après 6 secondes...
  })
  toaster.addMessage({
    description: "Description plus longue",
    type: "success",
  })
}
</script>
