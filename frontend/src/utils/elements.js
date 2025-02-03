import { slugifyType } from "@/utils/mappings"

// on check e.substance car c'est le format des substances calculés
// faut avoir quand même le format pour les microorganismes pour le cas où on travaille avec les données
//  du front et non pas du back
export const getElementName = (e) =>
  e.element?.name || e.substance?.name || e.newName || `${e.newGenre} ${e.newSpecies}`

export const getObjectSubTypeList = (objectList, subType = null) => {
  return subType
    ? objectList.filter((obj) => (obj.element ? obj.element.objectType == subType : obj.newType == subType))
    : objectList.filter((obj) => !obj.element?.objectType && !obj.newType)
}

export const getElementUrlComponent = (e, type) => `${e.id}--${slugifyType(type || e.objectType)}--${e.name}`
