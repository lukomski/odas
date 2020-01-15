<template>
	<div v-bind:class="{'d-inline': !this.edit }">
		<b-badge variant="info">
			{{ viewer }}
		</b-badge>
		<a type="button" @click="deleteViewer()" class="h5 mb-0" v-if="edit">
			<b-icon-x variant="danger"/>
		</a>
	</div>
</template>
<script>
	export default {
		data: function () {
			return {
			}
		},
		props: ["viewer", "is_public", "edit"],
		methods: {
			deleteViewer: function () {
				this.$emit('delete', this.viewer)
			}
		}
    }
	
</script>

