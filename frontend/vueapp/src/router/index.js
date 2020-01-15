import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router ({
  mode:'history',
  routes: [
    {
      path: '/',
      name: 'Home',
      component: () => import('@/components/Home/Home'),
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
      replace: true,
      component: () => import('@/components/Login')
    },
    {
      path: '/changepassword',
      name: 'ChangePassword',
      component: () => import('@/components/ChangePassword')
    },
    {
      path: '/register',
      name: 'Register',
      component: () => import('@/components/Register')
    }
  ],
})