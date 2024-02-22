<template>
  <DsfrCard
    :key="props.post.id"
    :title="props.post.title"
    :detail="isoToPrettyDate(props.post.displayDate)"
    :description="blogDescription(props.post)"
    :link="{ name: 'BlogPost', params: { id: props.post.id } }"
  />
</template>

<script setup>
const props = defineProps({ post: { type: Object, required: true } })
import { isoToPrettyDate } from "@/utils/date"

const blogDescription = (post) => post.tagline?.substring(0, 100) || ""
</script>
