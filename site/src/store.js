import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

import axios from "axios";

export default new Vuex.Store({
  state: {
    thedata: undefined
  },
  getters: {
    loaded: (state) => state.thedata !== undefined,
    users: (state) => state.thedata ? state.thedata.users : [],
    dates: (state) => state.thedata ? state.thedata.dates : [],
    thedata: (state) => state.thedata
  },
  mutations: {
    save(state, thedata) {
      state.thedata = thedata
    }
  },
  actions: {
    fetchTheData(context) {
      axios.get('./site-data.json').then(response => {
        context.commit('save', response.data);
      });
    }
  }
})
