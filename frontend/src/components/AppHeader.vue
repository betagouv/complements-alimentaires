<template>
  <DsfrHeader :logo-text="logoText" service-title="Compléments alimentaires" :quickLinks="quickLinks">
    <template v-if="environment != 'prod'" #operator>
      <DsfrBadge v-if="environment === 'dev'" :label="environment" type="info" />
      <DsfrBadge v-else-if="environment === 'demo'" :label="environment" type="new" />
      <DsfrBadge v-else :label="environment" type="warning" />
    </template>
    <template #mainnav>
      <DsfrNavigation :nav-items="navItems" />
    </template>
  </DsfrHeader>
  <DsfrModal title="Voulez-vous fermer votre session ?" :opened="logoutModalOpened" @close="closeModal">
    <form action="/se-deconnecter" method="post" class="inline">
      <input type="hidden" name="csrfmiddlewaretoken" :value="csrfToken" />
      <DsfrButton class="mr-2">Me déconnecter</DsfrButton>
    </form>
    <DsfrButton tertiary @click="closeModal">Revenir en arrière</DsfrButton>
  </DsfrModal>
</template>

<script setup>
import { computed, onMounted, watch, ref } from "vue"
import { useStore } from "vuex"
import { useRoute, useRouter } from "vue-router"

const logoutModalOpened = ref(false)

const route = useRoute()
const router = useRouter()

const csrfToken = window.CSRF_TOKEN

const logoText = ["Ministère", "de l'Agriculture", "et de la Souveraineté", "Alimentaire"]
const environment = window.ENVIRONMENT
const store = useStore()
const navItems = [
  {
    to: "/",
    text: "Accueil",
  },
  {
    to: "/entreprises",
    text: "Entreprises",
  },
  {
    to: "/blog",
    text: "Blog",
  },
]
const quickLinks = computed(function () {
  if (store.state.loggedUser)
    return [
      {
        label: "Se déconnecter",
        icon: "ri-logout-box-r-line",
        to: { query: { "confirmation-deconnexion": true }, replace: true },
      },
    ]
  else return []
})
onMounted(() => {
  store.dispatch("fetchLoggedUser")
})
const closeModal = () => {
  router.replace({ query: {} })
}
watch(
  () => route.query["confirmation-deconnexion"],
  (newValue) => {
    logoutModalOpened.value = newValue
  }
)
</script>
