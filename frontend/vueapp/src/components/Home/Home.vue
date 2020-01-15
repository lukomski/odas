<template>
	<div>
		<h1 id="title" v-if="this.isLogged">Użytkownik {{ this.username }}</h1>
		<h1 id="title" v-if="!this.isLogged">Strona użytkownika {{ this.username }}</h1>
		<div class="container-fluid" v-if="this.isLogged">
			<div class="row">
				<div class="col-md-6 panel">
					<br>
					<h1 id="title">Program do przechowywania notatek</h1>
					<br>
					<div class="h1 mb-0" id="imageDiv">
						<b-icon-book variant="warning" font-scale="7.5"/>
					</div>
					
				</div>
				<div class="col-md-6 panel">
					<br>
					<Card
						:insertMode=true
						:viewers=[]
					/>
				</div>
			</div>
		</div>
		<br>
		<div class="container-fluid">
			<div class="d-flex justify-content-center">
				<div class="col-md-8 panel">
					<h1>Dostępne notatki</h1><br>
					<ul class="list-group col-md-12">
						<Card 
							v-for="note in notes"
							:title="note.title"
							:key="note.id"
							:subtitle="note.author" 
							:message="note.message"
							:viewers="note.viewers"
							:inserMode=false
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

import FileDelegate from "@/components/Home/FileDelegate"
import Card from "@/components/Home/Card"

export default {
	data: function() {
		return {
			name: 'Home',			
			priv_files: [],
			upload_file: "",
			isOwner: true,
			pub_files: [],
			notes: [
				{
					'title': '"NYT": W ukraiński samolot uderzyły dwa pociski. Nowe nagranie',
					'author': 'Obserwatorzy',
					'message': 'Tuż po katastrofie pojawiły się spekulacje, że samolot mógł zostać zestrzelony przez Iran, ponieważ w tym czasie Teheran przeprowadzał atak na amerykańskie bazy w Iraku. Początkowo Iran odpierał zarzuty, jednak w sobotę ogłosił, że do zestrzelenia faktycznie doszło. "Z powodu błędu ludzkiego, w Czytaj więcej na https://fakty.interia.pl/raporty/raport-bliski-wschod/aktualnosci/news-nyt-w-ukrainski-samolot-uderzyly-dwa-pociski-nowe-nagranie,nId,4260996#utm_source=paste&utm_medium=paste&utm_campaign=chrome"',
					'viewers': [
						{ 'name': 'Adam', 'id': 0},
						{ 'name': 'Jacek', 'id': 1},
						{ 'name': 'Michał', 'id': 2}
						],
					'id': "0"
				},
				{
					'title': 'Interwencja w Nowym Czarnowie. Areszt dla drugiego policjanta',
					'author': 'Obserwatorzy',
					'message': 'Dwa miesiące w areszcie spędzi policjant, który usłyszał zarzut przekroczenia uprawnień podczas interwencji w Nowym Czarnowie - poinformowała we wtorek prokuratura. Wcześniej sąd zdecydował o tymczasowym aresztowaniu innego policjanta z patrolu, który miał niewłaściwie użyć siły wobec mieszkańca Gryfina.',
					'viewers': [
						{'name': 'Łysy', 'id': 0},
						{'name': 'Biały', 'id': 1}
						],
					'id': "1"
				}
			]
		}
	},
	computed: {
		isLogged () {
			return this.$store.state.isLogged
		},
		username () {
			return this.$store.state.username
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
				console.log("response = " + response)
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
			axios.get('http://localhost:5000/api/files/' + this.username + '/pub/' + file.name, 
			{
				responseType: 'blob'
			}
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
			axios.get('http://localhost:5000/api/files/' + this.username + '/priv/' + file.name,
			{
				responseType: 'blob',
				headers: {
					'Accept': 'application/vnd.ms-excel'
				}
			}
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
		deletePubFile: function (file) {
			axios.delete('http://localhost:5000/api/files/' + this.username + '/pub/' + file.name
			).then(response => {
				if (response.data.success) {
					console.log("OK PUB: " + response.data.message)
					this.loadPubData()
				} else {
					console.log("ER: " + response.data.message)
				}
			}).catch(e => {
				alert("CRITICAL: " + e)
			})
		},
		deletePrivFile: function (file) {
			axios.delete('http://localhost:5000/api/files/' + this.username + '/priv/' + file.name
			).then(response => {
				if (response.data.success) {
					console.log("OK PRIV: " + response.data.message)
					this.loadPrivData()
				} else {
					console.log("ER: " + response.data.message)
				}
			}).catch(e => {
				alert("CRITICAL: " + e)
			})
		},
		buyTv: function () {
			// Dispatch the action to buy a TV
			if (this.isLogged) {
				this.$store.dispatch('logOut')
			} else {
				this.$store.dispatch('logIn')
			}
		}
	},
	watch: {
		isLogged: function (val) {
			if (this.isLogged) {
				this.loadPubData()
				this.loadPrivData()
			}
		}
	},
	mounted: function () {
		console.log("mouted in Home")
		if (this.isLogged) {
			this.loadPubData()
			this.loadPrivData()
		} else {
			this.$router.push('/login').catch()
		}
	},
	components: {
		'FileDelegate': FileDelegate,
		'Card' : Card
	}
}

function uploadPubFilee() {
	
}

</script>


<style>
a.fileReferences {
	width: 60%;
}
#title, #imageDiv {
	text-align: center;
}
</style>