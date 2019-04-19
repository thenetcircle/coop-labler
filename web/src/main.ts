import Vue from 'vue'
import './plugins/vuetify'
import './plugins/vuetify'
import App from './App.vue'
import axios from 'axios'
import v4 from 'uuid'

Vue.config.productionTip = false

new Vue({
  render: (h) => h(App),
}).$mount('#app')
