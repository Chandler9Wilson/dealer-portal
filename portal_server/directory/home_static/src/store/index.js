import Vue from 'vue'
import Vuex from 'vuex'

// Module imports

// The active object e.g. a `Customer` instance
import activeObject from './modules/activeObject'

Vue.use(Vuex)

// See https://vuex.vuejs.org/en/strict.html
const debug = process.env.NODE_ENV !== 'production'

export default new Vuex.Store({
  modules: {
    activeObject
  },
  strict: debug
})
