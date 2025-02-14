// merci https://github.com/vuejs/vue-router/issues/997#issuecomment-1536254142
export const getLastRouteMaybe = (router) => {
  const backUrl = router.options.history.state.back
  return backUrl && router.resolve({ path: `${backUrl}` })
}

export const navigateBack = (router, defaultRoute, additionalParameters) => {
  const backRoute = getLastRouteMaybe(router) || defaultRoute
  if (additionalParameters) {
    Object.assign(backRoute, additionalParameters)
  }
  router.push(backRoute)
}
