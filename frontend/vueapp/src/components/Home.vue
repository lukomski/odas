<template>
	<div>
		<h1 id="title">Witaj {{ username }}</h1>
		<div class="container-fluid">
			<div class="row">
				<div class="col-md-6 panel">
					<h1>Dodaj plik</h1>
					<br>
					<form method="POST" enctype="multipart/form-data" action="#">
						<div class="form-group">
							<input 
								type="file" 
								name="file" 
								class="form-control-file" 
								id="fileInput"
								>
						</div>
						<button type="button" class="btn btn-outline-success" v-on:click="uploadPubFile()">Dodaj plik publiczny</button>
						<button type="button" class="btn btn-outline-warning" v-on:click="uploadPrivFile()">Dodaj plik prywatny</button>
					</form>
				</div>
			</div>
		</div>
		<br>
		<div class="container-fluid">
			<div class="row">
				<div class="col-md-6 panel">
					<h1>Pliki publiczne</h1><br>
					<ul class="list-group col-md-12">
						
						<li v-for="file in pub_files" :key="file" class="list-group-item d-flex justify-content-between align-items-center">
							<a class="fileReferences" href="#" target=”_blank” >{{ file.name }}</a>
							<button class="btn btn-outline-success">Pobierz</button>
							<button class="btn btn-outline-danger">Usun</button>
						</li>

					</ul>
				</div>

				<div v-if="isOwner" class="col-md-6 panel">
				<h1>Pliki prywatne</h1><br>
					<ul class="list-group col-md-12">

						<li v-for="file in priv_files" :key="file" class="list-group-item d-flex justify-content-between align-items-center">
						<a class="fileReferences" href="#" target=”_blank” >{{ file.name }}</a>
						<button class="btn btn-outline-warning">Pobierz</button>
						<button class="btn btn-outline-danger" onclick="">Usuń</button>
						</li>

					</ul>
				</div>
			</div>
		</div>
		<p>Here is some information. This is the home page</p>
	</div>

</template>

<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
	<script>window.jQuery || document.write('<script src="{{ url_for('static', filename='jquery.js') }}">\x3C/script>')</script>
<script>
import axios from 'axios'
axios.defaults.withCredentials = true

export default {
	data() {
		return {
			name: 'Home',
			username: "Usersruser",
			pub_files: [
			{ name: "pubfile"}
			],
			priv_files: [
			{ name: "privfile"}
			],
			upload_file: "",
			isOwner: true
		}
	},
	methods: {
		uploadPubFile() {
			let file = document.getElementById("fileInput").files[0]
			if (file == undefined) {
				alert("wybierz plik do wysłania")
				return
			}
			this.upload_file = file
			let form = new FormData()
			form.append("file", this.upload_file)

			axios.post('http://localhost:5000/api/files/' + this.username + '/pub/' + file.name, 
			form)
			.then(response => {
				let message = response.data.message
				if (response.data.status) {
					alert("OK: " + message)
					this.$parent.currentRoute  = '/'
				} else {
					alert("ER: " + message)
				}
			})
			.catch(e => {
				alert(e)  
			})
		},
		uploadPrivFile() {
			alert("uploadPrivFile")
			//this.$session.set("some_key","some_value")
			alert("nisldkmcslkm")
			axios.get('http://localhost:5000/api/files/' + this.username + '/pub/' + file.name, {
				crossDomain: true
			}).then(res => { 
				console.log(res);
			}).catch(error => {
				console.log('error', error);
			})
			
		}
	}
}

function uploadPubFilee() {
	
}

</script>


<style>
a.fileReferences {
	width: 60%;
}
</style>