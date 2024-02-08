import { createRouter, createWebHistory } from "vue-router"
import { useStore } from "vuex"
import LandingPage from "@/views/LandingPage"
import ProducersPage from "@/views/ProducersPage"
import BlogsHome from "@/views/BlogsHome"
import BlogPost from "@/views/BlogPost"
import SearchResults from "@/views/SearchResults"
import ElementView from "@/views/ElementView"
import ProducerForm from "@/views/ProducerForm"

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
    path: "/nouvelle-demarche",
    name: "ProducerForm",
    component: ProducerForm,
    meta: {
      authenticationRequired: true,
    },
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
