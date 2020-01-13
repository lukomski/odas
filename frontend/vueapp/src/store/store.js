import Vuex from 'vuex'
import Vue from 'vue'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    isLogged: false,
    username:''
  },
  
  getters: {
    // Here we will create a getter
  },
  
  mutations: {
    logIn(state) {
      state.isLogged = true
    },
    logOut(state) {
      state.isLogged = false
    },
    setUsername(state, username) {
      state.username = username
    }
  },
  
  actions: {
    logIn: function (context) {
      if (!context.state.isLogged) {
        context.commit('logIn')
      }
    },
    logOut: function (context) {
      if (context.state.isLogged) {
        context.commit('logOut')
      }
    },
    setUsername: function (context, username) {
      context.commit('setUsername', username)
    }


  }
});