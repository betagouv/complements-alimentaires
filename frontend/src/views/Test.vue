<template>
  <div class="p-10">
    <button @click="toto">CLICK</button>
  </div>
</template>

<script setup>
const toto = () => {
  console.log("clicked")
}
</script>
