import Vue from 'vue'
import Router from 'vue-router'

import overview from '../components/overview'
import customer from '../components/customer'
import facility from '../components/facility'
import device from '../components/device'
import newCustomer from '../components/newCustomer'
import newFacility from '../components/newFacility'
import newDevice from '../components/newDevice'
import customerFind from '../components/customerFind'
import facilityFind from '../components/facilityFind'
import deviceFind from '../components/deviceFind'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'overview',
      component: overview
    },
    {
      path: '/customers/new',
      name: 'newCustomer',
      component: newCustomer
    },
    {
      path: '/devices/new',
      name: 'newDevice',
      component: newDevice
    },
    {
      path: '/facilities/new',
      name: 'newfacility',
      component: newFacility
    },
    {
      path: '/customers/:id',
      name: 'customer',
      component: customer
    },
    {
      path: '/facilities/:id',
      name: 'facility',
      component: facility
    },
    {
      path: '/devices/:id',
      name: 'device',
      component: device
    },
    {
      path: '/customers',
      name: 'customers',
      component: customerFind
    },
    {
      path: '/facilities',
      name: 'facilities',
      component: facilityFind
    },
    {
      path: '/devices',
      name: 'devices',
      component: deviceFind
    }
  ]
})
