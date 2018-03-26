<template>
  <div>
    <section class="hero is-info">
      <div class="hero-body">
        <div class="container">
          <div class="columns">
            <div class="column is-two-thirds">
              <h1 class="title">
                Customer #{{ $route.params.id }}
              </h1>
              <h2 class="subtitle">
                {{ name }}
              </h2>
            </div>
            <div class="column is-one-third">
              <a @click="deleteWarning=true" class="button is-danger is-pulled-right">Delete</a>
            </div>
          </div>
        </div>
      </div>
    </section>

    <div class="spinner" v-if="loading">
      <div class="rect1"></div>
      <div class="rect2"></div>
      <div class="rect3"></div>
      <div class="rect4"></div>
      <div class="rect5"></div>
    </div>

    <div v-else-if="error">
      <!-- TODO improve error display -->
      {{ error }}
    </div>

    <div v-else>
    <!-- .prevent = the submit event will no longer reload the page -->
      <form class="box" @submit.prevent="updateCustomer">
        <div class="field">
          <label class="label">Name</label>
          <div class="control">
            <input v-model="name" class="input" type="text" placeholder="Bowditch Navigation">
          </div>
        </div>

        <div class="field is-grouped is-grouped-right">
          <div class="control">
            <button class="button is-success">
              <span class="icon is-small">
                <i class="fas fa-check"></i>
              </span>
              <span>Save</span>
            </button>
          </div>
        </div>
      </form>
    </div>

    <div v-if="deleteWarning">
      <div class="modal is-active">
        <div class="modal-background"></div>
        <div class="modal-content">
          <article class="message is-danger">
            <div class="message-header">
              <p>Warning</p>
              <button @click="deleteWarning=null" class="delete" aria-label="delete"></button>
            </div>
            <div class="message-body">
              <div class="columns is-centered">
                <div class="column is-6">
                  <p>This will <strong>permanently delete</strong> Customer #{{ $route.params.id }}</p>
                </div>
              </div>
              <div class="columns">
                <div class="column is-12">
                  <a @click="deleteCustomer" class="button is-danger is-pulled-right">Delete</a>
                  <a @click="deleteWarning=null" class="button is-pulled-right">Cancel</a>
                </div>
              </div>
            </div>

          </article>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'customer',
  data() {
    return {
      name: null,
      error: null,
      loading: null,
      deleteWarning: null
    }
  },
  // Called after view creation
  created() {
    this.fetchCustomer()
  },
  watch: {
    '$route' (to, from) {
      this.clearData()
      this.fetchCustomer()
    }
  },
  methods: {
    // TODO add error handling
    fetchCustomer() {
      var self = this
      self.loading = true
      var url = '/api/customers/' + self.$route.params.id + '/'

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
          return response.json()
        }
        // TODO improve this error
        throw new Error('Network response was not ok.')
      }).then(function(customerJSON) {
        self.name = customerJSON.name
        self.loading = false
      })
    },
    updateCustomer() {
      var self = this
      self.loading = true
      var url = '/api/customers/' + self.$route.params.id + '/'

      var myInit = {
        method: 'PUT',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        // https://developer.mozilla.org/en-US/docs/Web/API/Request/credentials
        credentials: 'same-origin',
        body: JSON.stringify({
          name: self.name
        })
      }
      fetch(url, myInit).then(function(response) {
        if (response.ok) {
          self.$alert('success', 'Customer was updated.')
          return response.json()
        }
        // TODO improve this error
        throw new Error('Network response was not ok.')
      }).then(function(customerJSON) {
        self.clearData()

        self.name = customerJSON.name
        self.loading = false
      })
    },
    deleteCustomer() {
      var self = this
      self.loading = true
      self.deleteWarning = null
      var url = '/api/customers/' + self.$route.params.id + '/'

      var myInit = {
        method: 'DELETE',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        // https://developer.mozilla.org/en-US/docs/Web/API/Request/credentials
        credentials: 'same-origin',
      }
      fetch(url, myInit).then(function(response) {
        if (response.status == 204) {
          self.$alert('success', 'Customer was deleted.')
          return null
        }
        // TODO improve this error
        throw new Error('Network response was not ok.')
      }).then(function() {
        self.clearData()
        self.$router.push('/')
      })
    },
    // TODO make this clear dynamically
    clearData() {
      var self = this

      self.name = null
      self.error = null
      self.loading = null
      self.deleteWarning = null
    }
  }
}
</script>