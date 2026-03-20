// https://projets-ts-fabnum.netlify.app/client/toaster.html#le-composable-usetoaster

// use-toaster.ts
import { reactive } from "vue"
import { getRandomHtmlId } from "@/utils/random"

/* -- Message object type --
  id?: string;
  title?: string;
  description: string;
  type?: 'info' | 'success' | 'warning' | 'error';
  closeable?: boolean;
  titleTag?: 'h1' | 'h2' | 'h3' | 'h4' | 'h5' | 'h6';
  timeout?: number;
  style?: Record<string, string>;
  class?: string | Record<string, string> | Array<string | Record<string, string>>;
*/

const timeouts = {} // Record<string, number>
const messages = reactive([]) //  Message[]

const useToaster = () => {
  const removeMessage = (id) => {
    const index = messages.findIndex((message) => message.id === id)
    clearTimeout(timeouts[id])
    if (index === -1) {
      return
    }
    messages.splice(index, 1)
  }

  const addMessage = (message) => {
    if (message.id && timeouts[message.id]) {
      removeMessage(message.id)
    }
    // These are default values for the toast
    message.id ??= getRandomHtmlId("toaster")
    message.titleTag ??= "h3"
    message.closeable ??= true
    message.type ??= "info"
    message.timeout ??= 5000
    if (!message.title && message.type === "success") message.title = "Succès"
    if (!message.title && message.type === "error") message.title = "Erreur"
    messages.push({ ...message, description: `${message.description}` })
    timeouts[message.id] = window.setTimeout(() => removeMessage(message.id), message.timeout)
  }

  const addSuccessMessage = (description) => addMessage({ type: "success", description })

  const addErrorMessage = (description) => addMessage({ type: "error", description })

  return {
    messages,
    addMessage,
    addSuccessMessage,
    addErrorMessage,
    removeMessage,
  }
}

export default useToaster
