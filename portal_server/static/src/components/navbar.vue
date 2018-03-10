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
          <router-link to="/" class="navbar-item">Home</router-link>

          <div class="navbar-item has-dropdown" v-bind:class="{'is-active': isActive}" @click="isActive = !isActive">
            <a class="navbar-link">
              Find
            </a>

            <div class="navbar-dropdown">
              <router-link to="/facilities" class="navbar-item">Facility</router-link>
              <router-link to="/customers" class="navbar-item">Customer</router-link>
              <router-link to="/devices" class="navbar-item">Device</router-link>
            </div>
          </div>
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
      msg: "Hello World",
      isActive: false
    }
  }
}
</script>
