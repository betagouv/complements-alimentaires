<template>
  <div ref="container" class="relative">
    <div :class="hideSearchButton ? '' : 'flex items-end'">
      <div class="grow">
        <DsfrInput
          v-model="searchTerm"
          :options="autocompleteResults"
          autocomplete="nothing"
          @update:searchTerm="$emit('update:searchTerm', $event)"
          v-bind="$attrs"
          :required="required"
          @focus="hasFocus = true"
          @blur="hasFocus = false"
          @keydown="checkKeyboardNav($event)"
        />
      </div>

      <DsfrButton
        v-if="!hideSearchButton"
        class="max-h-10 mt-2 rounded-r"
        @click="search"
        :iconOnly="true"
        icon="ri-search-line"
      />
    </div>
    <ul
      v-show="displayOptions"
      ref="optionsList"
      class="list-none absolute m-0 right-0 z-1 left-0 bg-white box-shadow max-h-17 scroll pointer p-0!"
      :class="{
        'at-the-top': displayAtTheTop,
        'z-10': true,
      }"
    >
      <li
        v-for="(option, i) of autocompleteResults"
        :key="option"
        class="list-item"
        :class="{ 'active-option': activeOption === i }"
        @mousedown="selectOption(option)"
      >
        <div class="p-2 pl-4 text-left flex">
          <div class="self-center"><v-icon scale="0.85" class="mr-2" :name="getTypeIcon(option.objectType)" /></div>
          <div>
            <div>
              <span class="font-bold capitalize">{{ option.autocompleteMatch.toLowerCase() }}</span>
              <span v-if="option.autocompleteMatch !== option.name" class="ml-2 capitalize">
                ({{ option.name.toLowerCase() }})
              </span>
            </div>
            <div>{{ getTypeInFrench(option.objectType) }}</div>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { computed, nextTick, ref, watch } from "vue"
import { headers } from "@/utils/data-fetching"
import { getTypeIcon, getTypeInFrench } from "@/utils/mappings"
import { useFetch, useDebounceFn } from "@vueuse/core"
import useToaster from "@/composables/use-toaster"

const modelValue = defineModel({
  type: String,
  default: "",
})

const container = ref(undefined)
const optionsList = ref(undefined)
const autocompleteResults = ref([])
const searchTerm = ref(modelValue.value)
const debounceDelay = 350

const props = defineProps({
  options: {
    type: Array,
    default: () => [],
  },
  chooseFirstAsDefault: {
    type: Boolean,
    default: true,
  },
  hideSearchButton: {
    type: Boolean,
    default: false,
  },
  required: {
    type: Boolean,
    default: true,
  },
  type: {
    type: String,
    default: null,
  },

  // Si true, les éléments non autorisés et les substances non bioactives
  // feront partie des résultats
  searchAll: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(["selected", "search"])
const hasFocus = ref(false)
const displayOptions = computed(() => hasFocus.value && !!autocompleteResults.value.length)

function convertRemToPixels(rem) {
  return rem * parseFloat(getComputedStyle(document.documentElement).fontSize)
}

function selectOption(option) {
  emit("selected", option)
}

function search() {
  emit("search", searchTerm.value)
}

function clear() {
  searchTerm.value = ""
  autocompleteResults.value = []
}

const displayAtTheTop = ref(false)

watch(displayOptions, () => {
  if (displayOptions.value) {
    const posContainerY = container.value.offsetTop
    const containerHeight = container.value.offsetHeight
    const screenHeight = document.body.scrollHeight
    const optionsHeight = convertRemToPixels(17)
    const isTooLow = optionsHeight + posContainerY + containerHeight > screenHeight

    displayAtTheTop.value = isTooLow
  }
})

const activeOption = ref(-1)

const isVisible = function (ele, container) {
  const { bottom, height, top } = ele.getBoundingClientRect()
  const containerRect = container.getBoundingClientRect()

  return top <= containerRect.top ? containerRect.top - top <= height : bottom - containerRect.bottom <= height
}

function checkIfActiveOptionIsVisible() {
  const activeLi = optionsList.value.querySelectorAll("li")[activeOption.value]
  const isLiVisible = isVisible(activeLi, optionsList.value)
  if (!isLiVisible) {
    // Scroll to activeLi
    activeLi.scrollIntoView({ behavior: "smooth" })
  }
}

function moveToPreviousOption() {
  const isFirst = activeOption.value <= 0
  activeOption.value = isFirst ? autocompleteResults.value.length - 1 : activeOption.value - 1
  nextTick().then(checkIfActiveOptionIsVisible)
}

function moveToNextOption() {
  const isLast = activeOption.value >= autocompleteResults.value.length - 1
  activeOption.value = isLast ? 0 : activeOption.value + 1
  nextTick().then(checkIfActiveOptionIsVisible)
}

function checkKeyboardNav($event) {
  if (["ArrowUp", "ArrowDown", "Enter"].includes($event.key)) {
    $event.preventDefault()
    if (!autocompleteResults.value.length) return
  }
  if ($event.key === "Enter") {
    // Prendre le premier élément si on n'a pas explicitement sélectionné un autre
    const option = props.chooseFirstAsDefault && activeOption.value < 0 ? 0 : activeOption.value
    if (option > -1) selectOption(autocompleteResults.value[option])
    else search()
    clear()
  } else if ($event.key === "ArrowUp") {
    moveToPreviousOption()
  } else if ($event.key === "ArrowDown") {
    moveToNextOption()
  }
}

const fetchAutocompleteResults = useDebounceFn(async () => {
  if (searchTerm.value.length < 3) {
    autocompleteResults.value = []
    return
  }

  const body = { term: searchTerm.value, type: props.type, all: props.searchAll || "" }
  const { error, data } = await useFetch("/api/v1/elements/autocomplete/", { headers: headers() }).post(body).json()

  if (error.value) {
    useToaster().addMessage({
      type: "error",
      title: "Erreur",
      description: "Une erreur avec la recherche est survenue, veuillez réessayer plus tard.",
      id: "autocomplete-error",
    })
    return
  }
  autocompleteResults.value = data.value
}, debounceDelay)

watch(searchTerm, fetchAutocompleteResults)
</script>

<style scoped>
.box-shadow {
  box-shadow:
    0px 16px 16px -16px rgba(0, 0, 0, 0.32),
    0px 8px 16px rgba(0, 0, 0, 0.1);
}

.max-h-17 {
  max-height: 17rem;
}

.scroll {
  overflow: auto;
}

.at-the-top {
  bottom: 2.8rem;
  box-shadow:
    0px -16px 16px -16px rgba(0, 0, 0, 0.32),
    0px -8px 16px rgba(0, 0, 0, 0.1);
}

.list-item.active-option,
.list-item:hover {
  background-color: var(--blue-france-sun-113-625);
  color: white;
}
</style>
