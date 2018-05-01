<template>
<div class="box">
  <p class="title">Data</p>

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
    <temp-chart :t1="t1" :t2="t2"></temp-chart>
  </div>
</div>
</template>

<script>
import tempChart from './tempChart.vue'

export default {
  name: 'dataCard',
  components: {
    tempChart
  },
  data() {
    return {
      loading: null,
      error: null,
      data: null
    }
  },
  computed: {
    t1: function() {
      self = this
      length = self.data.length

      if(length > 0) {
        var t1Array = []

        for(var i = 0; i < length; i++) {
          var obj = {}

          obj.y = self.data[i].t1
          obj.x = self.data[i].timestamp

          t1Array.push(obj)
        }

        return t1Array
      } else {
        return null
      }
    },
    t2: function() {
      self = this
      length = self.data.length

      if(length > 0) {
        var t2Array = []

        for(var i = 0; i < length; i++) {
          var obj = {}

          obj.y = self.data[i].t2
          obj.x = self.data[i].timestamp

          t2Array.push(obj)
        }

        return t2Array
      } else {
        return null
      }
    }
  },
  props: [
    'url'
  ],
  created() {
    this.fetchData(this.$props.url)
  },
  methods: {
    fetchData (url) {
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
      }).then(function(dataJSON) {
        self.data = dataJSON
        self.loading = null
      })
    }
  }
}
</script>