<template>
  <div>
    <section class="hero is-info">
      <div class="hero-body">
        <div class="container">
          <div class="columns">
            <div class="column is-two-thirds">
              <h1 class="title">
                Facility
              </h1>
              <h2 class="subtitle">
                {{ address }}
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
      <form class="box" @submit.prevent="updateFacility">
        <div class="field">
          <label class="label">Address</label>
          <div class="control">
            <input v-model="address" class="input" type="text" placeholder="Address">
          </div>
        </div>

        <div class="field">
          <label class="label">Customer ID</label>
          <div class="control">
            <input v-model.number="customerID" class="input" type="number" placeholder="1">
          </div>
          <p class="help">Customer ID number (this is not required)</p>
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
  name: 'facility',
  data() {
    return {
      address: null,
      customerID: null,
      error: null,
      loading: null,
    }
  },
  methods: {
    updateFacility() {
      var self = this
      self.loading = true
      var url = '/api/facilities/'

      var myInit = {
        method: 'POST',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        // https://developer.mozilla.org/en-US/docs/Web/API/Request/credentials
        credentials: 'same-origin',
        body: JSON.stringify({
          address: self.address,
          customer_id: self.customerID
        })
      }
      fetch(url, myInit).then(function(response) {
        if (response.status == 201) {
          return response.json()
        }
        // TODO improve this error
        throw new Error('Network response was not ok.')
      }).then(function(facilityData) {
        self.clearData()

        var facilityID = facilityData.id
        var facilityURL = '/facilities/' + facilityID + '/'
        self.$router.push(facilityURL)
      })
    },
    // TODO make this clear dynamically
    clearData() {
      var self = this

      self.address = null
      self.customerID = null
      self.error = null
      self.loading = null
    }
  }
}
</script>