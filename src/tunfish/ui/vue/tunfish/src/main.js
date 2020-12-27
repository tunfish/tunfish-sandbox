import Vue from 'vue'
import Vuex from 'vuex'
import VueMaterial from 'vue-material'
import 'vue-material/dist/vue-material.min.css'
import App from './App.vue'
import {tf_functions} from './js/tf_functions.js'


Vue.config.productionTip = false
Vue.use(VueMaterial)
Vue.use(Vuex)

Vue.prototype.$tf_functions = tf_functions

const store = new Vuex.Store({
  state: {
    session: null
  },
  mutations: {
    doConnection () {
      console.log('inside mutation doConnection')
      console.log(this.state.session)
      const autobahn = require('autobahn')
      const connection = new autobahn.Connection({url: 'ws://172.16.42.2:9000/ws', realm: 'tf_cb_router'})

      connection.onopen = function(new_session) {
        //this.$tf_variables.session = new_session;
        //tf_variables.session = new_session
        console.log('inside onopen')
        store.state.session = new_session
      }

      connection.onopen()
      console.log(this.state.session)
    }
  }
})

new Vue({
  render: h => h(App),
  store: store,
}).$mount('#app')