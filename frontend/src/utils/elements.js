export const getElementName = (e) => e.element?.name || e.newName || `${e.newGenre} ${e.newSpecies}`

export const getObjectSubTypeList = (objectList, subType = null) => {
  return subType
    ? objectList.filter((obj) => obj.element?.objectType == subType || obj.newType == subType)
    : objectList.filter((obj) => !obj.element?.objectType && !obj.newType)
}
