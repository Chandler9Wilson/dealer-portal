<template>
  <div>
    <section class="hero is-info">
      <div class="hero-body">
        <div class="container">
          <div class="columns">
            <div class="column is-two-thirds">
              <h1 class="title">
                Facility #{{ $route.params.id }}
              </h1>
              <h2 class="subtitle">
                {{ address }}
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
      <form class="box" @submit.prevent="validateBeforeSubmit">
        <div class="field">
          <label class="label">Address</label>
          <div class="control">
            <input
                v-validate.initial="'required'"
                v-model="address"
                :class="{'input': true, 'is-danger': errors.has('address')}"
                name="address"
                type="text"
                placeholder="1600 Pennsylvania Ave NW, Washington, DC 20500"
            />
            <span v-show="errors.has('address')" class="help is-danger">{{ errors.first('address') }}</span>
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
      <devices-card :url="'/api/facilities/' + $route.params.id + '/devices/'"></devices-card>
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
                  <p>This will <strong>permanently delete</strong> Facility #{{ $route.params.id }}</p>
                </div>
              </div>
              <div class="columns">
                <div class="column is-12">
                  <a @click="deleteFacility" class="button is-danger is-pulled-right">Delete</a>
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
import devicesCard from './devicesCard.vue'

export default {
  name: 'facility',
  components: {
    devicesCard
  },
  data() {
    return {
      address: null,
      customerID: null,
      error: null,
      loading: null,
      deleteWarning: null
    }
  },
  // Called after view creation
  created() {
    this.fetchFacility()
  },
  watch: {
    '$route' (to, from) {
      this.clearData()
      this.fetchFacility()
    }
  },
  methods: {
    // TODO add error handling
    fetchFacility() {
      var self = this
      self.loading = true
      var url = '/api/facilities/' + self.$route.params.id + '/'

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
      }).then(function(facilityJSON) {
        self.address = facilityJSON.address
        self.customerID = facilityJSON.customer_id
        self.loading = false
      })
    },
    updateFacility() {
      var self = this
      self.loading = true
      var url = '/api/facilities/' + self.$route.params.id + '/'

      var myInit = {
        method: 'PUT',
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
        if (response.ok) {
          self.$alert('success', 'Facility was updated')
          return response.json()
        }
        // TODO improve this error
        throw new Error('Network response was not ok.')
      }).then(function(facilityJSON) {
        self.clearData()

        self.address = facilityJSON.address
        self.customerID = facilityJSON.customer_id
        self.loading = false
      })
    },
    deleteFacility() {
      var self = this
      self.loading = true
      self.deleteWarning = null
      var url = '/api/facilities/' + self.$route.params.id + '/'

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
          self.$alert('success', 'Facility was deleted.')
          return null
        }
        // TODO improve this error
        throw new Error('Network response was not ok.')
      }).then(function() {
        self.clearData()
        self.$router.push('/')
      })
    },
    validateBeforeSubmit() {
      var self = this

      self.$validator.validateAll().then((result) => {
        if (result) {
          self.updateFacility()
          return
        } else {
          self.$alert('error', 'There was a problem validating the form.')
        }
      })
    },
    // TODO make this clear dynamically
    clearData() {
      var self = this

      self.address = null
      self.customerID = null
      self.error = null
      self.loading = null
      self.deleteWarning = null
    }
  }
}
</script>
