const { VueLoaderPlugin } = require('vue-loader')

var cssLoader = {
  loader: 'css-loader',
  options: {
    modules: true,
    localIdentName: '[local]_[hash:base64:8]'
  }
};

var rules = [
  {
    test: /\.ts$/,
    use: {
      loader: 'ts-loader',
      options: {
        appendTsSuffixTo: [/\.vue$/]
      }
    }
  },
  { test: /\.json$/, use: 'json-loader' },
  { test: /\.js$/, use: "source-map-loader" },
  { test: /\.css/, use: [
    "vue-style-loader",
    cssLoader
  ]},
  { test: /\.scss/, use: [
    "vue-style-loader",
    cssLoader,
    'sass-loader'
  ]},
  {
    test: /\.vue$/,
    use: 'vue-loader'
  },
];

let commonConfig = {
  entry: './index.ts',
  module: {
    rules: rules.slice(0)
  },
  devtool: 'source-map',
  externals: ['@jupyter-widgets/base'],
  resolve: {
    // Add '.ts' and '.tsx' as resolvable extensions.
    extensions: [".webpack.js", ".web.js", ".ts", ".js", ".vue"],
    alias: {
      vega: "vega-lib"
    }
  },
  plugins: [
    new VueLoaderPlugin()
  ]
}

module.exports = [
  // Notebook extension
  Object.assign({}, commonConfig,
    {
      output: {
        filename: 'index.js',
        path: __dirname + '/desdeo_vis/nbextension/static',
        libraryTarget: 'amd'
      },
    }
  ),

  // embeddable bundle (e.g. for docs)
  Object.assign({}, commonConfig,
    {
      output: {
          filename: 'embed-bundle.js',
          path: __dirname + '/docs/_static',
          library: "desdeo_vis",
          libraryTarget: 'amd'
      },
    }
  )
];
