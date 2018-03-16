<template>
  <div>
    <section class="hero is-info">
      <div class="hero-body">
        <div class="container">
          <div class="columns">
            <div class="column is-two-thirds">
              <h1 class="title">
                Device #{{ $route.params.id }}
              </h1>
              <h2 class="subtitle">
                {{ hvacDescription }}
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

    <div v-if="error">
      <!-- TODO improve error display -->
      {{ error }}
    </div>

    <div v-if="hardwareID">
    <!-- .prevent = the submit event will no longer reload the page -->
      <form class="box" @submit.prevent="updateDevice">
        <div class="field">
          <label class="label">Hardware ID</label>
          <div class="control">
            <input v-model.number="hardwareID" class="input" type="number" placeholder="123456789">
          </div>
        </div>

        <div class="field">
          <label class="label">Device Type</label>
          <div class="control">
            <input v-model="deviceType" class="input" type="text" placeholder="Temp only">
          </div>
          <p class="help">A description of the device</p>
        </div>

        <div class="field">
          <label class="label">HVAC Description</label>
          <div class="control">
            <input v-model="hvacDescription" class="input" type="text" placeholder="West Wing Unit 1">
          </div>
          <p class="help">A description of the hvac unit a device is monitoring</p>
        </div>

        <div class="field">
          <label class="label">Facility ID</label>
          <div class="control">
            <input v-model.number="facilityID" class="input" type="number" placeholder="12">
          </div>
          <p class="help">Facility ID number (this is not required)</p>
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
                  <p>This will <strong>permanently delete</strong> Device #{{ $route.params.id }}</p>
                </div>
              </div>
              <div class="columns">
                <div class="column is-12">
                  <a @click="deleteDevice" class="button is-danger is-pulled-right">Delete</a>
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
  name: 'device',
  data() {
    return {
      hardwareID: null,
      deviceType: null,
      hvacDescription: null,
      facilityID: null,
      error: null,
      loading: null,
      deleteWarning: null
    }
  },
  // Called after view creation
  created() {
    this.fetchDevice()
  },
  watch: {
    '$route' (to, from) {
      this.clearData()
      this.fetchDevice()
    }
  },
  methods: {
    // TODO add error handling
    fetchDevice() {
      var self = this
      self.loading = true
      var url = '/api/devices/' + self.$route.params.id + '/'

      fetch(url).then(function(response) {
        if (response.ok) {
          return response.json()
        }
        // TODO improve this error
        throw new Error('Network response was not ok.')
      }).then(function(deviceJSON) {
        self.hardwareID = deviceJSON.hardware_id
        self.deviceType = deviceJSON.device_type
        self.hvacDescription = deviceJSON.hvac_description
        self.facilityID = deviceJSON.facility_id
        self.loading = false
      })
    },
    updateDevice() {
      var self = this
      self.loading = true
      var url = '/api/devices/' + self.$route.params.id + '/'

      var myInit = {
        method: 'PUT',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        // https://developer.mozilla.org/en-US/docs/Web/API/Request/credentials
        credentials: 'same-origin',
        body: JSON.stringify({
          hardware_id: self.hardwareID,
          device_type: self.deviceType,
          hvac_description: self.hvacDescription,
          facility_id: self.facilityID
        })
      }
      fetch(url, myInit).then(function(response) {
        if (response.ok) {
          return response.json()
        }
        // TODO improve this error
        throw new Error('Network response was not ok.')
      }).then(function(deviceJSON) {
        self.clearData()

        self.hardwareID = deviceJSON.hardware_id
        self.deviceType = deviceJSON.device_type
        self.hvacDescription = deviceJSON.hvac_description
        self.facilityID = deviceJSON.facility_id
        self.loading = false
      })
    },
    deleteDevice() {
      var self = this
      self.loading = true
      self.deleteWarning = null
      var url = '/api/devices/' + self.$route.params.id + '/'

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

      self.hardwareID = null
      self.deviceType = null
      self.hvacDescription = null
      self.facilityID = null
      self.error = null
      self.loading = null
      self.deleteWarning = null
    }
  }
}
</script>