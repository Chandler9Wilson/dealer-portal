<template>
  <div>
    <section class="hero is-info">
      <div class="hero-body">
        <div class="container">
          <div class="columns">
            <div class="column is-two-thirds">
              <h1 class="title">
                Customer
              </h1>
              <h2 class="subtitle">
                {{ name }}
              </h2>
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
      <form class="box" @submit.prevent="validateBeforeSubmit">
        <div class="field">
          <label class="label">Name</label>
          <div class="control">
            <input
                v-validate="'required'"
                v-model="name"
                :class="{'input': true, 'is-danger': errors.has('name')}"
                name="name"
                type="text"
                placeholder="Bowditch Navigation"
            />
            <span v-show="errors.has('name')" class="help is-danger">{{ errors.first('name') }}</span>
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
    }
  },
  methods: {
    updateCustomer() {
      var self = this
      self.loading = true
      var url = '/api/customers/'

      var myInit = {
        method: 'POST',
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
        if (response.status == 201) {
          return response.json()
        }
        // TODO improve this error
        throw new Error('Network response was not ok.')
      }).then(function(customerJSON) {
        self.clearData()

        var customerID = customerJSON.id
        var customerURL = '/customers/' + customerID + '/'
        self.$router.push(customerURL)
      })
    },
    validateBeforeSubmit() {
      var self = this

      self.$validator.validateAll().then((result) => {
        if (result) {
          self.updateCustomer()
          return
        } else {
          self.$alert('error', 'There was a problem validating the form.')
        }
      })
    },
    // TODO make this clear dynamically
    clearData() {
      var self = this

      self.name = null
      self.error = null
      self.loading = null
    }
  }
}
</script>