<template>
  <div class="p-4 border shadow-md">
    <div class="sm:flex">
      <div class="flex">
        <div class="self-center">
          <div class="font-bold capitalize">
            {{ getElementName(model).toLowerCase() }}
          </div>
          <div v-if="synonyms">
            {{ synonyms }}
          </div>
          <div v-if="model.new" class="self-center mt-1">
            <DsfrBadge label="Nouvel ingrédient" type="info" />
          </div>
        </div>
        <div class="content-center ml-6 pl-4 sm:border-l">
          <ElementCommentModal v-model="model" :hidePrivateComments="true" />
        </div>
      </div>

      <div class="flex grow">
        <div class="grow sm:pl-4 sm:ml-4 pt-4 sm:border-l self-center">
          <DsfrCheckbox
            :disabled="getActivityReadonlyByType(objectType)"
            v-model="model.active"
            :label="model.active ? 'Actif' : 'Non actif'"
          />
        </div>

        <div><DsfrButton secondary @click="$emit('remove', model)">Enlever</DsfrButton></div>
      </div>
    </div>

    <div v-if="showFields">
      <hr class="mt-2" />
      <ElementDetail :objectType="objectType" v-model="model" />
    </div>
  </div>
</template>

<script setup>
import { computed, watch } from "vue"
import { getElementName } from "@/utils/elements"
import { getActivityReadonlyByType } from "@/utils/mappings"
import ElementCommentModal from "@/components/ElementCommentModal"
import ElementDetail from "@/components/ElementDetail"

const model = defineModel()

defineEmits(["remove"])
const props = defineProps({ objectType: { type: String } })
const synonyms = computed(() => model.value.element?.synonyms?.map((x) => x.name)?.join(", "))

const showFields = computed(() => {
  if (model.value.active && ["plant", "microorganism"].indexOf(props.objectType) >= 0) return true
  if (
    model.value.active &&
    ["active_ingredient", "form_of_supply", "substance"].indexOf(props.objectType) >= 0 &&
    !model.value.element?.substances?.length
  )
    // TODO: à terme les form_of_supply auront forcément des substances liées donc cette condition ne sera plus nécessaire
    // TODO: à terme le type active_ingredient n'existera plus, seulement le type ingrédient et la propriété active
    return true
  return false
})

// Reset de l'unité si le microorganism est inactivé
watch(
  () => model.value.activated,
  (activatedField) => {
    if (activatedField == false) {
      model.value.quantity = null
    }
  }
)
</script>
