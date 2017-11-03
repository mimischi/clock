var path = require('path');
var webpack = require('webpack');
const merge = require('webpack-merge');
const UglifyJSPlugin = require('uglifyjs-webpack-plugin');
var BundleTracker = require('webpack-bundle-tracker');
const common = require('./webpack.common.js');

module.exports = merge(common, {
  devtool: 'source-map',
  output: {
    path: path.resolve('./assets/assets/'),
    filename: "[name]-[hash].js",
    publicPath: '/static/dist/'
  },
  plugins: [
    new UglifyJSPlugin({
      sourceMap: true
    }),

    // removes a lot of debugging code in React
    new webpack.DefinePlugin({
      'process.env': {
        'NODE_ENV': JSON.stringify('production')
      }}),

    new BundleTracker({filename: './webpack-stats-prod.json'}),

    // keeps hashes consistent between compilations
    new webpack.optimize.OccurrenceOrderPlugin(),

    // minifies your code
    new webpack.optimize.UglifyJsPlugin({
      compressor: {
        warnings: false
      }
    })
  ]
});
