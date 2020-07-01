import colors from 'vuetify/es5/util/colors';
import fs from 'fs';
import path from 'path';

const environment = process.env.NODE_ENV
const envSet = require(`./env.${environment}.js`)

export default {
  env: envSet,

  axios: {proxy: true},
  proxy: {
    "/getImage": envSet.apiUrl,
    "/list": envSet.apiUrl,
    "/image": envSet.apiUrl,
  },

  mode: 'universal',
  /*
  ** Nuxt target
  ** See https://nuxtjs.org/api/configuration-target
  */
  target: 'server',
  /*
  ** Headers of the page
  ** See https://nuxtjs.org/api/configuration-head
  */
  head: {
    titleTemplate: '%s - ' + process.env.npm_package_name,
    title: process.env.npm_package_name || '',
    meta: [
      {charset: 'utf-8'},
      {name: 'viewport', content: 'width=device-width, initial-scale=1'},
      {
        hid: 'description',
        name: 'description',
        content: process.env.npm_package_description || ''
      }
    ],
    link: [
      {rel: 'icon', type: 'image/x-icon', href: '/favicon.png'},
      {
        rel: 'stylesheet',
        href: 'https://fonts.googleapis.com/css?family=Heebo:600,800&display=swap'
      }
    ]
  },
  /*
  ** Global CSS
  */
  css: [
    '~/assets/scss/style.scss',
  ],
  /*
  ** Plugins to load before mounting the App
  ** https://nuxtjs.org/guide/plugins
  */
  plugins: [],
  /*
  ** Auto import components
  ** See https://nuxtjs.org/api/configuration-components
  */
  components: true,
  /*
  ** Nuxt.js dev-modules
  */
  buildModules: [
    '@nuxtjs/vuetify',
  ],
  /*
  ** Nuxt.js modules
  */
  modules: [
    '@nuxtjs/style-resources',
    '@nuxtjs/axios',
  ],
  styleResources: {
    scss: [
      '~assets/scss/style.scss'
    ]
  },
  devModules: ['@nuxtjs/vuetify'],
  vuetify: {
    customVariables: ['~/assets/scss/vuetify_variables.scss'],
    treeShake: true,
    theme: {
      dark: false,
      themes: {
        dark: {
          primary: colors.blue.darken2,
          accent: colors.grey.darken3,
          secondary: colors.amber.darken3,
          info: colors.teal.lighten1,
          warning: colors.amber.base,
          error: colors.deepOrange.accent4,
          success: colors.green.accent3
        }
      },
      defaultAssets: false
    },
  },
  /*
  ** Build configuration
  ** See https://nuxtjs.org/api/configuration-build/
  */
  build: {},
  server: {
    port: 8000,
    host: '0.0.0.0',
    https: {
      key: fs.readFileSync(
          path.resolve(
              __dirname,
              'server/localhost-key.pem'
          )
      ),
      cert: fs.readFileSync(
          path.resolve(__dirname, 'server/localhost.pem')
      )
    }
  }
}
