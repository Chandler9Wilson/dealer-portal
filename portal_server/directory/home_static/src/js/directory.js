import Vue from 'vue'

// Vue plugins
import Toasted from 'vue-toasted'
import VeeValidate from 'vee-validate'

// Project files
import router from '../router'
import App from './../App.vue'

// Font awesome library followed by imported icons
import fontawesome from '@fortawesome/fontawesome'
import faCheck from '@fortawesome/fontawesome-free-solid/faCheck'

// Vue plugin registration
Vue.use(VeeValidate)
Vue.use(Toasted)

require('bulma/css/bulma.css')

fontawesome.library.add(faCheck)

// Register custom toasts
Vue.toasted.register('error',
  (payload) => {
    if (payload.message) {
      return payload.message
    }
    return 'A problem occured'
  },
  {
    position: 'bottom-center',
    type: 'primary',
    className: ['button', 'is-danger'],
    duration: 8000
  }
)

Vue.toasted.register('success',
  (payload) => {
    if (payload.message) {
      return payload.message
    }
    return 'Success!'
  },
  {
    position: 'bottom-center',
    type: 'primary',
    className: ['button', 'is-success'],
    duration: 3000
  }
)

Vue.toasted.register('info',
  (payload) => {
    if (payload.message) {
      return payload.message
    }
    return 'The programmer should really not pass an info message without info...'
  },
  {
    position: 'bottom-center',
    type: 'primary',
    className: ['button', 'is-info'],
    duration: 3000
  }
)

/* eslint-disable no-unused-vars */
Vue.prototype.$alert = function (type, message) {
  switch (type) {
    case 'error':
      var newProblem = Vue.toasted.global.error({
        message: message
      })
      newProblem.el.classList.remove('primary')

      break
    case 'info':
      var newInfo = Vue.toasted.global.info({
        message: message
      })
      newInfo.el.classList.remove('primary')

      break
    case 'success':
      var newSuccess = Vue.toasted.global.success({
        message: message
      })
      newSuccess.el.classList.remove('primary')

      break
    default:
      console.log('You passed in an unkown $alert type: ' + type)
      var alertProblem = Vue.toasted.global.error()
      alertProblem.el.classList.remove('primary')
  }
}

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  components: { App },
  template: '<App/>'
})
