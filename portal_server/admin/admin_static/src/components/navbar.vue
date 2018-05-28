<template>
  <nav class="navbar is-primary" role="navigation" aria-label="main navigation">
    <div class="navbar-brand">
      <a href="/" class="navbar-item">
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
          <a href="/" class="navbar-item">
            Home
          </a>
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
      // TODO improve the dropdown toggle to also capture clicks outside of the button
      // posible solution https://github.com/buefy/buefy/blob/dev/src/components/dropdown/Dropdown.vue
      isActive: false,
      isAdmin: null,
      showNav: false
    }
  },
  created() {
    this.checkIfAdmin()
  },
  methods: {
    checkIfAdmin() {
      var self = this
      self.loading = true
      var url = '/admin/api/'

      var myInit = {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        // https://developer.mozilla.org/en-US/docs/Web/API/Request/credentials
        credentials: 'same-origin'
      }

      fetch(url, myInit).then(function(response) {
        if (response.ok) {
          return self.isAdmin = true
        }
      })
    }
  }
}
</script>
