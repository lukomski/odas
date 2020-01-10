import '@babel/polyfill'
import 'mutationobserver-shim'
import Vue from 'vue'
import './plugins/bootstrap-vue'
import App from './App.vue'


import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
// app.js
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

Vue.config.productionTip = false

// const routes = {
//   '/': Home,
//   '/about': About,
//   '/app' : App,
//   '/login' : Login,
//   '/register' : Register
// }
import VueSession from 'vue-session'

Vue.use(VueSession)

import router from "./router";


// new Vue({
//   el: '#app',
//   data: {
//     currentRoute: window.location.pathname
//   },
//   computed: {
//     ViewComponent () {
//       return routes[this.currentRoute] || PageNotFound
//     }
//   },
//   render (h) { 
//     return h(this.ViewComponent) 
//   },
//   methods: {
//     changedRoute(route) {
//       alert("whitam w mainie" + route);
//       this.currentRoute = route
//     }
//   }
// })

new Vue({
  router,
  render: h => h(App)
}).$mount("#app");

var VueCookie = require('vue-cookie');
// Tell Vue to use the plugin
Vue.use(VueCookie);