import Vue from 'vue'
import router from '../router'
import App from './../App.vue'

require('bulma/css/bulma.css')

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
