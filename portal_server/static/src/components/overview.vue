<template>
  <!-- TODO split customers, devices etc. into seperate components -->
  <div class="tile is-ancestor box">
    <div class="tile is-vertical is-parent is-3">
      <div class="tile is-child box">
        <p class="title">Customers</p>

        <div class="spinner" v-if="customers.loading">
          <div class="rect1"></div>
          <div class="rect2"></div>
          <div class="rect3"></div>
          <div class="rect4"></div>
          <div class="rect5"></div>
        </div>

        <div v-if="customers.error">
          <!-- TODO improve error display -->
          {{ error }}
        </div>


        <div v-if="customers.data">
          <table class="table is-hoverable">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="customer in customers.data" :key="customer.id">
                <td><router-link :to="{ name: 'customer', params: { id: customer.id }}">{{ customer.id }}</router-link></td>
                <td><router-link :to="{ name: 'customer', params: { id: customer.id }}">{{ customer.name }}</router-link></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="tile is-vertical is-parent">
      <div class="tile is-child box">
        <p class="title">Facilities</p>

        <div class="spinner" v-if="facilities.loading">
          <div class="rect1"></div>
          <div class="rect2"></div>
          <div class="rect3"></div>
          <div class="rect4"></div>
          <div class="rect5"></div>
        </div>

        <div v-if="facilities.error">
          <!-- TODO improve error display -->
          {{ error }}
        </div>

        <div v-if="facilities.data">
          <table class="table is-hoverable">
            <thead>
              <tr>
                <th>ID</th>
                <th>Address</th>
                <th>Customer ID</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="facility in facilities.data" :key="facility.id">
                <td><router-link :to="{ name: 'facility', params: { id: facility.id }}">{{ facility.id }}</router-link></td>
                <td><router-link :to="{ name: 'facility', params: { id: facility.id }}">{{ facility.address }}</router-link></td>
                <td><router-link :to="{ name: 'facility', params: { id: facility.id }}">{{ facility.customer_id }}</router-link></td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div class="tile is-vertical is-parent">
      <div class="tile is-child box">
        <p class="title">Devices</p>

        <div class="spinner" v-if="devices.loading">
          <div class="rect1"></div>
          <div class="rect2"></div>
          <div class="rect3"></div>
          <div class="rect4"></div>
          <div class="rect5"></div>
        </div>

        <div v-if="devices.error">
          <!-- TODO improve error display -->
          {{ error }}
        </div>

        <div v-if="devices.data">
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
              <tr v-for="device in devices.data" :key="device.id">
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
  </div>
</template>

<script>
export default {
  name: 'overview',
  data() {
    return {
      customers: {
        data: null,
        error: null,
        loading: null
      },
      devices: {
        data: null,
        error: null,
        loading: null
      },
      facilities: {
        data: null,
        error: null,
        loading: null
      }
    }
  },
  // Called after view creation
  created() {
    this.fetchCustomers()
    this.fetchDevices()
    this.fetchFacilities()
  },
  methods: {
    fetchCustomers() {
      var self = this
      self.customers.loading = true,

      fetch('/api/customers/').then(function(response) {
        return response.json()
      }).then(function(customerJSON) {
        self.customers.data = customerJSON
        self.customers.loading = false
      })
    },
    fetchDevices() {
      var self = this
      self.devices.loading = true,

      fetch('/api/devices/').then(function(response) {
        return response.json()
      }).then(function(deviceJSON) {
        self.devices.data = deviceJSON
        self.devices.loading = false
      })
    },
    fetchFacilities() {
      var self = this
      self.facilities.loading = true,

      fetch('/api/facilities/').then(function(response) {
        return response.json()
      }).then(function(customerJSON) {
        self.facilities.data = customerJSON
        self.facilities.loading = false
      })
    }
  }
}
</script>