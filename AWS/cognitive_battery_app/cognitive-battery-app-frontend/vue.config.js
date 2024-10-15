const { defineConfig } = require('@vue/cli-service')

module.exports = {
  pluginOptions: {
    electronBuilder: {
      preload: 'src/preload.js',
      mainProcessFile: 'src/background.js',
      rendererProcessFile: 'src/main.js',
      externals: ['serialport'],
    }
  },
  chainWebpack: (config) => {
    // ... existing chainWebpack configurations

    // Add this block to transpile serialport
    config.module
      .rule('js')
      .include.add(/node_modules[\\/]serialport/)
      .end()
      .use('babel')
      .loader('babel-loader')
      .tap((options) => {
        // Modify options if necessary
        return options;
      });
  },
}

