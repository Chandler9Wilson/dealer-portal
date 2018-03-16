import Vue from 'vue'
import router from '../router'
import App from './../App.vue'

import fontawesome from '@fortawesome/fontawesome'
import faCheck from '@fortawesome/fontawesome-free-solid/faCheck'

require('bulma/css/bulma.css')

fontawesome.library.add(faCheck)

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
