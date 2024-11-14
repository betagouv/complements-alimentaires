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
    extract: false,
  },
  chainWebpack: (config) => {
    config.optimization.splitChunks(false)

    config.plugin("BundleTracker").use(BundleTracker)

    config.resolve.alias.set("__STATIC__", "static")

    config.devServer
      .host("0.0.0.0")
      .port(8080)
      .hot(true)
      .https(false)
      // eslint-disable-next-line no-useless-escape
      .headers({ "Access-Control-Allow-Origin": ["*"] })
  },
})
