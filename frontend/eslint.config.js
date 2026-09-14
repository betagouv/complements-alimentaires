import pluginVue from "eslint-plugin-vue"
import prettierRecommended from "eslint-plugin-prettier/recommended"
import js from "@eslint/js"
import globals from "globals"

export default [
  { ignores: ["**/web/static/js/**"] },
  js.configs.recommended,
  ...pluginVue.configs["flat/essential"],
  prettierRecommended,
  {
    languageOptions: {
      globals: {
        ...globals.node,
        ...globals.browser,
        ...globals.es2015,
      },
    },
    rules: {
      "vue/no-mutating-props": "off",
      "vue/multi-word-component-names": "off",
      "vue/no-v-text-v-html-on-component": "off",
      "vue/no-multiple-template-root": "off",
      "no-unused-vars": 1,
      "prettier/prettier": ["error", { semi: false }],
    },
  },
]
