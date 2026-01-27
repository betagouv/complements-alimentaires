const { defineConfig } = require("@vue/cli-service")
const BundleTracker = require("webpack-bundle-tracker")
const debug = !process.env.DEBUG || process.env.DEBUG === "True"
const FRONTEND_URL = "http://localhost:8080"
const publicPath = debug ? FRONTEND_URL : "/static/"

module.exports = defineConfig({
  transpileDependencies: true,
  runtimeCompiler: true,
  publicPath: publicPath,
  outputDir: "./dist/",
  configureWebpack: {
    devtool: "source-map",
  },

  css: {
    sourceMap: true,
    extract: true,
  },
  chainWebpack: (config) => {
    config.optimization.splitChunks(false)

    config.plugin("BundleTracker").use(BundleTracker)

    config.resolve.alias.set("__STATIC__", "static")

    // il faut specifier __VUE_PROD_HYDRATION_MISMATCH_DETAILS__ pour éviter un warning dans le console
    // https://vuejs.org/api/compile-time-flags#vue-cli
    config.plugin("define").tap((definitions) => {
      Object.assign(definitions[0], {
        __VUE_OPTIONS_API__: "true",
        __VUE_PROD_DEVTOOLS__: "false",
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: "false",
      })
      return definitions
    })

    config.devServer
      .host("0.0.0.0")
      .port(8080)
      .hot(true)
      .https(false)
      // eslint-disable-next-line no-useless-escape
      .headers({ "Access-Control-Allow-Origin": ["*"] })

    config.module
      .rule("vue")
      .use("vue-loader")
      .tap((options) => {
        options.compilerOptions = options.compilerOptions || {}
        options.compilerOptions.isCustomElement = (tag) => ["bar-chart"].includes(tag)
        return options
      })
  },
})
