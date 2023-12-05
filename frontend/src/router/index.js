import { createRouter, createWebHistory } from "vue-router"
import LandingPage from "@/views/LandingPage"
import BlogsHome from "@/views/BlogsHome"
import BlogPost from "@/views/BlogPost"

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
  },
  {
    path: "/blog/:id",
    name: "BlogPost",
    component: BlogPost,
    props: true,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
