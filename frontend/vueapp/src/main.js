import Vue from 'vue'
import App from './App.vue'
import PageNotFound from './pages/404.vue'
import Home from './pages/Home.vue'
import About from './pages/About.vue'
import Login from '@/components/Login.vue'
import Register from '@/components/Register.vue'

import { BootstrapVue, IconsPlugin } from 'bootstrap-vue'
// app.js
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

// Install BootstrapVue
Vue.use(BootstrapVue)
// Optionally install the BootstrapVue icon components plugin
Vue.use(IconsPlugin)

const routes = {
  '/': Home,
  '/about': About,
  '/app' : App,
  '/login' : Login,
  '/register' : Register
}

new Vue({
  el: '#app',
  data: {
    currentRoute: window.location.pathname
  },
  computed: {
    ViewComponent () {
      return routes[this.currentRoute] || PageNotFound
    }
  },
  render (h) { 
    return h(this.ViewComponent) 
  },
  methods: {
    changedRoute(route) {
      alert("whitam w mainie" + route);
      this.currentRoute = route
    }
  }
})