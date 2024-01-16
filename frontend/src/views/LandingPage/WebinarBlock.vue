<template>
  <div v-if="webinars && webinars.length > 0">
    <h3>Webinaires à venir</h3>
    <p class="m-0">
      Expertes et experts du secteur partagent expériences et conseils pour développer vos produits et répondre à vos
      obligations réglementaires, inscrivez-vous pour y assister !
    </p>
    <div class="border border-slate-200 my-4 grid grid-cols-12" v-for="webinar in webinars" :key="webinar.id">
      <div :class="`hidden md:flex md:justify-center md:col-span-3 ${gradientClass}`">
        <img
          src="/static/images/ca-webinar.jpg"
          class="object-scale-down self-center rounded-full bg-white h-40 w-40 border-solid border-4 border-blue-france-main-525"
        />
      </div>
      <div class="p-6 col-span-12 sm:col-span-8 md:col-span-6">
        <div class="fr-h4">{{ webinar.title }}</div>
        <div>{{ webinar.tagline }}</div>
      </div>
      <div class="p-6 col-span-12 sm:col-span-4 md:col-span-3">
        <div class="font-bold capitalize">{{ formattedDate(webinar) }}</div>
        <div class="mb-4">{{ formattedStartTime(webinar) }} à {{ formattedEndTime(webinar) }}</div>
        <div class="fr-text--xs text-slate-500">
          <v-icon scale="0.9" class="-mb-1 mr-1" name="ri-video-chat-line"></v-icon>
          Visio-conférence
        </div>
        <a :href="webinar.link">
          <DsfrButton label="Je m'inscris" />
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { verifyResponse } from "@/utils"

const webinars = ref(null)

const gradientClass = "bg-gradient-to-r from-blue-france-925 via-blue-france-850 via-30 to-transparent"

const formattedDate = (webinar) => {
  const options = {
    weekday: "long",
    month: "long",
    day: "numeric",
  }
  const date = new Date(webinar.startDate)
  return date.toLocaleString("fr", options)
}

const formatTime = (date) => {
  const hour = date.toLocaleString("fr", { hour: "numeric" })
  const minutes = date.toLocaleString("fr", { minute: "2-digit" })
  return `${hour}${minutes}`.replace(" ", "")
}

const formattedStartTime = (webinar) => formatTime(new Date(webinar.startDate))
const formattedEndTime = (webinar) => formatTime(new Date(webinar.endDate))

onMounted(() => {
  const url = "/api/v1/webinars/"
  return fetch(url)
    .then(verifyResponse)
    .then((response) => (webinars.value = response))
    .catch(() => {
      window.alert("Une erreur est survenue veuillez réessayer plus tard")
    })
})
</script>
