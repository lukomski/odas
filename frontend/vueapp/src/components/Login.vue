<template>
 <div>
<br>
 <div class="d-flex justify-content-center">
  <div class="col-md-4">
    <b-form v-if="show">
      <b-form-group
        id="input-group-1"
        label="Login"
        label-for="input-1"
      >
        <b-form-input
          id="loginInput"
          v-model="form.login"
          required
          placeholder=""
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-2" label="Hasło" label-for="input-2">
        <b-form-input
          id="passwordInput"
          v-model="form.password"
          required
          placeholder=""
          type="password"
        ></b-form-input>
      </b-form-group>

      <b-button type="button" v-on:click="onSubmit()" variant="success">Zaloguj</b-button>
    </b-form>
  </div>
  </div>
  </div>
</template>

<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script>window.jQuery || document.write('<script src="{{ url_for('static', filename='jquery.js') }}">\x3C/script>')</script>

<script>
  import axios from 'axios';
  import config from '@/store/config'
  export default {
    data() {
      return {
        form: {
          login: '',
          password: ''
        },
        show: true
      }
    },
    methods: {
      onSubmit(evt) {
        //evt.preventDefault()
       //console.log(evt)
        axios.post(config.api + '/api/user', null, {
          params: {
            username: this.form.login,
            password: this.form.password
          } ,
        })
        .then(response => {
          console.log(response.data)
          let message = response.data.message
          if (response.data.success) {
            this.$session.set("username",response.data.username) // in case of reload page
            this.$cookie.set('session_id', response.data.session_id);
            
            this.$store.dispatch('logIn')
            this.$store.dispatch('setUsername', response.data.username)
            this.$router.push('/user/'+response.data.username).catch()
          } else {
            alert("ER: " + message)
          }
        })
        .catch(e => {
            alert(e)  
        })
      }
    }
  }
</script>