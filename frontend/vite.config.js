import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
import tailwindcss from "@tailwindcss/vite"
import { fileURLToPath, URL } from "url"

// https://vite.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("src", import.meta.url)),
    },
    extensions: [".mjs", ".js", ".ts", ".jsx", ".tsx", ".json", ".vue"],
  },
  plugins: [vue(), tailwindcss()],
  css: {
    lightningcss: {
      // Fix d'un bug de lightningCSS décrit ici : https://github.com/parcel-bundler/lightningcss/issues/214
      errorRecovery: true,
    },
  },
  base: "/",
})
