import tailwindConfig from "/tailwind.config.js"
import { ref, watch } from "vue"
import { useWindowSize } from "@vueuse/core"

const { width } = useWindowSize()

const getCurrentBreakpoint = () => {
  const screensArray = Object.entries(tailwindConfig.theme.screens).map((x) => [x[0], parseInt(x[1].replace("px", ""))])
  const sortedScreens = screensArray.sort((a, b) => a[1] - b[1])
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
