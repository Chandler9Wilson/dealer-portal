<template>
  <div id="app">
    <navbar/>
    <breadcrumb/>
    <router-view/>
  </div>
</template>

<script>
import navbar from './components/navbar'
import breadcrumb from './components/breadcrumb'

export default {
  name: 'App',
  components: {
    navbar,
    breadcrumb
  }
}
</script>


