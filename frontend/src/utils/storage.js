import { onMounted, nextTick } from "vue"
import { useStorage } from "@vueuse/core"
import { useRouter, useRoute, onBeforeRouteLeave } from "vue-router"

export const useQueryStorage = (storageKey, additionalSetup = () => {}) => {
  const router = useRouter()
  const route = useRoute()
  const savedQuery = useStorage(storageKey, {})

  onMounted(() => {
    if (savedQuery.value.page) {
      additionalSetup(savedQuery)
      nextTick().then(() => router.replace({ query: { ...savedQuery.value } }))
    }
  })

  onBeforeRouteLeave(() => {
    savedQuery.value = route.query
  })
}
