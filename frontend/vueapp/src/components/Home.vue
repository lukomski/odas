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

						<FileDelegate 
							v-for="file in pub_files"
							v-bind:file = "file"
							v-bind:isPublic = true
							v-bind:key="file.name" 
							v-on:download="downloadPubFile"
							class="list-group-item d-flex justify-content-between align-items-center"
						/>

					</ul>
				</div>

				<div v-if="isOwner" class="col-md-6 panel">
				<h1>Pliki prywatne</h1><br>
					<ul class="list-group col-md-12">


						<FileDelegate 
							v-for="file in priv_files"
							v-bind:file = "file"
							v-bind:isPublic = true
							v-bind:key="file.name" 
							v-on:download="downloadPrivFile"
							class="list-group-item d-flex justify-content-between align-items-center"
						/>

					</ul>
				</div>
			</div>
		</div>

	</div>

</template>

<script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<script>window.jQuery || document.write('<script src="{{ url_for('static', filename='jquery.js') }}">\x3C/script>')</script>

<script>

import axios from 'axios'
axios.defaults.withCredentials = true

import FileDelegate from "@/components/FileDelegate"

export default {
	data: function() {
		return {
			name: 'Home',
			username: "test",
			
			priv_files: [
				{ name: "privfile"}
			],
			upload_file: "",
			isOwner: true,
			pub_files: [
				{ name: "pubfile"}
			]
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
			form
			).then(response => {
				let message = response.data.message
				if (response.data.success) {
					//alert("OK: " + message)
					this.loadPubData()
				} else {
					alert("ER: " + message)
				}
			}).catch(e => {
				alert(e)  
			})
		},
		uploadPrivFile() {
			let file = document.getElementById("fileInput").files[0]
			if (file == undefined) {
				alert("wybierz plik do wysłania")
				return
			}
			this.upload_file = file
			let form = new FormData()
			form.append("file", this.upload_file)

			axios.post('http://localhost:5000/api/files/' + this.username + '/priv/' + file.name, 
			form
			).then(response => {
				let message = response.data.message
				if (response.data.success) {
					//alert("OK: " + message)
					this.loadPrivData()
				} else {
					alert("ER: " + message)
				}
			}).catch(e => {
				alert(e)  
			})
			
		},
		loadPubData: function () {
			// load public files
			let self = this
			axios.get('http://localhost:5000/api/files/' + this.username + '/pub'
				).then(response => {
					let message = response.data.message
					if (response.data.success) {
						let list = []
						for (let file of response.data.files) {
							list.push({"name":file})		
						}
						this.pub_files = list
					} else {
						console.log("ER: " + message)
					}
				}).catch(e => {
					// page not found
					alert("Nieznany pub użytkownik " + this.username)
					//alert(e.response)  
				})
			
		},
		loadPrivData: function () {
			//load private files
			axios.get('http://localhost:5000/api/files/' + this.username + '/priv'
			).then(response => {
				let message = response.data.message
				if (response.data.success) {
					//this.priv_files = []
					let list = []
					console.log("OK PRIV: " + message + response.data.files)
					for (let file of response.data.files) {
						list.push({"name":file})
					}
					this.priv_files = list
				} else {
					console.log("ER: " + message)
				}
			}).catch(e => {
				// page not found
				alert("CRITICAL: " + e)
				//alert(e.response)  
			})
		},
		downloadPubFile: function (file) {
			axios.get('http://localhost:5000/api/files/' + this.username + '/pub/' + file.name
			).then(response => {
				let downloadedfile = response.data
				const url = window.URL.createObjectURL(new Blob([downloadedfile]));
				const link = document.createElement('a');
				link.href = url;
				link.setAttribute('download', file.name);
				document.body.appendChild(link);
				link.click();
			}).catch(e => {
				alert("CRITICAL: " + e)
			})
		},
		downloadPrivFile: function (file) {
			axios.get('http://localhost:5000/api/files/' + this.username + '/priv/' + file.name
			).then(response => {
				let downloadedfile = response.data
				const url = window.URL.createObjectURL(new Blob([downloadedfile]));
				const link = document.createElement('a');
				link.href = url;
				link.setAttribute('download', file.name);
				document.body.appendChild(link);
				link.click();
			}).catch(e => {
				alert("CRITICAL: " + e)
			})
		}	
	},
	mounted: function () {
		this.loadPubData()
		this.loadPrivData()
	},
	components: {
		'FileDelegate': FileDelegate
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