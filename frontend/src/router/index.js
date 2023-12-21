import { createRouter, createWebHistory } from "vue-router"
import LandingPage from "@/views/LandingPage"
import BlogsHome from "@/views/BlogsHome"
import BlogPost from "@/views/BlogPost"
import SearchResults from "@/views/SearchResults"

const routes = [
  {
    path: "/",
    name: "LandingPage",
    component: LandingPage,
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
    path: "/résultats/",
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
