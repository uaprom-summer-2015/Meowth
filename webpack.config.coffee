path = require 'path'
webpack = require 'webpack'
{keys} = require 'lodash'
pkginfo = require "./package.json"
ExtractTextPlugin = require 'extract-text-webpack-plugin'
StatsPlugin = require 'stats-webpack-plugin'
isProduction = process.env.NODE_ENV == 'production';

aliases =
  jquery: "npm-zepto"
  ckeditor: path.join __dirname, 'project', 'frontend', "./vendor/ckeditor.js"

module.exports =
  context: path.join __dirname, 'project', 'frontend'
  cache: true

  entry:
    main: "./scripts/main.js"
    vacancies: "./scripts/vacancies.js"
    vacancy: "./scripts/vacancy.js"
    contacts: "./scripts/contacts.js"
    hamburger: "./scripts/hamburger.js"
    offercv: "./scripts/offer_cv.js"
    admin_vacancies: "./scripts/admin.vacancies.js"
    admin_vacancy: "./scripts/admin.vacancy.js"
    admin_page: "./scripts/admin.page.js"
    admin_pageblock: "./scripts/admin.pageblock.js"
    admin_pagechunk: "./scripts/admin.pagechunk.js"
    admin_mailtemplate: "./scripts/admin.mailtemplate.js"
#    ckeditor: "./vendor/ckeditor.js"
    client: "./client.js"
    admin: "./admin.js"
    vendor: Array::concat ['jquery'], keys(pkginfo.dependencies)

  output:
    path: path.join __dirname, 'static'
    publicPath: '/static/'
    filename: if isProduction then '[name].[hash].bundle.js' else '[name].trunk.bundle.js'

  module:
    loaders: [
#      {test: /ckeditor\/(?!ckeditor\.js)/, loader: 'file?name=[path][name].[ext]'}
      {test: /\.coffee$/, loader: 'coffee-loader'}
      {test: /\.css$/, exclude: /ckeditor/, loader: ExtractTextPlugin.extract("style-loader", "css-loader")}
      {test: /\.less$/, loader: ExtractTextPlugin.extract("style-loader", "css-loader!less-loader")}
      {test: /\.(sass|scss)$/, loader: ExtractTextPlugin.extract("style-loader", "css-loader!scss-loader")}
      {test: /\.styl$/, loader: ExtractTextPlugin.extract("style-loader", "css-loader!stylus-loader")}
      {test: /\.(woff|woff2|eot|ttf)$/, exclude: /ckeditor/, loaders: if isProduction then ['file?name=font/[hash:4].[ext]'] else ['file?name=font/[name].[ext]']}
      {
        test: /.*\.(gif|png|jpg|jpeg|svg)$/,
        exclude: /ckeditor/,
        loaders: Array::concat(
          if isProduction then ['file?name=img/[hash:4].[ext]'] else ['file?name=img/[name].[ext]']
          if isProduction then ['image-webpack?optimizationLevel=7&interlaced=false'] else []
        )
      }
    ]

  resolve:
    alias: aliases
    extensions: ['', '.coffee', '.js', '.styl', '.css']
    modulesDirectories: ['node_modules', 'scripts']

  plugins: Array::concat(
    if isProduction then [
      new webpack.optimize.UglifyJsPlugin({compress:false})
      new StatsPlugin 'stats.json', modules: false, chunks: false, assets: false, version: false, errorDetails: false
    ] else []
    [
      new ExtractTextPlugin if isProduction then "[name].[hash].css" else "[name].trunk.css"
      new webpack.optimize.CommonsChunkPlugin name: 'vendor', minChunks: Infinity
    ]
  )
