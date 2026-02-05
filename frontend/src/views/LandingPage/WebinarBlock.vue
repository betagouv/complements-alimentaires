<template>
  <div v-if="webinars.length > 0">
    <h3>Webinaires à venir</h3>
    <p class="m-0">
      Expertes et experts du secteur partagent expériences et conseils pour développer vos produits et répondre à vos
      obligations réglementaires, inscrivez-vous pour y assister !
    </p>
    <div class="border border-slate-200 my-4 grid grid-cols-12" v-for="webinar in webinars" :key="webinar.id">
      <div class="hidden md:flex md:justify-center md:col-span-3 gradient-dsfr">
        <img
          src="/static/images/ca-webinar.jpg"
          class="object-scale-down self-center rounded-full bg-white h-40 w-40 border-solid border-4 border-blue-france-main-525"
          alt=""
        />
      </div>
      <div class="p-6 col-span-12 sm:col-span-8 md:col-span-6">
        <div class="fr-h4">{{ webinar.title }}</div>
        <div>{{ webinar.tagline }}</div>
      </div>
      <div class="p-6 col-span-12 sm:col-span-4 md:col-span-3">
        <div class="font-bold capitalize">{{ isoToPrettyDate(webinar.startDate, dateOptions) }}</div>
        <div class="mb-4">{{ isoToPrettyTime(webinar.startDate) }} à {{ isoToPrettyTime(webinar.endDate) }}</div>
        <div class="fr-text--xs text-slate-500">
          <v-icon scale="0.9" class="-mb-1 mr-1" name="ri-video-chat-line"></v-icon>
          Visio-conférence
        </div>
        <a :href="webinar.link" target="_blank" rel="noopener external" class="fr-btn fr-btn--md">Je m'inscris</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useFetch } from "@vueuse/core"
import { isoToPrettyDate, isoToPrettyTime } from "@/utils/date"
import { handleError } from "@/utils/error-handling"

const dateOptions = {
  weekday: "long",
  month: "long",
  day: "numeric",
}

const { data: webinars, response } = await useFetch("/api/v1/webinars").json()
await handleError(response)
</script>
