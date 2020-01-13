<template>
  <div>
  <b-navbar toggleable="lg" type="dark" variant="dark">
    <b-navbar-brand href="#">ODAS</b-navbar-brand>

    <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

    <b-collapse id="nav-collapse" is-nav>
      <b-navbar-nav>
        <b-nav-item :to="{ name: 'Home' }" v-if="this.isLogged">Strona główna</b-nav-item>
      </b-navbar-nav>

      <!-- Right aligned nav items -->
      <b-navbar-nav class="ml-auto">
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
  computed: {
    isLogged: function () {
      return this.$store.state.isLogged
    }
  },
  methods: {
    logout: function () {
      this.$session.remove("username")
      this.$cookie.delete('session_id')
      this.$store.dispatch('logOut')
    }
  }
}
</script>
<style>
</style>