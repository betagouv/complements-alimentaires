import tailwindConfig from "/tailwind.config.js"

export const getCurrentBreakpoint = () => {
  /*
  Retourne le breakpoint actif depuis notre config tailwind. À noter que
  les breakpoints doivent être triés dans le fichier de configuration.
  */
  for (const [key, value] of Object.entries(tailwindConfig.theme.screens)) {
    const numericValue = parseInt(value.replace("px", ""))
    if (window.innerWidth < numericValue) return key
  }
  return null
}
