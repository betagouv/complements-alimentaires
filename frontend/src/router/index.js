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
import InstructionPage from "@/views/InstructionPage"
import VisaDeclarationsPage from "@/views/VisaDeclarationsPage"
import VisaPage from "@/views/VisaPage"
import CompanyDeclarationsPage from "@/views/CompanyDeclarationsPage"
import A11yPage from "@/views/A11yPage.vue"

const routes = [
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
  },
  {
    path: "/entreprises",
    name: "ProducerHomePage",
    component: ProducerHomePage,
  },
  {
    path: "/blog",
    name: "BlogHomePage",
    component: BlogHomePage,
    meta: {
      title: "Articles de blog",
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
  },
  {
    path: "/element/:urlComponent",
    name: "ElementPage",
    component: ElementPage,
    props: true,
  },
  {
    path: "/mentions-legales",
    name: "LegalNoticesPage",
    component: LegalNoticesPage,
    meta: {
      title: "Mentions légales",
    },
  },
  {
    path: "/cgu",
    name: "CGUPage",
    component: CGUPage,
    meta: {
      title: "Conditions générales d'utilisation",
    },
  },
  {
    path: "/politique-de-confidentialite",
    name: "PrivacyPolicyPage",
    component: PrivacyPolicyPage,
    meta: {
      title: "Politique de confidentialité",
    },
  },
  {
    path: "/cookies",
    name: "CookiesInfoPage",
    component: CookiesInfoPage,
    meta: {
      title: "Cookies",
    },
  },
  {
    path: "/accessibilite",
    name: "A11yPage",
    component: A11yPage,
    meta: {
      title: "Accessibilité",
    },
  },
  {
    path: "/connexion",
    name: "LoginPage",
    component: LoginPage,
    meta: {
      title: "Se connecter",
    },
  },
  {
    path: "/inscription",
    name: "SignupPage",
    component: SignupPage,
    meta: {
      title: "S'enregistrer",
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
    meta: { title: "Tableau de bord", authenticationRequired: true },
  },
  {
    path: "/nouvelle-demarche",
    name: "NewDeclaration",
    component: ProducerFormPage,
    meta: {
      title: "Nouvelle démarche",
      requiredRole: "DeclarantRole",
      authenticationRequired: true,
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
        status: "DRAFT,OBSERVATION,OBJECTION",
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
    },
  },
  {
    path: "/gestion-des-collaborateurs/:id",
    name: "CollaboratorsPage",
    component: CollaboratorsPage,
    meta: {
      title: "Gestion des collaborateurs",
      requiredRole: "SupervisorRole",
      authenticationRequired: true,
    },
  },
  {
    path: "/les-declarations-de-mon-entreprise/:id",
    name: "CompanyDeclarationsPage",
    component: CompanyDeclarationsPage,
    meta: {
      title: "Les déclarations de mon entreprise",
      requiredRole: "SupervisorRole",
      authenticationRequired: true,
      defaultQueryParams: {
        page: 1,
        status: "AWAITING_INSTRUCTION,ONGOING_INSTRUCTION,AWAITING_VISA,ONGOING_VISA,OBJECTION,OBSERVATION",
      },
    },
  },
  {
    path: "/instruction",
    name: "InstructionDeclarations",
    component: InstructionDeclarationsPage,
    meta: {
      title: "Instruction",
      requiredRole: "InstructionRole",
      authenticationRequired: true,
      defaultQueryParams: {
        page: 1,
        status: "AWAITING_INSTRUCTION,ONGOING_INSTRUCTION",
        entrepriseDe: "",
        entrepriseA: "",
      },
    },
  },
  {
    path: "/instruction/:declarationId",
    props: true,
    name: "InstructionPage",
    component: InstructionPage,
    meta: {
      title: "Instruction",
      requiredRole: "InstructionRole",
      authenticationRequired: true,
    },
  },
  {
    path: "/visa",
    name: "VisaDeclarations",
    component: VisaDeclarationsPage,
    meta: {
      title: "Visa",
      requiredRole: "VisaRole",
      authenticationRequired: true,
      defaultQueryParams: {
        page: 1,
        status: "AWAITING_VISA,ONGOING_VISA",
        entrepriseDe: "",
        entrepriseA: "",
      },
    },
  },
  {
    path: "/visa/:declarationId",
    props: true,
    name: "VisaPage",
    component: VisaPage,
    meta: {
      title: "Visa",
      requiredRole: "VisaRole",
      authenticationRequired: true,
    },
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
    const authenticationCheck = !to.meta.authenticationRequired || store.loggedUser
    const roleCheck =
      !to.meta.requiredRole ||
      store.companies?.some((c) => c.roles?.some((x) => x.name === to.meta.requiredRole)) ||
      store.loggedUser?.globalRoles?.some((x) => x.name === to.meta.requiredRole)

    authenticationCheck && roleCheck ? next() : next({ name: "LoginPage" })
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

router.beforeEach((to, from, next) => {
  const store = useRootStore()
  if (ensureDefaultQueryParams(to, next)) chooseAuthorisedRoute(to, from, next, store)
})

export default router
