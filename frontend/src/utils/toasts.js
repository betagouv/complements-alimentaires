import useToaster from "@/composables/use-toaster"

export const addUnknownErrorMessage = () =>
  useToaster().addMessage({
    type: "error",
    title: "Erreur",
    description: "Une erreur est survenue, veuillez réessayer plus tard.",
  })
