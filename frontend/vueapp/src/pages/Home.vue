<template>
  <div>
	<NavigationBar/>
    <h1>Home</h1>
    <p>Here is some information. This is the home page</p>
  </div>
</template>

<script>
import NavigationBar from '../components/NavigationBar'
export default {
  name: 'Home', //this is the name of the component
  components: {
	'NavigationBar' : NavigationBar
  }
}
</script>
<style>
</style>