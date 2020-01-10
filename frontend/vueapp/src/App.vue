<template>
  <div id="app">
    <NavigationBar/>
    <router-view></router-view>
  </div>
</template>

<script>
import NavigationBar from '@/components/NavigationBar'

export default {
  name: 'app',
  components: {
    'NavigationBar': NavigationBar
  }
}
</script>

<style></style>
