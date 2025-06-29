
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView,
    },

    {
      path: '/production_management',
      name: 'management',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/ProductionManagement.vue'),
    },

    {
      path: '/selling',
      name: 'selling',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/SellingView.vue'),
    },

    {
      path: '/:catchAll(.*)',
      name: 'pageNotFind',
      component: () => import('../views/404.vue'),
    },

    {
      path: '/report',
      name: 'Report',
      component: () => import('../views/Report.vue'),
    },

  ],
})

export default router
