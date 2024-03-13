<template>
  <DsfrButton label="Créer un nouvel ingrédient" secondary size="sm" @click="opened = true" ref="modalOrigin" />
  <DsfrModal ref="modal" @close="opened = false" :opened="opened">
    <p>
      Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas varius tortor nibh, sit amet tempor nibh finibus
      et. Aenean eu enim justo. Vestibulum aliquam hendrerit molestie. Mauris malesuada nisi sit amet augue accumsan
      tincidunt. Maecenas tincidunt, velit ac porttitor pulvinar, tortor eros facilisis libero, vitae commodo nunc quam
      et ligula. Ut nec ipsum sapien. Interdum et malesuada fames ac ante ipsum primis in faucibus. Integer id nisi nec
      nulla luctus lacinia non eu turpis. Etiam in ex imperdiet justo tincidunt egestas. Ut porttitor urna ac augue
      cursus tincidunt sit amet sed orci.
    </p>
  </DsfrModal>
</template>

<script setup>
import { ref } from "vue"

const opened = ref(false)
</script>
