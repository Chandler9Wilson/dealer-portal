<template>
  <nav class="breadcrumb box no-bottom" aria-label="breadcrumbs">
    <ul>
      <!-- TODO make this dynamic possibly read from $route with an if statement for devices/1 etc -->
      <li><a href="#">Hello</a></li>
      <li><a href="#">World</a></li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'breadcrumb'
}
</script>

<style scoped>
.no-bottom {
  margin-bottom: 0;
}
</style>
