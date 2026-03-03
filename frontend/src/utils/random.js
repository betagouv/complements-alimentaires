// https://projets-ts-fabnum.netlify.app/client/toaster.html#le-composable-usetoaster

const alphanumBase = "abcdefghijklmnopqrstuvwyz0123456789"

const alphanum = alphanumBase.repeat(10)

const getRandomAlphaNum = () => {
  const randomIndex = Math.floor(Math.random() * alphanum.length)
  return alphanum[randomIndex]
}

const getRandomString = (length) => {
  return Array.from({ length }).map(getRandomAlphaNum).join("")
}

export const getRandomHtmlId = (prefix = "", suffix = "") => {
  return (prefix ? prefix + "-" : "") + getRandomString(5) + (suffix ? "-" + suffix : "")
}
