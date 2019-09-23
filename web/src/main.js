import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import axios from './assets/js/axios'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import { faGithub, faLinkedin, faWeixin, faGalacticSenate } from '@fortawesome/free-brands-svg-icons'
import { faPaw, faExternalLinkAlt } from '@fortawesome/free-solid-svg-icons'
library.add(
  faGithub, faLinkedin, faWeixin, faGalacticSenate,
  faPaw, faExternalLinkAlt
)

Vue.prototype.$axios = axios
Vue.component('font-awesome-icon', FontAwesomeIcon)
Vue.config.productionTip = false
Vue.use(ElementUI)

new Vue({
  router,
  render: function (h) { return h(App) }
}).$mount('#app')
