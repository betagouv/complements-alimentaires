import { createRouter, createWebHistory } from "vue-router"
import { useRootStore } from "@/stores/root"
import LandingPage from "@/views/LandingPage"
import ProducerHomePage from "@/views/ProducerHomePage"
import BlogHomePage from "@/views/BlogHomePage"
import BlogPostPage from "@/views/BlogPostPage"
import ElementSearchResultsPage from "@/views/ElementSearchResultsPage"
import ElementPage from "@/views/ElementPage"
import CGUPage from "@/views/CGUPage.vue"
import PrivacyPolicyPage from "@/views/PrivacyPolicyPage.vue"
import LegalNoticesPage from "@/views/LegalNoticesPage"
import CookiesInfoPage from "@/views/CookiesInfoPage"
import ProducerFormPage from "@/views/ProducerFormPage"
import NotFound from "@/views/NotFound"
import LoginPage from "@/views/LoginPage.vue"

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
    path: "/resultats/",
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
    path: "/nouvelle-demarche",
    name: "ProducerFormPage",
    component: ProducerFormPage,
    meta: {
      authenticationRequired: true,
    },
  },
  {
    path: "/login",
    name: "LoginPage",
    component: LoginPage,
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

function chooseAuthorisedRoute(to, from, next, store) {
  if (!store.initialDataLoaded) {
    store
      .fetchInitialData()
      .then(() => chooseAuthorisedRoute(to, from, next, store))
      .catch((e) => {
        console.error(`An error occurred: ${e}`)
        next({ name: "LandingPage" })
      })
  } else {
    if (to.meta.home) next({ name: "LandingPage" })
    else if (!to.meta.authenticationRequired || store.loggedUser) next()
    else window.location.href = `/s-identifier?next=${to.path}`
  }
}

router.beforeEach((to, from, next) => {
  const store = useRootStore()
  chooseAuthorisedRoute(to, from, next, store)
})

export default router
