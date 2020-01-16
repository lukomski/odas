<template>
	<div id="app">
		<NavigationBar/>
		<router-view></router-view>
	</div>
</template>

<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script>window.jQuery || document.write('<script src="{{ url_for('static', filename='jquery.js') }}">\x3C/script>')</script>

<script>
import NavigationBar from '@/components/NavigationBar'
	import axios from 'axios';
	export default {
		name: 'app',
		components: {
			'NavigationBar': NavigationBar
		},
		computed: {
			isLogged () {
				return this.$store.state.isLogged
			},
		},
		watch: {
			isLogged: function (val) {
				let session_id = this.$cookie.get('session_id')
				if (session_id != undefined) {
				//	this.$store.dispatch('logIn')
				} else {
					this.$router.push('/login')
				}
			}
		},
		methods: {
			test: function () {
				console.log("App mouted")
			},
			askServerAboutBasics: function (session_id) {
				axios.get('http://localhost:5000/api/user',{
					withCredentials: true
				})
				.then(response => {
					console.log("YYY:")
					console.log(response.data)
					let message = response.data.message
					if (response.data.success) {
						this.$store.dispatch('setUsername', response.data.username)
						this.$store.dispatch('logIn')
					} else {
						this.$router.push('/login').catch()
					}
				})
				.catch(e => {
					alert(e)  
				})
			}
		},
		mounted: function () {
			// check cookies and login state
			let session_id = this.$cookie.get('session_id')
			if (session_id != undefined) {
				this.askServerAboutBasics(session_id)
				// this.$store.dispatch('setUsername', this.$session.get("username"))
				// this.$store.dispatch('logIn')
			} else {
				this.$router.push('/login').catch()
				// console.log(this.$router.history.current.name == 'Login')

				// console.log(this.$router.history.current)
				// if (this.$router.history.current.path == '/') {

					//this.$router.go('/login') // go redirect whithout saving to history
				// }
			}
			
			console.log("App mouted = " )
			
		}
	}
</script>

<style></style>
