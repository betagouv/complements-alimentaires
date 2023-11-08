import { createApp } from "vue"
import "./styles/index.css"
import "@gouvfr/dsfr/dist/dsfr.min.css" // Import des styles du DSFR
import "@gouvminint/vue-dsfr/styles" // Import des styles globaux propre à VueDSFR
import VueDsfr from "@gouvminint/vue-dsfr" // Import (par défaut) de la bibliothèque
import "@gouvfr/dsfr/dist/utility/icons/icons.min.css"

import App from "./App.vue"

createApp(App).use(VueDsfr).mount('#app')
