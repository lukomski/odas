import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router ({
  mode:'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('@/components/Home'),
      meta: { 
        requiresAuth: true,
        title: "Dashboard"
      }
    },
    {
      path: '/about',
      name: 'About',
      component: () => import('@/pages/About'),
      meta: { 
        requiresAuth: true,
        title: "About"
      }
    },
    {
      path: '/login',
      name: 'Login',
      component: () => import('@/components/Login')
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/components/Register')
    }
  ]
})