<template>
  <nav class="navbar is-primary" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <a class="navbar-item" href="/home">
        <img src="http://via.placeholder.com/112x28" alt="I should probably update" width="112" height="28">
      </a>
    </div>

    <div class="navbar-menu">
        <!-- Left side of the navbar after the brand image -->
        <div class="navbar-start">
          <a class="navbar-item" href="/home">Home</a>
        </div>

        <!-- Right side of the navbar -->
        <div class="navbar-end">
          <a class="navbar-item" href="/login?logout=true" onclick="logout()">Logout</a>
        </div>
      </div>
  </nav>
</template>

<script>
export default {
  name: 'navbar',
  data() {
    return {
      msg: "Hello World"
    }
  }
}
</script>
