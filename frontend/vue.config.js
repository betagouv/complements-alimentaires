const { defineConfig } = require("@vue/cli-service");
const BundleTracker = require("webpack-bundle-tracker");
const debug = !process.env.DEBUG || process.env.DEBUG === "True";
const publicPath = debug ? "http://127.0.0.1:8080/" : "/static/";

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
    config.optimization.splitChunks(false);

    config
      .plugin("BundleTracker")
      .use(BundleTracker, [
        { path: "../frontend/", filename: "webpack-stats.json" },
      ]);

    config.resolve.alias.set("__STATIC__", "static");

    config.devServer
      .host("127.0.0.1")
      .port(8080)
      .hot(true)
      .https(false)
      // eslint-disable-next-line no-useless-escape
      .headers({ "Access-Control-Allow-Origin": ["*"] });
  },
});
