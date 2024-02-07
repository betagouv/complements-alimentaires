import { createRouter, createWebHistory } from "vue-router"
import LandingPage from "@/views/LandingPage"
import ProducersPage from "@/views/ProducersPage"
import BlogsHome from "@/views/BlogsHome"
import BlogPost from "@/views/BlogPost"
import SearchResults from "@/views/SearchResults"
import ElementView from "@/views/ElementView"
import CGU from "@/views/CGU.vue"
import PrivacyPolicy from "@/views/PrivacyPolicy.vue"
import LegalNotices from "@/views/LegalNotices"

const routes = [
  {
    path: "/",
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
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
