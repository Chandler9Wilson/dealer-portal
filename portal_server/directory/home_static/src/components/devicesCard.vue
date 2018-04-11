<template>
<div class="tile is-vertical is-parent">
    <div class="tile is-child box">
      <p class="title">Devices</p>

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

      <div v-if="data && data.length > 0" class="table__wrapper">
        <table class="table is-hoverable">
          <thead>
            <tr>
              <th>ID</th>
              <th>Hardware ID</th>
              <th>Device Type</th>
              <th>HVAC Description</th>
              <th>Facility ID</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="device in data" :key="device.id">
              <td><router-link :to="{ name: 'device', params: { id: device.id }}">{{ device.id }}</router-link></td>
              <td><router-link :to="{ name: 'device', params: { id: device.id }}">{{ device.hardware_id }}</router-link></td>
              <td><router-link :to="{ name: 'device', params: { id: device.id }}">{{ device.device_type }}</router-link></td>
              <td><router-link :to="{ name: 'device', params: { id: device.id }}">{{ device.hvac_description }}</router-link></td>
              <td><router-link :to="{ name: 'device', params: { id: device.id }}">{{ device.facility_id }}</router-link></td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'devicesCard',
  data() {
    return {
      loading: null,
      error: null,
      data: null
    }
  },
  props: [
    'url'
  ],
  created() {
    this.fetchDevices(this.$props.url)
  },
  methods: {
    fetchDevices (url) {
      var self = this
      self.loading = true

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
      }).then(function(deviceJSON) {
        self.data = deviceJSON
        self.loading = false
      })
    }
  }
}
</script>