import { createRouter, createWebHistory } from "vue-router"
import LandingPage from "@/views/LandingPage"
import BlogsHome from "@/views/BlogsHome"
import BlogPost from "@/views/BlogPost"
import SearchResults from "@/views/SearchResults"
import ElementView from "@/views/ElementView"

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
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
