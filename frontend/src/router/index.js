import { createRouter, createWebHistory } from "vue-router"
import LandingPage from "@/views/LandingPage"
import BlogsHome from "@/views/BlogsHome"

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
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
