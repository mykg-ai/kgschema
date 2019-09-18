import Vue from 'vue'
import Router from 'vue-router'
import Home from './views/Home.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'layout',
      component: () => import('./views/Layout.vue'),
      children: [
        {
          path: '/',
          name: 'home',
          component: Home,
          children: [
            {
              path: '/_search',
              name: 'query',
              component: () => import('./views/Search.vue')
            },
          ]
        },
        {
          path: '/_classify',
          name: 'classify',
          component: () => import('./views/Classify.vue')
        },
        {
          path: '/_about',
          name: 'about'
        },
        {
          path: '/_link',
          name: 'link'
        },
        {
          path: '/:word',
          name: 'word',
          component: () => import('./views/Word.vue')
        }
      ]
    }
  ]
})
