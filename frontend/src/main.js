import { createApp } from "vue"
import "./styles/index.css"
import VueMatomo from "vue-matomo"
import "@gouvfr/dsfr/dist/dsfr.min.css" // Import des styles du DSFR
import "@gouvminint/vue-dsfr/styles" // Import des styles globaux propre à VueDSFR
import VueDsfr from "@gouvminint/vue-dsfr" // Import (par défaut) de la bibliothèque

import App from "./App.vue"
import router from "./router"
import { createPinia } from "pinia"

const pinia = createPinia()
const app = createApp(App).use(router).use(pinia).use(VueDsfr)

if (window.MATOMO_ID)
  app.use(VueMatomo, {
    host: "https://stats.beta.gouv.fr",
    siteId: window.MATOMO_ID,
    trackerFileName: "matomo",
    router: router,
    requireConsent: false,
    enableLinkTracking: true,
    trackInitialView: true,
    debug: false,
    userId: undefined,
  })

app.mount("#app")
