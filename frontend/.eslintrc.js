module.exports = {
  root: true,

  env: {
    node: true,
    browser: true,
    es6: true,
  },

  extends: ["plugin:vue/essential", "eslint:recommended", "plugin:prettier/recommended"],

  parser: "vue-eslint-parser",
  parserOptions: {
    parser: "@babel/eslint-parser",
    requireConfigFile: false,
  },

  rules: {
    "vue/no-mutating-props": "off",
    "vue/multi-word-component-names": "off",
    "vue/no-v-text-v-html-on-component": "off",
    "vue/no-multiple-template-root": "off",
    // Change some errors to warning only, to not prevent development
    "no-unused-vars": 1,
    "prettier/prettier": ["error", { semi: false }],
  },
  plugins: ["prettier"],

  overrides: [
    {
      files: ["**/__tests__/*.{j,t}s?(x)", "**/tests/unit/**/*.spec.{j,t}s?(x)"],
      env: {
        jest: true,
      },
    },
  ],
}
