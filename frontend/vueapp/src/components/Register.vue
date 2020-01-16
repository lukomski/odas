<template>
 <div>
<br>
 <div class="d-flex justify-content-center">
  <div class="col-md-4 ">
    <b-form @submit="onSubmit"  v-if="show">
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
          id="input-password"
          v-model="form.password"
          required
          placeholder=""
          type="password"
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-2" label="Powtórz hasło" label-for="input-2">
        <b-form-input
          id="input-repeat-password"
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

<!-- Need to console.log works -->
<script src="//unpkg.com/vue@latest/dist/vue.min.js"/>

<script>
  import axios from 'axios';
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

        axios.post('http://localhost:5000/api/users', null, {
          params: {
            username: this.form.login,
            password: this.form.password
          } ,
        })
        .then(response => {
          console.log(response.data)
          let message = response.data.message
          if (response.data.status) {
          } else {
          }
        })
        .catch(e => {
            alert(e)  
        })
      },
    }
  }
</script>