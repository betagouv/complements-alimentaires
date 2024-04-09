export const getEmitIdentificationData = (responseData) => {
  // Logique à part car utilisée par 2 composants
  switch (responseData.companyStatus) {
    case "unregistered_company":
      return {
        index: 2,
        name: "Enregistrement d'une nouvelle entreprise",
        component: "CreateCompany",
        goToNextStep: true,
      }
    case "registered_and_supervised_by_me":
      return {
        index: 2,
        name: "L'entreprise existe déjà !",
        component: "NothingToDo",
        goToNextStep: true,
      }
    case "registered_and_supervised_by_other":
      return {
        index: 2,
        name: "Demande de co-gestion d'une entreprise existante",
        component: "ClaimCoSupervision",
        goToNextStep: true,
      }
    case "registered_and_unsupervised":
      return {
        index: 2,
        name: "Revendication d'une entreprise existante",
        component: "ClaimSupervision",
        goToNextStep: true,
      }
  }
}
