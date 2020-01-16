<template>
<div>
    <br>
    <div class="d-flex justify-content-center">
      <div class="col-md-4 ">
        <b-form @submit="onSubmit">
      <b-form-group id="input-group-1" label="Obecne hasło" label-for="input-1">
        <b-form-input
          id="input-1"
          v-model="form.oldPassword"
          required
          placeholder=""
          type="password"
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-2" label="Nowe hasło" label-for="input-2">
        <b-form-input
          id="input-password"
          v-model="form.password"
          required
          placeholder=""
          type="password"
        ></b-form-input>
      </b-form-group>

      <b-form-group id="input-group-2" label="Powtórz nowe hasło" label-for="input-2">
        <b-form-input
          id="input-repeat-password"
          v-model="form.repeatPassword"
          required
          placeholder=""
          type="password"
        ></b-form-input>
      </b-form-group>

      <b-button type="submit" variant="success">Zmień hasło</b-button>
    </b-form>
  </div>
  </div>
  </div>
</template>

<!-- Need to console.log works -->
<script src="//unpkg.com/vue@latest/dist/vue.min.js"/>

<script>
  import axios from 'axios'
  axios.defaults.withCredentials = true

  export default {
    data() {
      return {
        form: {
          oldPassword: '',
          password: '',
          repeatPassword: '',
        },
        show: true
      }
    },
    computed: {
      username () {
        return this.$store.state.username
      }
    },
    methods: {
      onSubmit(evt) {
        evt.preventDefault()
        if (this.form.password != this.form.repeatPassword) {
          alert("Hasła nie są takie same")
          return
        }

        axios.put('http://localhost:5000/api/users/' + this.username + "/password", null, {
          params: {
            old_password: this.form.oldPassword,
            password: this.form.password
          } ,
        })
        .then(response => {
          console.log(response.data)
          let message = response.data.message
          if (response.data.success) {
            alert("OK: " + message)
          } else {
            alert("ER: " + message)
          }
        })
        .catch(e => {
            alert(e)  
        })
      },
    }
  }
</script>