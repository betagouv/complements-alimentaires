import { createRouter, createWebHistory } from "vue-router"
import { useRootStore } from "@/stores/root"

// views
import LandingPage from "@/views/LandingPage"
import ProducerHomePage from "@/views/ProducerHomePage"
import BlogHomePage from "@/views/BlogHomePage"
import BlogPostPage from "@/views/BlogPostPage"
import ElementSearchResultsPage from "@/views/ElementSearchResultsPage"
import ElementPage from "@/views/ElementPage"
import CGUPage from "@/views/CGUPage"
import PrivacyPolicyPage from "@/views/PrivacyPolicyPage"
import LegalNoticesPage from "@/views/LegalNoticesPage"
import CookiesInfoPage from "@/views/CookiesInfoPage"
import ProducerFormPage from "@/views/ProducerFormPage"
import CompanyFormPage from "@/views/CompanyFormPage"
import CompanyPage from "@/views/CompanyPage"
import NotFound from "@/views/NotFound"
import LoginPage from "@/views/LoginPage"
import SignupPage from "@/views/SignupPage"
import VerifyEmailPage from "@/views/VerifyEmailPage"
import DashboardPage from "@/views/DashboardPage"
import UserAccountPage from "@/views/UserAccountPage"
import VerificationSentPage from "@/views/VerificationSentPage"
import DeclarationsHomePage from "@/views/DeclarationsHomePage"
import CollaboratorsPage from "@/views/CollaboratorsPage"
import InstructionDeclarationsPage from "@/views/InstructionDeclarationsPage"
import NewElementsPage from "@/views/NewElementsPage"
import NewVisaPage from "@/views/NewVisaPage"
import NewInstructionPage from "@/views/NewInstructionPage"
import ProductSection from "@/components/NewBepiasViews/ProductSection"
import IdentitySection from "@/components/NewBepiasViews/IdentitySection"
import HistorySection from "@/components/NewBepiasViews/HistorySection"
import VisaDeclarationsPage from "@/views/VisaDeclarationsPage"
import CompanyDeclarationsPage from "@/views/CompanyDeclarationsPage"
import A11yPage from "@/views/A11yPage.vue"
import ContactForm from "@/views/ContactForm"
import CompliancePage from "@/views/CompliancePage"
import DeclaredElementPage from "@/views/DeclaredElementPage"
import ElementForm from "@/views/ElementForm"
import MandatedCompaniesPage from "@/views/MandatedCompaniesPage"
import FaqPage from "@/views/FaqPage"
import AdvancedSearchPage from "@/views/AdvancedSearchPage"
import AdvancedSearchResult from "@/views/AdvancedSearchResult"
import StatsPage from "@/views/StatsPage"
import DeclarationSearchPage from "@/views/DeclarationSearchPage"
import CompanySearchPage from "@/views/CompanySearchPage"
import CompanyDetails from "@/views/CompanyDetails"
import DeclarationIndividualPage from "@/views/DeclarationIndividualPage"
import ProductControlSection from "@/views/DeclarationIndividualPage/ProductControlSection"
import HistoryControlSection from "@/views/DeclarationIndividualPage/HistoryControlSection"
import CompanyControlSection from "@/views/DeclarationIndividualPage/CompanyControlSection"
import SiteMap from "@/views/SiteMap"
import { ref } from "vue"

export const routes = [
  {
    path: "/",
    name: "Root",
    meta: {
      home: true,
    },
  },
  {
    path: "/accueil",
    name: "LandingPage",
    component: LandingPage,
    meta: {
      title: "Accueil",
      sitemap: true,
    },
  },
  {
    path: "/entreprises",
    name: "ProducerHomePage",
    component: ProducerHomePage,
    meta: {
      title: "Recherche ingrédients",
      sitemap: true,
    },
  },
  {
    path: "/contactez-nous",
    name: "ContactForm",
    component: ContactForm,
    meta: {
      title: "Contactez-nous",
      sitemap: true,
    },
  },
  {
    path: "/blog",
    name: "BlogHomePage",
    component: BlogHomePage,
    meta: {
      title: "Articles de blog",
      sitemap: true,
    },
  },
  {
    path: "/blog/:id",
    name: "BlogPostPage",
    component: BlogPostPage,
    props: true,
  },
  {
    path: "/resultats",
    name: "ElementSearchResultsPage",
    component: ElementSearchResultsPage,
    props: true,
    beforeEnter(to) {
      if (!to.query?.q) return { to: "LandingPage" }
    },
    meta: {
      title: "Résultats de recherche",
    },
  },
  {
    path: "/element/:urlComponent",
    name: "ElementPage",
    component: ElementPage,
    props: true,
  },
  {
    path: "/ingredient-demande/:type/:id",
    name: "DeclaredElementPage",
    component: DeclaredElementPage,
    props: true,
    meta: {
      title: "Demande d'ajout d'ingrédient",
      requiredRoles: ["InstructionRole"],
      authenticationRequired: true,
    },
  },
  {
    path: "/nouvel-ingredient",
    name: "CreateElement",
    component: ElementForm,
    meta: {
      title: "Nouvel ingrédient",
      authenticationRequired: true,
      requiredRoles: ["InstructionRole"],
    },
  },
  {
    path: "/modification-ingredient/:urlComponent",
    name: "ModifyElement",
    component: ElementForm,
    props: true,
    meta: {
      title: "Modification ingrédient",
      authenticationRequired: true,
      requiredRoles: ["InstructionRole"],
    },
  },
  {
    path: "/mentions-legales",
    name: "LegalNoticesPage",
    component: LegalNoticesPage,
    meta: {
      title: "Mentions légales",
      sitemap: true,
    },
  },
  {
    path: "/cgu",
    name: "CGUPage",
    component: CGUPage,
    meta: {
      title: "Conditions générales d'utilisation",
      sitemap: true,
    },
  },
  {
    path: "/politique-de-confidentialite",
    name: "PrivacyPolicyPage",
    component: PrivacyPolicyPage,
    meta: {
      title: "Politique de confidentialité",
      sitemap: true,
    },
  },
  {
    path: "/cookies",
    name: "CookiesInfoPage",
    component: CookiesInfoPage,
    meta: {
      title: "Cookies",
      sitemap: true,
    },
  },
  {
    path: "/accessibilite",
    name: "A11yPage",
    component: A11yPage,
    meta: {
      title: "Accessibilité",
      sitemap: true,
    },
  },
  {
    path: "/connexion",
    name: "LoginPage",
    component: LoginPage,
    meta: {
      title: "Se connecter",
      omitIfLoggedIn: true,
      sitemap: true,
    },
  },
  {
    path: "/inscription",
    name: "SignupPage",
    component: SignupPage,
    meta: {
      title: "S'enregistrer",
      omitIfLoggedIn: true,
      sitemap: true,
    },
  },
  {
    path: "/verification-envoyee",
    name: "VerificationSentPage",
    component: VerificationSentPage,
    meta: {
      title: "Vérification envoyée",
    },
  },
  {
    path: "/verification-email",
    name: "VerifyEmailPage",
    component: VerifyEmailPage,
    meta: {
      title: "Vérifier son adresse e-mail",
    },
  },
  {
    path: "/tableau-de-bord",
    name: "DashboardPage",
    component: DashboardPage,
    meta: {
      title: "Tableau de bord",
      authenticationRequired: true,
      sitemap: true,
    },
  },
  {
    path: "/nouvelle-demarche",
    name: "NewDeclaration",
    component: ProducerFormPage,
    meta: {
      title: "Nouvelle démarche",
      requiredRoles: ["DeclarantRole"],
      authenticationRequired: true,
      defaultQueryParams: {
        tab: 0,
      },
    },
  },
  {
    path: "/informations-personnelles",
    name: "UserAccountPage",
    component: UserAccountPage,
    meta: {
      title: "Mes informations personnelles",
      authenticationRequired: true,
    },
  },
  {
    path: "/entreprise/:id",
    name: "CompanyPage",
    component: CompanyPage,
    meta: {
      title: "Mon entreprise",
      authenticationRequired: true,
    },
  },
  {
    path: "/nouvelle-entreprise",
    name: "CompanyFormPage",
    component: CompanyFormPage,
    meta: {
      title: "Nouvelle entreprise",
      authenticationRequired: true,
    },
  },
  {
    path: "/mes-declarations",
    name: "DeclarationsHomePage",
    component: DeclarationsHomePage,
    meta: {
      title: "Mes déclarations",
      authenticationRequired: true,
      defaultQueryParams: {
        page: 1,
        status: "DRAFT,OBSERVATION,OBJECTION,INSTRUCTION",
        company: "",
        author: "",
        limit: "10",
        recherche: "",
      },
    },
  },
  {
    path: "/mes-declarations/:id",
    name: "DeclarationPage",
    component: ProducerFormPage,
    props: true,
    meta: {
      title: "Ma déclaration",
      authenticationRequired: true,
      defaultQueryParams: {
        tab: 0,
      },
    },
  },
  {
    path: "/gestion-des-collaborateurs/:id",
    name: "CollaboratorsPage",
    component: CollaboratorsPage,
    meta: {
      title: "Gestion des collaborateurs",
      requiredRoles: ["SupervisorRole"],
      authenticationRequired: true,
    },
  },
  {
    path: "/mandats/:id",
    name: "MandatedCompaniesPage",
    component: MandatedCompaniesPage,
    meta: {
      title: "Gestion des entreprises mandatées",
      requiredRoles: ["SupervisorRole"],
      authenticationRequired: true,
    },
  },
  {
    path: "/les-declarations-de-mon-entreprise/:id",
    name: "CompanyDeclarationsPage",
    component: CompanyDeclarationsPage,
    meta: {
      title: "Les déclarations de mon entreprise",
      requiredRoles: ["SupervisorRole"],
      authenticationRequired: true,
      defaultQueryParams: {
        page: 1,
        status: "INSTRUCTION,OBJECTION,OBSERVATION,ABANDONED,AUTHORIZED,WITHDRAWN",
        company: "",
        author: "",
        recherche: "",
      },
    },
  },
  {
    path: "/instruction",
    name: "InstructionDeclarations",
    component: InstructionDeclarationsPage,
    meta: {
      title: "Instruction",
      requiredRoles: ["InstructionRole"],
      authenticationRequired: true,
      defaultQueryParams: {
        page: 1,
        status: "AWAITING_INSTRUCTION,ONGOING_INSTRUCTION",
        entrepriseDe: "",
        entrepriseA: "",
        personneAssignée: "",
        triage: "responseLimitDate",
        article: "",
        limit: "10",
        recherche: "",
      },
    },
  },
  {
    path: "/nouveaux-ingredients",
    name: "NewElementsPage",
    component: NewElementsPage,
    meta: {
      title: "Nouveaux ingrédients",
      requiredRoles: ["InstructionRole"],
      authenticationRequired: true,
      defaultQueryParams: {
        page: 1,
        statut: "REQUESTED,INFORMATION",
        type: "", // par défaut on ne filtre pas sur le type
        statutDeclaration: "", // par défaut on filtre par les statuts ouverts
        triage: "responseLimitDate",
        limit: "10",
      },
    },
  },
  {
    path: "/instruction/:declarationId",
    props: true,
    component: NewInstructionPage,
    meta: {
      title: "Instruction",
      requiredRoles: ["InstructionRole"],
      authenticationRequired: true,
    },
    children: [
      {
        path: "",
        redirect: { name: "InstructionPage" },
      },
      {
        name: "InstructionPage",
        path: "instruction",
        component: ProductSection,
      },
      {
        name: "IdentitySection",
        path: "identite",
        component: IdentitySection,
      },
      {
        name: "HistorySection",
        path: "historique",
        component: HistorySection,
      },
    ],
  },
  {
    path: "/visa/:declarationId",
    props: true,
    component: NewVisaPage,
    meta: {
      title: "Visa",
      requiredRoles: ["VisaRole"],
      authenticationRequired: true,
    },
    children: [
      {
        path: "",
        redirect: { name: "VisaPage" },
      },
      {
        name: "VisaPage",
        path: "produit",
        component: ProductSection,
      },
      {
        name: "VisaIdentitySection",
        path: "identite",
        component: IdentitySection,
      },
      {
        name: "VisaHistorySection",
        path: "historique",
        component: HistorySection,
      },
    ],
  },
  {
    path: "/visa",
    name: "VisaDeclarations",
    component: VisaDeclarationsPage,
    meta: {
      title: "Visa",
      requiredRoles: ["VisaRole"],
      authenticationRequired: true,
      defaultQueryParams: {
        page: 1,
        status: "AWAITING_VISA,ONGOING_VISA",
        entrepriseDe: "",
        entrepriseA: "",
        triage: "responseLimitDate",
        article: "",
        limit: "10",
      },
    },
  },
  {
    path: "/conformite",
    props: true,
    name: "CompliancePage",
    component: CompliancePage,
    meta: {
      title: "Conformité au droit alimentaire",
      sitemap: true,
    },
  },
  {
    path: "/faq",
    name: "FaqPage",
    component: FaqPage,
    meta: {
      title: "Foire aux questions",
      sitemap: true,
    },
  },
  {
    path: "/stats",
    name: "StatsPage",
    component: StatsPage,
    meta: {
      title: "Mesures d'impact",
      sitemap: true,
    },
  },
  {
    path: "/recherche-avancee",
    name: "AdvancedSearchPage",
    component: AdvancedSearchPage,
    meta: {
      title: "Recherche avancée",
      requiredRoles: ["InstructionRole", "VisaRole"],
      authenticationRequired: true,
      defaultQueryParams: {
        page: 1,
        status:
          "AWAITING_INSTRUCTION,ONGOING_INSTRUCTION,AWAITING_VISA,ONGOING_VISA,OBJECTION,OBSERVATION,ABANDONED,AUTHORIZED,REJECTED,WITHDRAWN",
        triage: "-creationDate",
        article: "",
        population: "",
        condition: "",
        formeGalenique: "",
        limit: "10",
        recherche: "",
        composition: "",
        pays: "",
        dose: "",
        soumissionAvant: "",
        soumissionApres: "",
        decisionAvant: "",
        decisionApres: "",
      },
    },
  },
  {
    path: "/recherche-avancee/:declarationId",
    props: true,
    name: "AdvancedSearchResult",
    component: AdvancedSearchResult,
    meta: {
      title: "Résultat de recherche",
      authenticationRequired: true,
      requiredRoles: ["InstructionRole", "VisaRole"],
    },
  },
  {
    path: "/recherche-complements-alimentaires",
    name: "DeclarationSearchPage",
    component: DeclarationSearchPage,
    meta: {
      title: "Tableau des compléments alimentaires",
      requiredRoles: ["ControlRole"],
      authenticationRequired: true,
      defaultQueryParams: {
        page: 1,
        limit: 10,
        triage: "-creationDate",
        simplifiedStatus: "",
        surveillanceOnly: "false",
        population: "",
        condition: "",
        formeGalenique: "",
      },
    },
  },
  {
    path: "/recherche-entreprises",
    name: "CompanySearchPage",
    component: CompanySearchPage,
    meta: {
      title: "Les entreprises",
      requiredRoles: ["ControlRole"],
      authenticationRequired: true,
      defaultQueryParams: {
        page: 1,
        limit: 10,
        triage: "-creationDate",
      },
    },
  },
  {
    path: "/detail-entreprise/:companyId",
    name: "CompanyDetails",
    props: true,
    component: CompanyDetails,
    meta: {
      title: "Détail de l'entreprise",
      requiredRoles: ["ControlRole"],
      authenticationRequired: true,
      defaultQueryParams: {
        page: 1,
        limit: 10,
        triage: "-creationDate",
        simplifiedStatus: "",
      },
    },
  },
  {
    path: "/complement-alimentaire/:declarationId",
    props: true,
    component: DeclarationIndividualPage,
    meta: {
      title: "Complément alimentaire",
      authenticationRequired: true,
      requiredRoles: ["ControlRole"],
    },
    children: [
      {
        path: "",
        redirect: { name: "DeclarationIndividualPage" },
      },
      {
        name: "DeclarationIndividualPage",
        path: "produit",
        component: ProductControlSection,
      },
      {
        name: "DeclarationHistoryPage",
        path: "historique",
        component: HistoryControlSection,
      },
      {
        name: "DeclarationCompanyPage",
        path: "entreprise",
        component: CompanyControlSection,
      },
    ],
  },
  {
    path: "/sitemap",
    component: SiteMap,
    name: "SiteMap",
  },
  {
    path: "/:catchAll(.*)*", // https://stackoverflow.com/a/70343919/2255491
    component: NotFound,
    name: "NotFound",
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) return { el: to.hash }

    // Ne pas scroller en haut si c'est simplement un changement de queryparam
    if (from.name === to.name && from.fullPath !== to.fullPath) return

    if (savedPosition) return savedPosition
    return { top: 0 }
  },
})

const chooseAuthorisedRoute = async (to, from, next, store) => {
  // 1) vérifie si les données initiales sont chargées, sinon le fait avant toute chose
  if (!store.initialDataLoaded) {
    store
      .fetchInitialData()
      .then(() => chooseAuthorisedRoute(to, from, next, store))
      .catch((e) => {
        console.error(`An error occurred: ${e}`)
        next({ name: "LandingPage" })
      })
  } else {
    // 2) vérifie les règles de redirection
    if (to.meta.home) {
      next({ name: store.loggedUser ? "DashboardPage" : "LandingPage" })
      return
    }
    if (to.meta.omitIfLoggedIn && store.loggedUser) {
      next(to.query.next || { name: "DashboardPage" })
      return
    }
    const authenticationCheck = !to.meta.authenticationRequired || store.loggedUser
    const companyRoles = store.companies?.map((x) => x.roles.map((y) => y.name) || []).flat() || []
    const globalRoles = store.loggedUser?.globalRoles?.map((x) => x.name) || []
    const roles = [...companyRoles, ...globalRoles]
    const roleCheck = !to.meta.requiredRoles || to.meta.requiredRoles.some((x) => roles.indexOf(x) > -1)

    if (!authenticationCheck) next({ name: "LoginPage", query: { next: to.path } })
    else if (!roleCheck) next({ name: "DashboardPage" })
    else next()
  }
}

const ensureDefaultQueryParams = (route, next) => {
  if (!route.meta.defaultQueryParams) return true
  let needsRedirection = false
  for (const [queryParam, value] of Object.entries(route.meta.defaultQueryParams))
    if (!(queryParam in route.query)) {
      route.query[queryParam] = value
      needsRedirection = true
    }
  if (!needsRedirection) return true
  next(route)
  return false
}

// This utility function allows us to find the previous route
const previousRoute = ref(null)
router.getPreviousRoute = () => previousRoute

router.navigateBack = (defaultRoute, additionalParameters) => {
  const backRoute = router.getPreviousRoute().value || defaultRoute
  if (additionalParameters) {
    Object.assign(backRoute, additionalParameters)
  }
  router.push(backRoute)
}

router.beforeEach((to, from, next) => {
  const store = useRootStore()
  previousRoute.value = from
  if (ensureDefaultQueryParams(to, next)) chooseAuthorisedRoute(to, from, next, store)
})

export default router
