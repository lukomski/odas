<template>
 <div>
<NavigationBar/>
<br>
 <div class="d-flex justify-content-center">
  <div class="col-md-4 ">
    <b-form @submit="onSubmit" @reset="onReset" v-if="show">
      <b-form-group
        id="input-group-1"
        label="Login"
        label-for="input-1"
      >
        <b-form-input
          id="input-1"
          v-model="form.login"
          required
          placeholder=""
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-2" label="Hasło" label-for="input-2">
        <b-form-input
          id="input-2"
          v-model="form.password"
          required
          placeholder=""
          type="password"
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-2" label="Powtórz hasło" label-for="input-2">
        <b-form-input
          id="input-2"
          v-model="form.repeatPassword"
          required
          placeholder=""
          type="password"
        ></b-form-input>
      </b-form-group>

      <b-button type="submit" variant="success">Zarejestruj</b-button>
    </b-form>
  </div>
  </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import NavigationBar from './NavigationBar'
  export default {
    data() {
      return {
        form: {
          login: '',
          password: '',
          repeatPassword: '',
        },
        show: true
      }
    },
    methods: {
      onSubmit(evt) {
        evt.preventDefault()

        axios.get('http://localhost:5000/api/adduser', {
          params: {
            username: this.form.login,
            password: this.form.password
          } ,
        })
        .then(response => {
          let message = response.data.message
          if (response.data.status) {
            alert("OK: " + message)
          } else {
            alert("ER: " + message)
          }
        })
        .catch(e => {
            alert(e)  
        })
      },
    },
    components: {
     'NavigationBar' : NavigationBar
    }
  }
</script>