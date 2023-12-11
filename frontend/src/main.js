import { createApp } from "vue"
import "./styles/index.css"
import * as icons from "./icons.js"
import "@gouvfr/dsfr/dist/dsfr.min.css" // Import des styles du DSFR
import "@gouvminint/vue-dsfr/styles" // Import des styles globaux propre à VueDSFR
import VueDsfr from "@gouvminint/vue-dsfr" // Import (par défaut) de la bibliothèque
import "@gouvfr/dsfr/dist/utility/icons/icons.min.css"

import App from "./App.vue"
import router from "./router"
import store from "./store"

createApp(App)
  .use(router)
  .use(store)
  .use(VueDsfr, { icons: Object.values(icons) })
  .mount("#app")
