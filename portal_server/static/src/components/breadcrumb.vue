<template>
  <nav class="breadcrumb box" aria-label="breadcrumbs">
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