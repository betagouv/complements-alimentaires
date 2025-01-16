import tailwindConfig from "/tailwind.config.js"

export const getCurrentBreakpoint = () => {
  /*
  Retourne le breakpoint actif depuis notre config tailwind.
  */
  const screensArray = Object.entries(tailwindConfig.theme.screens).map((x) => [x[0], parseInt(x[1].replace("px", ""))])
  const sortedScreens = screensArray.sort((a, b) => a[1] - b[1])
  for (const [key, value] of sortedScreens) if (window.innerWidth < value) return key
  return null
}
