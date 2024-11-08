<template>
  <div>
    <DsfrNotice title="Page en construction" />
    <DsfrNotice
      title="NOUVEL INGRÉDIENT"
      desc="Ingrédient non intégré dans la base de donnée et en attente de validation. "
    />
    <div class="fr-container">
      <!-- TODO: add link to declaration in between -->
      <DsfrBreadcrumb
        class="mb-8"
        :links="[
          { to: { name: 'InstructionDeclarations' }, text: 'Déclarations pour instruction' },
          { text: 'Demande d\'ajout d\'ingrédient' },
        ]"
      />
      <div class="grid grid-cols-2 gap-4">
        <div class="bg-grey-975 py-4 px-4 mb-8">
          <p class="mt-6">
            <v-icon :name="icon" />
            {{ typeName }}
          </p>
          <!-- TODO: flag for authorisation -->
          <!-- Maybe it's easier to do this more declaratively... -->
          <div v-for="(info, idx) in request" :key="idx" class="grid grid-cols-2">
            <p>
              <b>{{ info.label }}</b>
            </p>
            <p>{{ info.text }}</p>
          </div>
          <!-- TODO: potentially link to reglementation -->
          <div class="grid justify-items-end">
            <!-- TODO: link to decla -->
            <router-link>
              Voir la déclaration
              <v-icon icon="ri-arrow-right-line"></v-icon>
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, watch } from "vue"
import { getTypeIcon, getTypeInFrench, getApiType } from "@/utils/mappings"
import { useFetch } from "@vueuse/core"

const props = defineProps({ type: String, id: Number })
const icon = computed(() => getTypeIcon(props.type))
const typeName = computed(() => getTypeInFrench(props.type))

const url = computed(() => `/api/v1/declared-elements/${getApiType(props.type)}s/${props.id}`)
const { data: element, response, execute } = useFetch(url, { immediate: false }).get().json()

const request = computed(() => {
  if (!element.value) return []
  const items = [
    // TODO: authorisation
    {
      label: "Nom",
      text: element.value.newName,
    },
    {
      label: "Description",
      text: element.value.newDescription,
    },
    // TODO: source reglementaire
  ]
  if (element.value.authorizationMode !== "FR") {
    items.push({
      label: "Pays de référence",
      text: element.value.euReferenceCountry,
    })
  }
  return items
})

// Init
execute()
watch(element, (newElement) => {
  if (newElement) document.title = `${newElement.name} - Compl'Alim`
})
</script>
