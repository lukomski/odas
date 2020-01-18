<template>
  <div>
  <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand>ODAS</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        
        <b-nav-form>
          <b-form-input size="sm" class="mr-sm-2" v-model="username_input" placeholder="Użytkownik"></b-form-input>
          <b-button size="sm" v-b-toggle.nav-collapse class="my-2 my-sm-0" @click="searchUser()">Szukaj</b-button>
        </b-nav-form>
 
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
        <b-nav-item :to="{ name: 'Home' }" v-if="this.isLogged">Moja strona</b-nav-item>
        <b-nav-item :to="{ name: 'Register' }" v-if="!this.isLogged">Zarejestruj się</b-nav-item>
        <b-nav-item :to="{ name: 'Login' }" v-if="!this.isLogged">Zaloguj się</b-nav-item>
        <b-nav-item :to="{ name: 'ChangePassword' }" v-if="this.isLogged">Zmień hasło</b-nav-item>
        <b-nav-item v-if="this.isLogged" @click="logout()">Wyloguj się</b-nav-item>
      </b-navbar-nav>
    </b-collapse>
  </b-navbar>
</div>
</template>

<script>
export default {
  name: 'About',
  data: function () {
    return {
      username_input: ''
    }
  },
  computed: {
    isLogged: function () {
      return this.$store.state.isLogged
    },
    username () {
      return this.$store.state.username
    }
  },
  methods: {
    logout: function () {
      this.$session.remove("username")
      this.$cookie.delete('session_id')
      this.$store.dispatch('logOut')
    },
    searchUser: function () {
      // get check if user exists
      let new_route = '/user/' + this.username_input
      if (window.location.pathname != new_route) {
        this.$router.push(new_route).catch()
      }
      
      // if exists open page /user/<username>
    },
    goToHomePage: function () {
      if (this.isLogged) {
        let new_route = '/user/' + this.username_input
        if (window.location.pathname != new_route) {
          this.$router.push(new_route).catch()
        }
      } else {
        let new_route = '/login'
        if (window.location.pathname != new_route) {
          this.$router.push(new_route).catch()
        }
      }
      
    }
  }
}
</script>
<style>
</style>