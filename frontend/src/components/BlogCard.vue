<template>
  <DsfrCard
    :key="props.post.id"
    :title="props.post.title"
    :detail="blogDate(props.post)"
    :description="blogDescription(props.post)"
    :link="{ name: 'BlogPost', params: { id: props.post.id } }"
  />
</template>

<script setup>
const props = defineProps({ post: { type: Object, required: true } })

const blogDate = (post) => {
  return new Date(post.displayDate).toLocaleDateString("fr-FR", {
    year: "numeric",
    month: "short",
    day: "numeric",
  })
}
const blogDescription = (post) => post.tagline?.substring(0, 100) || ""
</script>
