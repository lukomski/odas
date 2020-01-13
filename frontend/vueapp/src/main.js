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

import VueSession from 'vue-session'

Vue.use(VueSession)

import router from "./router";
import store from './store/store'

var VueCookie = require('vue-cookie');
// Tell Vue to use the plugin
Vue.use(VueCookie);

new Vue({
	router,
	store,
	render: h => h(App)
}).$mount("#app");

