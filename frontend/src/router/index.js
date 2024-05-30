import { createRouter, createWebHistory } from "vue-router"
import { useRootStore } from "@/stores/root"

// layouts
import Main from "@/layouts/main"

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
import AllDeclarationsPage from "@/views/AllDeclarationsPage"
import InstructionPage from "@/views/InstructionPage"
import OfficialLetterPage from "@/views/OfficialLetterPage"

const routes = [
  {
    path: "/",
    component: Main,
    children: [
      {
        path: "accueil",
        name: "LandingPage",
        component: LandingPage,
      },
      {
        path: "entreprises",
        name: "ProducerHomePage",
        component: ProducerHomePage,
      },
      {
        path: "blog",
        name: "BlogHomePage",
        component: BlogHomePage,
        meta: {
          title: "Articles de blog",
        },
      },
      {
        path: "blog/:id",
        name: "BlogPostPage",
        component: BlogPostPage,
        props: true,
      },
      {
        path: "resultats",
        name: "ElementSearchResultsPage",
        component: ElementSearchResultsPage,
        props: true,
        beforeEnter(to) {
          if (!to.query?.q) return { to: "LandingPage" }
        },
      },
      {
        path: "element/:urlComponent",
        name: "ElementPage",
        component: ElementPage,
        props: true,
      },
      {
        path: "mentions-legales",
        name: "LegalNoticesPage",
        component: LegalNoticesPage,
        meta: {
          title: "Mentions légales",
        },
      },
      {
        path: "cgu",
        name: "CGUPage",
        component: CGUPage,
        meta: {
          title: "Conditions générales d'utilisation",
        },
      },
      {
        path: "politique-de-confidentialite",
        name: "PrivacyPolicyPage",
        component: PrivacyPolicyPage,
        meta: {
          title: "Politique de confidentialité",
        },
      },
      {
        path: "cookies",
        name: "CookiesInfoPage",
        component: CookiesInfoPage,
        meta: {
          title: "Cookies",
        },
      },
      {
        path: "connexion",
        name: "LoginPage",
        component: LoginPage,
        meta: {
          title: "Se connecter",
        },
      },
      {
        path: "inscription",
        name: "SignupPage",
        component: SignupPage,
        meta: {
          title: "S'enregistrer",
        },
      },
      {
        path: "verification-envoyee",
        name: "VerificationSentPage",
        component: VerificationSentPage,
        meta: {
          title: "Vérification envoyée",
        },
      },
      {
        path: "verification-email",
        name: "VerifyEmailPage",
        component: VerifyEmailPage,
        meta: {
          title: "Vérifier son adresse e-mail",
        },
      },
      {
        path: "pro",
        redirect: { name: "DashboardPage" },
        meta: {
          authenticationRequired: true,
        },
        children: [
          {
            path: "tableau-de-bord",
            name: "DashboardPage",
            component: DashboardPage,
            meta: { title: "Tableau de bord" },
          },
          {
            path: "nouvelle-demarche",
            name: "NewDeclaration",
            component: ProducerFormPage,
            meta: {
              title: "Nouvelle démarche",
              requiredRole: "DeclarantRole",
            },
          },
          {
            path: "informations-personnelles",
            name: "UserAccountPage",
            component: UserAccountPage,
            meta: {
              title: "Mes informations personnelles",
            },
          },
          {
            path: "entreprise/:id",
            name: "CompanyPage",
            component: CompanyPage,
            meta: {
              title: "Mon entreprise",
            },
          },
          {
            path: "nouvelle-entreprise",
            name: "CompanyFormPage",
            component: CompanyFormPage,
            meta: {
              title: "Nouvelle entreprise",
            },
          },
          {
            path: "mes-declarations",
            name: "DeclarationsHomePage",
            component: DeclarationsHomePage,
            meta: {
              title: "Mes déclarations",
            },
          },
          {
            path: "mes-declarations/:id",
            name: "DeclarationPage",
            component: ProducerFormPage,
            props: true,
            meta: {
              title: "Ma déclaration",
            },
          },
          {
            path: "gestion-des-collaborateurs",
            name: "CollaboratorsPage",
            component: CollaboratorsPage,
            meta: {
              title: "Gestion des collaborateurs",
              requiredRole: "SupervisorRole",
            },
          },
          {
            path: "toutes-les-declarations",
            name: "AllDeclarations",
            component: AllDeclarationsPage,
            meta: {
              title: "Toutes les déclarations",
              requiredRole: "InstructionRole",
              defaultQueryParams: {
                page: 1,
                status: "",
                entrepriseDe: "",
                entrepriseA: "",
              },
            },
          },
          {
            path: "instruction/:declarationId",
            props: true,
            name: "InstructionPage",
            component: InstructionPage,
            meta: {
              title: "Instruction",
              requiredRole: "InstructionRole",
            },
          },
        ],
      },
    ],
  },
  {
    path: "/lettre-officielle",
    name: "OfficialLetterPage",
    component: OfficialLetterPage, // puisqu'à la racine des routes, n'utilise pas de layout
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
    if (to.path === "/") next({ name: store.loggedUser ? "DashboardPage" : "LandingPage" })
    const authenticationCheck = !to.meta.authenticationRequired || store.loggedUser
    const roleCheck =
      !to.meta.requiredRole ||
      store.company?.roles?.some((x) => x.name === to.meta.requiredRole) ||
      store.loggedUser?.globalRoles?.some((x) => x.name === to.meta.requiredRole)

    authenticationCheck && roleCheck ? next() : next({ name: "LoginPage" })
  }
}

const ensureDefaultQueryParams = (route, next) => {
  if (!route.meta.defaultQueryParams) return
  let needsRedirection = false
  for (const [queryParam, value] of Object.entries(route.meta.defaultQueryParams))
    if (!(queryParam in route.query)) {
      route.query[queryParam] = value
      needsRedirection = true
    }
  if (needsRedirection) next(route)
}

router.beforeEach((to, from, next) => {
  const store = useRootStore()
  ensureDefaultQueryParams(to, next)
  chooseAuthorisedRoute(to, from, next, store)
})

export default router
