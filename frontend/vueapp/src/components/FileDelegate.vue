<template>

	<li class="list-group-item d-flex justify-content-between align-items-center">
		<a class="fileReferences" @click="download" target=”_blank”>{{file.name}}</a>
		<button class="btn btn-outline-success" @click="download">Pobierz</button>
		<button class="btn btn-outline-danger" @click="remove">Usun</button>
	</li>

</template>

<script>
	import axios from 'axios'
	axios.defaults.withCredentials = true

	export default {
		props: ["file", "isPublic"],
		methods: {
			download: function () {
				if (this.isPublic) {
					this.$emit('download',this.file)
				//	this.downloadPubFile(this.file.name)
				}
				else {
					alert("not public TODO")
				}
			},
			remove: function () {
				alert("should remove " + this.file.name)
			},
			downloadPubFile: function (filename) {
				axios.get('http://localhost:5000/api/files/' + this.username + '/pub/' + filename
				).then(response => {
					let message = response.data.message
					if (response.data.success) {
						alert("OK: " + message)
					} else {
						alert("ER: " + message)
					}
				}).catch(e => {
					// page not found
					alert("Nieznany pub użytkownik " + this.username + " e = " + e)
					//alert(e.response)  
				})
			}
		}
	}

</script>

<style>
	
</style>