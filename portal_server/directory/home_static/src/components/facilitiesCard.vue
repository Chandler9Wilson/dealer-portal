<template>
<div class="tile is-vertical is-parent">
  <div class="tile is-child box">
    <p class="title">Facilities</p>

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
            <th>Address</th>
            <th>Customer ID</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="facility in data" :key="facility.id">
            <td><router-link :to="{ name: 'facility', params: { id: facility.id }}">{{ facility.id }}</router-link></td>
            <td><router-link :to="{ name: 'facility', params: { id: facility.id }}">{{ facility.address }}</router-link></td>
            <td><router-link :to="{ name: 'facility', params: { id: facility.id }}">{{ facility.customer_id }}</router-link></td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>
</template>

<script>
export default {
  name: 'facilitiesCard',
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
    this.fetchFacilities(this.$props.url)
  },
  methods: {
    fetchFacilities(url) {
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
      }).then(function(facilityJSON) {
        self.data = facilityJSON
        self.loading = false
      })
    }
  }
}
</script>