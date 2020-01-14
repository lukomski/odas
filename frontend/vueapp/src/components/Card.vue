<template>
	<div>
		<b-card>
			<b-card-title>
				<a v-if="!edit_title">
					{{ title }}
				</a>

				<b-form-input v-model="edit_title_input" placeholder="Tytuł notatki" v-if="edit_title" :value="title"/>

				<a type="button" @click="startEditTitle()" class="h2 mb-0" v-if="!edit_title">
					<b-icon-pencil variant="info"/>
				</a>

				<a type="button" @click="acceptEditTitle()" class="h2 mb-0" v-if="edit_title">
					<b-icon-check variant="success"/>
				</a>

				<a type="button" @click="rejectEditTitle()" class="h2 mb-0" v-if="edit_title">
					<b-icon-x variant="danger"/>
				</a>
			</b-card-title>
			
			<b-card-sub-title>{{ subtitle }}</b-card-sub-title>
			<b-card-text>
				<a v-if="!edit_message">
					{{ message }}
				</a>
				<b-form-textarea
					v-model="edit_message_input"
					placeholder="Treść notatki"
					rows="10"
					v-if="edit_message"
				/>
				<a type="button" @click="startEditMessage()" class="h2 mb-0" v-if="!edit_message">
					<b-icon-pencil variant="info"/>
				</a>

				<a type="button" @click="acceptEditMessage()" class="h2 mb-0" v-if="edit_message">
					<b-icon-check variant="success"/>
				</a>

				<a type="button" @click="rejectEditMessage()" class="h2 mb-0" v-if="edit_message">
					<b-icon-x variant="danger"/>
				</a>
			</b-card-text>
		</b-card>
	</div>
</template>
   
  <!-- Load Vue followed by BootstrapVueIcons -->
  <script src="//unpkg.com/vue@latest/dist/vue.min.js"></script>
  <script src="//unpkg.com/bootstrap-vue@latest/dist/bootstrap-vue-icons.min.js"></script>

<script>
	import { BIcon, BIconArrowUp, BIconArrowDown } from 'bootstrap-vue'
	export default {
		data: function () {
			return {
				edit_title: false,
				edit_title_input: "",
				edit_message: false,
				edit_message_input: ""
			}
		},
		props: ["title", "subtitle", "message"],
		methods: {
			startEditTitle: function () {
				this.edit_title_input = this.title
				this.edit_title=true;
			},
			acceptEditTitle: function () {
				this.title = this.edit_title_input
				this.edit_title=false;
			},
			rejectEditTitle: function () {
				this.edit_title=false;
			},

			startEditMessage: function () {
				this.edit_message_input = this.message
				this.edit_message=true;
			},
			acceptEditMessage: function () {
				this.message = this.edit_message_input
				this.edit_message=false;
			},
			rejectEditMessage: function () {
				this.edit_message=false;
			}
		}
    }
	
</script>
<link type="text/css" rel="stylesheet" href="//unpkg.com/bootstrap/dist/css/bootstrap.min.css" />
  <link type="text/css" rel="stylesheet" href="//unpkg.com/bootstrap-vue@latest/dist/bootstrap-vue-icons.min.css" />
