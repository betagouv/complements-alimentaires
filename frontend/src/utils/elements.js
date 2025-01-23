import { slugifyType } from "@/utils/mappings"

export const getElementName = (e) => e.element?.name || e.substance?.name || getNewElementName(e)

export const getNewElementName = (e) => e.newName || `${e.newGenre} ${e.newSpecies}`

export const getObjectSubTypeList = (objectList, subType = null) => {
  return subType
    ? objectList.filter((obj) => obj.element?.objectType == subType || obj.newType == subType)
    : objectList.filter((obj) => !obj.element?.objectType && !obj.newType)
}

export const getElementUrlComponent = (e, type) => `${e.id}--${slugifyType(type || e.objectType)}--${e.name}`
