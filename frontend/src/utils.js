// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error#custom_error_types
export class AuthenticationError extends Error {
  constructor(...params) {
    super(...params)
    // Maintains proper stack trace for where our error was thrown (only available on V8)
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, AuthenticationError)
    }
    this.name = "AuthenticationError"
  }
}

// https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Error#custom_error_types
export class BadRequestError extends Error {
  constructor(jsonPromise, ...params) {
    super(...params)
    // Maintains proper stack trace for where our error was thrown (only available on V8)
    if (Error.captureStackTrace) {
      Error.captureStackTrace(this, BadRequestError)
    }
    this.name = "BadRequestError"
    this.jsonPromise = jsonPromise
  }
}

export const verifyResponse = (response) => {
  const contentType = response.headers.get("content-type")
  const hasJSON = contentType && contentType.startsWith("application/json")

  if (response.status < 200 || response.status >= 400) {
    if (response.status === 403) throw new AuthenticationError()
    else if (response.status === 400) {
      if (hasJSON) {
        throw new BadRequestError(response.json())
      } else {
        throw new BadRequestError()
      }
    } else throw new Error(`API responded with status of ${response.status}`)
  }

  return hasJSON ? response.json() : response.text()
}
