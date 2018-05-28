<template>
  <div id="app">
    <navbar></navbar>
  </div>
</template>

<script>
// Navbar is directly imported from the home dashboard's set of components
import navbar from './components/navbar.vue'

export default {
  name: 'app',
  components: {
    navbar
  }
}
</script>
