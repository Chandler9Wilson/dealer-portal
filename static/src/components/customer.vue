<template>
  <div>
    This is Customer #{{ $route.params.id }}
    <div>My name is {{ name }}</div>
  </div>
</template>

<script>
export default {
  name: 'customer',
  data() {
    return {
      id: null,
      name: null,
      loading: null
    }
  },
  created() {
    this.fetchCustomer()
  },
  methods: {
    fetchCustomer() {
      var self = this
      self.loading = true
      var uri = '/api/customers/' + this.$route.params.id

      fetch(uri).then(function(response) {
        return response.json()
      }).then(function(customerJSON) {
        self.id = customerJSON.id
        self.name = customerJSON.name
        self.loading = false
      })
    }
  }
}
</script>