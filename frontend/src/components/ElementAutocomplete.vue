<template>
  <div ref="container" class="relative">
    <DsfrInput
      :model-value="modelValue"
      @update:model-value="$emit('update:modelValue', $event)"
      v-bind="$attrs"
      :required="true"
      @focus="hasFocus = true"
      @blur="hasFocus = false"
      @keydown="checkKeyboardNav($event)"
    />
    <ul
      v-show="displayOptions"
      ref="optionsList"
      class="list-none absolute m-0 right-0 z-1 left-0 bg-white box-shadow max-h-17 scroll pointer !p-0"
      :class="{
        'at-the-top': displayAtTheTop,
        'z-10': true,
      }"
    >
      <li
        v-for="(option, i) of options"
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
            <div>{{ getType(option.objectType) }}</div>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { computed, nextTick, ref, watch } from "vue"
import { getTypeIcon, getType } from "@/utils/mappings"

const container = ref(undefined)
const optionsList = ref(undefined)

const props = defineProps({
  options: {
    type: Array,
    default: () => [],
  },
})

defineModel({
  type: String,
  default: "",
})

const emit = defineEmits(["selected"])
const hasFocus = ref(false)
const displayOptions = computed(() => hasFocus.value && !!props.options.length)

function convertRemToPixels(rem) {
  return rem * parseFloat(getComputedStyle(document.documentElement).fontSize)
}

function selectOption(option) {
  emit("selected", option)
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
  activeOption.value = isFirst ? props.options.length - 1 : activeOption.value - 1
  nextTick().then(checkIfActiveOptionIsVisible)
}

function moveToNextOption() {
  const isLast = activeOption.value >= props.options.length - 1
  activeOption.value = isLast ? 0 : activeOption.value + 1
  nextTick().then(checkIfActiveOptionIsVisible)
}

function checkKeyboardNav($event) {
  if (["ArrowUp", "ArrowDown", "Enter"].includes($event.key)) {
    $event.preventDefault()
    if (!props.options.length) return
  }
  if ($event.key === "Enter") {
    selectOption(props.options[activeOption.value])
  } else if ($event.key === "ArrowUp") {
    moveToPreviousOption()
  } else if ($event.key === "ArrowDown") {
    moveToNextOption()
  }
}
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
