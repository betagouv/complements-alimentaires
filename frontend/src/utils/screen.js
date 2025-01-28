import { ref, watch } from "vue"
import { useWindowSize } from "@vueuse/core"

const { width } = useWindowSize()

const getCurrentBreakpoint = () => {
  const sortedScreens = [576, 768, 992, 1440] // from index.css
  for (const [key, value] of sortedScreens) if (width.value < value) return key
  return sortedScreens[sortedScreens.length - 1][0]
}

export const useCurrentBreakpoint = () => {
  /*
  Retourne une ref vers le breakpoint actif depuis notre config tailwind.
  */
  const breakpoint = ref(null)
  watch(width, () => (breakpoint.value = getCurrentBreakpoint()), { immediate: true })
  return breakpoint
}
