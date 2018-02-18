import Vue from 'vue'
import Router from 'vue-router'

import customerFind from '../components/customerFind'
import facilityFind from '../components/facilityFind'
import deviceFind from '../components/deviceFind'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/customer',
      name: 'customer',
      component: customerFind
    },
    {
      path: '/facility',
      name: 'facility',
      component: facilityFind
    },
    {
      path: '/device',
      name: 'device',
      component: deviceFind
    }
  ]
})
