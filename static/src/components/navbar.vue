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

          <div class="navbar-item has-dropdown" v-bind:class="{'is-active': isActive}" @click="isActive = !isActive">
            <a class="navbar-link">
              Find
            </a>

            <div class="navbar-dropdown">
              <router-link to="/facility" class="navbar-item">Facility</router-link>
              <router-link to="/customer" class="navbar-item">Customer</router-link>
              <router-link to="/device" class="navbar-item">Device</router-link>
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
