<template>
  <nav class="navbar is-primary" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <a class="navbar-item" href="/home">
        <img src="https://via.placeholder.com/112x28" alt="I should probably update" width="112" height="28">
      </a>

      <div class="navbar-burger" @click="showNav = !showNav" :class="{ 'is-active': showNav }">
        <span></span>
        <span></span>
        <span></span>
      </div>
    </div>

    <div class="navbar-menu" :class="{ 'is-active': showNav }">
        <!-- Left side of the navbar after the brand image -->
        <div class="navbar-start">
          <router-link to="/" class="navbar-item">Home</router-link>

          <div class="navbar-item has-dropdown" v-bind:class="{'is-active': isActive}" @click="isActive = !isActive">
            <a class="navbar-link">
              Create New
            </a>

            <div class="navbar-dropdown">
              <router-link to="/facilities/new" class="navbar-item">Facility</router-link>
              <router-link to="/customers/new" class="navbar-item">Customer</router-link>
              <router-link to="/devices/new" class="navbar-item">Device</router-link>
            </div>
          </div>
        </div>

        <!-- Right side of the navbar -->
        <div class="navbar-end">
          <a class="navbar-item" href="/logout/">Logout</a>
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
      // TODO improve the dropdown toggle to also capture clicks outside of the button
      // posible solution https://github.com/buefy/buefy/blob/dev/src/components/dropdown/Dropdown.vue
      isActive: false,
      showNav: false
    }
  }
}
</script>
