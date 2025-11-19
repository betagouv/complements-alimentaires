import { useStorage } from "@vueuse/core"
import { useRoute, onBeforeRouteLeave } from "vue-router"

export const useQueryStorage = () => {
  const route = useRoute()
  const savedQuery = useStorage(route.name, {})

  onBeforeRouteLeave(() => {
    savedQuery.value = route.query
  })
}
