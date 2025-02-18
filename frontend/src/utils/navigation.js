export const navigateBack = (router, defaultRoute, additionalParameters) => {
  const backRoute = router.getPreviousRoute().value || defaultRoute
  if (additionalParameters) {
    Object.assign(backRoute, additionalParameters)
  }
  router.push(backRoute)
}
