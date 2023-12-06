/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,vue}"],
  theme: {
    extend: {},

    // DSFR breakpoints taken from here:
    // https://github.com/dnum-mi/vue-dsfr/blob/e363297144888021f3d4379c13ef0164ba80a90e/.storybook/preview.ts#L44
    screens: {
      sm: "576px",
      md: "768px",
      lg: "992px",
      xl: "1440px",
    },
  },
  plugins: [],
}
