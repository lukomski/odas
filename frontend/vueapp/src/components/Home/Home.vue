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
						:ownerMode=true
						:viewers=[]
						v-on:reloadNotes="loadNotes()"
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
							:note_hash="note.id"
							:note_public="note.public"
							:inserMode=false
							:ownerMode=true
							v-on:updated="loadNote(note.id)"
							v-on:deleted="deleteNote(note.id)"
							v-on:reloadNotes="loadNotes()"
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
import config from '@/store/config'

export default {
	data: function() {
		return {
			name: 'Home',			
			priv_files: [],
			upload_file: "",
			isOwner: true,
			pub_files: [],
			notes: []
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
		loadNotes: function () {
			console.log("loadNotes")
			axios.get(config.api + '/api/notes', null, {
				params: {
				}
			})
			.then(response => {
				console.log(response.data)
				let message = response.data.message
				if (response.data.success) {
					let notes = response.data.notes
					console.log(notes)
					let new_notes = []
					for (var i=0; i < notes.length; i++) {
						let v = {
							"title" : notes[i].title,
							"author" : "Obserwatorzy", // to refactor
							"message" : notes[i].message,
							"viewers" : notes[i].viewers,
							"public" : notes[i].public,
							"id" : notes[i].id
						}
						new_notes.push(v)
					}
					this.notes = new_notes
				} else {
				}
			})
			.catch(e => {
				alert(e)  
			})
		},
		loadNote: function (note_hash) {
			console.log("loadNotes")
			axios.get(config.api + '/api/notes/' + note_hash, null, {
				params: {
				}
			})
			.then(response => {
				console.log(response.data)
				let message = response.data.message
				if (response.data.success) {
					// get note with note_hash
					let it = undefined
					for (var i=0; i<this.notes.length; i++) {
						if (this.notes[i].id == note_hash) {
							it = i
							break
						}
					}
					if (it == undefined) {
						console.log("note "+ note_hash + " not found in notes")
						return
					}
					let v = {
						"title" : response.data.note.title,
						"author" : "Obserwatorzy", // to refactor
						"message" : response.data.note.message,
						"viewers" : response.data.note.viewers,
						"public" : response.data.note.public,
						"id" : response.data.note.id
					}

					let new_notes = []
					for (var i=0; i<this.notes.length; i++) {
						if (this.notes[i].id == note_hash) {
							new_notes.push(v)
						} else {
							new_notes.push(this.notes[i])
						}
					}
					this.notes = new_notes
				} else {
				}
			})
			.catch(e => {
				alert(e)  
			})
		},
		deleteNote: function (note_hash) {
			let new_notes = []
			for (var i=0; i<this.notes.length; i++) {
				if (this.notes[i].id != note_hash) {
					new_notes.push(this.notes[i])
				}
			}
			this.notes = new_notes
		},
	},
	watch: {
		isLogged: function (val) {
			if (this.isLogged) {
				this.loadNotes()
			} else {
				//this.$router.push('/login').catch()
			}
		}
	},
	mounted: function () {
		console.log("mouted in Home")
		if (this.isLogged) {
			this.loadNotes()
		} else {
			//this.$router.push('/login').catch()
		}
	},
	components: {
		'FileDelegate': FileDelegate,
		'Card' : Card
	}
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