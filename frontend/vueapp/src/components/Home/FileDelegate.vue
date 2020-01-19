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
				this.$emit('download',this.file)
			},
			remove: function () {
				this.$emit('delete',this.file)
			},
		}
	}

</script>

<style>
	
</style>