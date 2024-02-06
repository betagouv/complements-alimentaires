/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{html,js,vue}"],
  theme: {
    extend: {
      colors: {
        "blue-france-main-525": "#6a6af4",
        "blue-france-sun-113": "#000091",
        "blue-france-975": "#f5f5fe",
        "blue-france-950": "#ececfe",
        "blue-france-925": "#e3e3fd",
        "blue-france-850": "#cacafb",
        "blue-france-625": "#8585f6",
        "blue-france-200": "#313178",
        "blue-france-125": "#272747",
        "blue-france-100": "#21213f",
        "blue-france-75": "#1b1b35",
        "red-marianne-main-472": "#e1000f",
        "red-marianne-425": "#c9191e",
        "red-marianne-975": "#fef4f4",
        "red-marianne-950": "#fee9e9",
        "red-marianne-925": "#fddede",
        "red-marianne-850": "#fcbfbf",
        "red-marianne-625": "#f95c5e",
        "red-marianne-200": "#5e2a2b",
        "red-marianne-125": "#3b2424",
        "red-marianne-100": "#331f1f",
        "red-marianne-75": "#2b1919",
        "success-main-525": "#1f8d49",
        "success-425": "#18753c",
        "success-975": "#dffee6",
        "success-950": "#b8fec9",
        "success-925": "#88fdaa",
        "success-850": "#3bea7e",
        "success-625": "#27a658",
        "success-200": "#204129",
        "success-125": "#1e2e22",
        "success-100": "#19271d",
        "success-75": "#142117",
        "warning-main-525": "#d64d00",
        "warning-425": "#b34000",
        "warning-975": "#fff4f3",
        "warning-950": "#ffe9e6",
        "warning-925": "#ffded9",
        "warning-850": "warning-850",
      },
    },
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
