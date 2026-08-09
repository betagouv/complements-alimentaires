import { createFetch } from "@vueuse/core"

export const headers = () => ({
  "Content-Type": "application/json",
})

export const useFetch = createFetch({
  baseUrl: import.meta.env.VITE_API_ROOT,
  fetchOptions: {
    credentials: import.meta.env.VITE_CREDENTIALS || "same-origin",
  },
  options: {
    beforeFetch({ options }) {
      const csrfToken = localStorage.getItem("csrfToken")
      if (csrfToken) {
        options.headers = { ...options.headers, "X-CSRFToken": csrfToken }
      }
      return { options }
    },
  },
})
