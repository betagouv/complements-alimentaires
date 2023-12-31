import { createApp } from "vue"
import "./styles/index.css"
import * as icons from "./icons.js"
import { OhVueIcon, addIcons } from "oh-vue-icons"
import "@gouvfr/dsfr/dist/dsfr.min.css" // Import des styles du DSFR
import "@gouvminint/vue-dsfr/styles" // Import des styles globaux propre à VueDSFR
import VueDsfr from "@gouvminint/vue-dsfr" // Import (par défaut) de la bibliothèque

import App from "./App.vue"
import router from "./router"
import store from "./store"

addIcons(...Object.values({ icons }))

const app = createApp(App)
  .use(router)
  .use(store)
  .use(VueDsfr, { icons: Object.values(icons) })
app.component("v-icon", OhVueIcon)
app.mount("#app")
