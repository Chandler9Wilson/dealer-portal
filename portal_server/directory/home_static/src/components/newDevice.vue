<template>
  <div>
    <section class="hero is-info">
      <div class="hero-body">
        <div class="container">
          <div class="columns">
            <div class="column is-two-thirds">
              <h1 class="title">
                Device
              </h1>
              <h2 class="subtitle">
                {{ hvacDescription }}
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
          <label class="label">Hardware ID</label>
          <div class="control">
            <input
                v-validate="'required'"
                v-model.number="hardwareID"
                :class="{'input': true, 'is-danger': errors.has('hardwareID')}"
                name="hardwareID"
                type="number"
                placeholder="123456789"
            />
            <span v-show="errors.has('hardwareID')" class="help is-danger">{{ errors.first('hardwareID') }}</span>
          </div>
        </div>

        <div class="field">
          <label class="label">Device Type</label>
          <div class="control">
            <input
                v-validate="'required'"
                v-model="deviceType"
                :class="{'input': true, 'is-danger': errors.has('deviceType')}"
                name="deviceType"
                type="text"
                placeholder="Temp sensor V.1.23"
            />
            <span v-show="errors.has('deviceType')" class="help is-danger">{{ errors.first('deviceType') }}</span>
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
    }
  },
  methods: {
    updateDevice() {
      var self = this
      self.loading = true
      var url = '/api/devices/'

      var myInit = {
        method: 'POST',
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
        if (response.status == 201) {
          return response.json()
        }
        // TODO improve this error
        throw new Error('Network response was not ok.')
      }).then(function(deviceJSON) {
        self.clearData()

        var deviceID = deviceJSON.id
        var deviceURL = '/devices/' + deviceID + '/'
        self.$router.push(deviceURL)
      })
    },
    validateBeforeSubmit() {
      var self = this

      self.$validator.validateAll().then((result) => {
        if (result) {
          self.updateDevice()
          return
        } else {
          self.$alert('error', 'There was a problem validating the form.')
        }
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
    }
  }
}
</script>
