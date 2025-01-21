import { slugifyType } from "@/utils/mappings"

// on check e.substance car c'est le format des substances calculés
export const getElementName = (e) => e.element?.name || e.substance?.name || e.newName

export const getObjectSubTypeList = (objectList, subType = null) => {
  return subType
    ? objectList.filter((obj) => obj.element?.objectType == subType || obj.newType == subType)
    : objectList.filter((obj) => !obj.element?.objectType && !obj.newType)
}

export const getElementUrlComponent = (e, type) => `${e.id}--${slugifyType(type || e.objectType)}--${e.name}`
