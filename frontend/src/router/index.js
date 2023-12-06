import { createRouter, createWebHistory } from "vue-router"
import LandingPage from "@/views/LandingPage"
import SearchResults from "@/views/SearchResults"

const routes = [
  {
    path: "/",
    name: "LandingPage",
    component: LandingPage,
  },
  {
    path: "/résultats",
    name: "SearchResults",
    component: SearchResults,
    props: true,
    beforeEnter(to) {
      if (!to.query?.q) return { to: "LandingPage" }
    },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
