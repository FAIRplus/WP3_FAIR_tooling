import Vue from 'vue'
import App from './App.vue'
import router from './router'
import {BootstrapVue, IconsPlugin, PaginationPlugin} from 'bootstrap-vue'
import vuetify from './plugins/vuetify'
import './plugins/vuetify'


Vue.use(BootstrapVue)
Vue.use(IconsPlugin)
Vue.use(PaginationPlugin)

Vue.config.productionTip = false

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
