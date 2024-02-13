import { createRouter, createWebHistory } from "vue-router"
import { useStore } from "vuex"
import LandingPage from "@/views/LandingPage"
import ProducersPage from "@/views/ProducersPage"
import BlogsHome from "@/views/BlogsHome"
import BlogPost from "@/views/BlogPost"
import SearchResults from "@/views/SearchResults"
import ElementView from "@/views/ElementView"
import CGU from "@/views/CGU.vue"
import PrivacyPolicy from "@/views/PrivacyPolicy.vue"
import LegalNotices from "@/views/LegalNotices"
import CookiesInfo from "@/views/CookiesInfo"
import ProducerForm from "@/views/ProducerForm"
import NotFound from "@/views/NotFound"

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
    name: "ProducersPage",
    component: ProducersPage,
  },
  {
    path: "/blog",
    name: "BlogsHome",
    component: BlogsHome,
    meta: {
      title: "Articles de blog",
    },
  },
  {
    path: "/blog/:id",
    name: "BlogPost",
    component: BlogPost,
    props: true,
  },
  {
    path: "/resultats/",
    name: "SearchResults",
    component: SearchResults,
    props: true,
    beforeEnter(to) {
      if (!to.query?.q) return { to: "LandingPage" }
    },
  },
  {
    path: "/element/:urlComponent",
    name: "ElementView",
    component: ElementView,
    props: true,
  },
  {
    path: "/mentions-legales",
    name: "LegalNotices",
    component: LegalNotices,
    meta: {
      title: "Mentions légales",
    },
  },
  {
    path: "/cgu",
    name: "CGU",
    component: CGU,
    meta: {
      title: "Conditions générales d'utilisation",
    },
  },
  {
    path: "/politique-de-confidentialite",
    name: "PrivacyPolicy",
    component: PrivacyPolicy,
    meta: {
      title: "Politique de confidentialité",
    },
  },
  {
    path: "/cookies",
    name: "CookiesInfo",
    component: CookiesInfo,
    meta: {
      title: "Cookies",
    },
  },
  {
    path: "/nouvelle-demarche",
    name: "ProducerForm",
    component: ProducerForm,
    meta: {
      authenticationRequired: true,
    },
  },
  {
    path: "/:catchAll(.*)",
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
  if (!store.state.initialDataLoaded) {
    store
      .dispatch("fetchInitialData")
      .then(() => chooseAuthorisedRoute(to, from, next, store))
      .catch((e) => {
        console.error(`An error occurred: ${e}`)
        next({ name: "LandingPage" })
      })
  } else {
    if (to.meta.home) next({ name: "LandingPage" })
    else if (!to.meta.authenticationRequired || store.state.loggedUser) next()
    else window.location.href = `/s-identifier?next=${to.path}`
  }
}

router.beforeEach((to, from, next) => {
  const store = useStore()
  chooseAuthorisedRoute(to, from, next, store)
})

export default router
