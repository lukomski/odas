import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router ({
  routes: [
    {
      path: '/',
      name: 'HelloWorld',
      component: () => import('@/components/Login')
    },
    {
      path: '/home',
      name: 'Home',
      component: () => import('@/pages/Home')
    },
    {
      path: '/about',
      name: 'About',
      component: () => import('@/pages/About')
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