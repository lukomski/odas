<template>
	<div>
		<b-card>
			<b-card-title>
				<a v-if="!edit_title && !insertMode">
					{{ title }}
				</a>
				<b-form-input v-model="edit_title_input" placeholder="Tytuł notatki" v-if="edit_title_visible" :value="title"/>
				<a type="button" @click="startEditTitle()" class="h2 mb-0" v-if="title_pencil_visible">
					<b-icon-pencil variant="info"/>
				</a>
				<a type="button" @click="acceptEditTitle()" class="h2 mb-0" v-if="edit_title">
					<b-icon-check variant="success"/>
				</a>
				<a type="button" @click="rejectEditTitle()" class="h2 mb-0" v-if="edit_title">
					<b-icon-x variant="danger"/>
				</a>
			</b-card-title>
			
			<b-card-sub-title>

			{{ subtitle }}
			<BadgeElement 
				variant="info"
				v-for="viewer in viewers"
				:key="viewer.id"
				:viewer="viewer.name"
				:edit="edit_viewers_visible"
				@delete="deleteViewer(viewer.id)"
			/>
			
			<a type="button" @click="startEditViewers()" class="h4 mb-0" v-if="viewers_pencil_visible">
				<b-icon-pencil variant="info"/>
			</a>

			<div class="form-group form-inline" v-if="edit_viewers_visible">
				<b-form-input v-model="edit_viewer_input" placeholder="Nowy obserwator"/>
				<a type="button" @click="addNewViewer()" class="h2 mb-0">
					<b-icon-plus variant="info"/>
				</a>
				<b-form-checkbox v-model="edit_public_input">Publiczny</b-form-checkbox>
			</div>
			<a type="button" @click="acceptEditViewers()" class="h2 mb-0" v-if="edit_viewers">
				<b-icon-check variant="success"/>
			</a>

			</b-card-sub-title>

			<b-card-text>
				<a v-if="!edit_message_visible">
					{{ message }}
				</a>
				<b-form-textarea v-model="edit_message_input" placeholder="Treść notatki" rows="10" v-if="edit_message_visible"/>
				<a type="button" @click="startEditMessage()" class="h2 mb-0" v-if="message_pencil_visible">
					<b-icon-pencil variant="info"/>
				</a>
				<a type="button" @click="acceptEditMessage()" class="h2 mb-0" v-if="edit_message">
					<b-icon-check variant="success"/>
				</a>
				<a type="button" @click="rejectEditMessage()" class="h2 mb-0" v-if="edit_message">
					<b-icon-x variant="danger"/>
				</a>
			</b-card-text>
			<b-button variant="success" @click="addNote()" v-if="insertMode">Dodaj notatkę</b-button>
			<b-button variant="danger" @click="deleteNote()" v-if="remove_button_visible">Usuń notatkę</b-button>
		</b-card>
		<br>
	</div>
</template>
   
<!-- Need to console.log works -->
<script src="//unpkg.com/vue@latest/dist/vue.min.js"/>

<script>
	import BadgeElement from "@/components/Home/BadgeElement"
	import axios from 'axios'
	export default {
		data: function () {
			return {
				edit_title: false,
				edit_title_input: "",
				edit_message: false,
				edit_message_input: "",
				edit_viewers: false,
				edit_viewer_input:'',
				edit_public_input: false
			}
		},
		props: ["title", "subtitle", "message", "viewers", "insertMode", "ownerMode", "note_hash", "note_public"],
		methods: {
			startEditTitle: function () {
				this.rejectAllEditions()
				this.edit_title_input = this.title
				this.edit_title=true;
			},
			acceptEditTitle: function () {
			//	this.title = this.edit_title_input
				this.edit_title=false;

				// send request
				this.sendUpdateToServer(this.edit_title_input, this.message)
				console.log("send request to update title of note")
			},
			rejectEditTitle: function () {
				this.edit_title=false;
			},

			startEditMessage: function () {
				this.rejectAllEditions()
				this.edit_message_input = this.message
				this.edit_message=true;
			},
			acceptEditMessage: function () {
			//	this.message = this.edit_message_input
				this.edit_message=false;
				this.sendUpdateToServer(this.title, this.edit_message_input)
				console.log("send request to update message of note")
			},
			rejectEditMessage: function () {
				this.edit_message=false;
			},

			startEditViewers: function () {
				this.rejectAllEditions()
				this.edit_viewers=true
			},
			addNewViewer: function () {
				let newViewer = this.edit_viewer_input
				this.viewers.push({
					'name': newViewer,
					'id': this.viewers.length
				})
				this.edit_viewer_input = ''
				// check if user with such id exists
				// add user assign user to the note
				console.log("send request to update viewers in note")
			},
			deleteViewer: function (viewer_id) {
				console.log("deleteViewer" + viewer_id)
				// remove from viewers element with viewer_id
				for (var i = 0; i < this.viewers.length; i++) {
					var viewer = this.viewers[i];

					if (viewer.id == viewer_id) {
						this.viewers.splice(i, 1);
					}
				}
				// send remove request to server
				console.log("send request to update viewers in note")
			},
			acceptEditViewers: function () {
				this.edit_viewers=false
			},
			rejectAllEditions: function () {
				this.rejectEditMessage()
				this.rejectEditTitle()
				this.acceptEditViewers() // it can be only accepted.
			},
			deleteNote: function () {
				console.log('deleteNote')
				axios.delete('http://localhost:5000/api/notes/' + this.note_hash)
				.then(response => {
					console.log(response.data)
					let message = response.data.message
					if (response.data.success) {
						//this.$emit('deleted')
						this.$emit('reloadNotes')
					} else {
						alert("ER: " + message)
					}
				})
				.catch(e => {
					alert(e)  
				})	
			},
			addNote: function() {
				let payload = {
					viewers: ['ala', 'ma', 'kota'],
					title: this.edit_title_input,
					message: this.edit_message_input,
					public: this.edit_public_input
				}
				axios.post('http://localhost:5000/api/notes', null, {
					data: payload
				})
				.then(response => {
					console.log(response.data)
					let message = response.data.message
					if (response.data.success) {
						console.log("emit next")
						this.$emit('reloadNotes')
						console.log("after emit")
					} else {
						alert("ER: " + message)
					}
				})
				.catch(e => {
					alert(e)  
				})
			},
			sendUpdateToServer: function (new_title, new_message) {
				let payload = {
					viewers: ['ala', 'ma', 'kota'],
					title: new_title,
					message: new_message,
					public: this.edit_public_input
				}
				axios.post('http://localhost:5000/api/notes/' + this.note_hash, null, {
					params: {
					},
					data: payload
				})
				.then(response => {
					console.log(response.data)
					let message = response.data.message
					if (response.data.success) {
						this.$emit('updated')
					} else {
						alert("ER: " + message)
					}
				})
				.catch(e => {
					alert(e)  
				})
			}
		},
		computed: {
			edit_title_visible: function () {
				return this.edit_title || this.insertMode
			},
			edit_viewers_visible: function () {
				return this.edit_viewers || this.insertMode
			},
			viewers_pencil_visible: function () {
				return (!this.edit_viewers) && this.ownerMode && (!this.insertMode)
			},
			edit_message_visible: function () {
				return this.edit_message || this.insertMode
			},
			message_pencil_visible: function () {
				return (!this.edit_message) && this.ownerMode && (!this.insertMode)
			},
			title_pencil_visible: function () {
				return (!this.edit_title) && this.ownerMode && (!this.insertMode)
			},
			remove_button_visible: function () {
				return (!this.insertMode) && (this.ownerMode)
			}
		},
		watch: {
			edit_public_input: function () {
				if (this.edit_public_input) {
					// send req to make note public
					console.log("send req to make note public")
					// rm all 
					this.viewers.splice(0, this.viewers.length)
				}

			}
		},
		components: {
			'BadgeElement' : BadgeElement
		}
    }
	
</script>
