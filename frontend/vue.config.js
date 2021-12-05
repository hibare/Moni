module.exports = {
  transpileDependencies: [
    'vuetify'
  ],

  devServer: {
    proxy: {
      '^/api': {
        target: 'http://127.0.0.1:5000',
      },
    }
  },

  outputDir: './dist',

  assetsDir: 'static',
}
