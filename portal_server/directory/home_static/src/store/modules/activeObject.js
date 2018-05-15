// HTTP client
import axios from 'axios'

// initial state
const state = {
  loadedObject: null,
  model: null,
  loading: null,
  error: null
}

const getters = {
  activeObject: state => {
    if (state.loading || state.error) {
      return null
    } else {
      return state.loadedObject
    }
  }
}

const actions = {
  // see https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment for {} in the params
  getNewActive ({ commit, state }, url) {
    state.loading = true

    axios.get(url)
      .then(response => {
        commit('setLoadedObject', response)
      })
      .catch(error => {
        // TODO possibly call a toast?
        console.log(error)
      })
  }
}

const mutations = {
  setLoadedObject (state, payload) {
    state.loadedObject = payload
  }
}

export default {
  state,
  getters,
  actions,
  mutations
}
