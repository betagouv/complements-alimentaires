export const shouldShowReasons = (declaration) => {
  const concernedStatus = ["OBSERVATION", "OBJECTION", "REJECTED"]
  return concernedStatus.indexOf(declaration?.status) > -1 && declaration?.blockingReasons
}
