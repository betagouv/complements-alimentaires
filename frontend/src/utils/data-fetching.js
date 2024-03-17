/* custom headers used for POST requests */
export const headers = () => ({
  "X-CSRFToken": window.CSRF_TOKEN || "",
  "Content-Type": "application/json",
})
