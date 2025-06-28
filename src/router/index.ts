import { createRouter, createWebHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/list'
  },
  {
    path: '/surah/:number',
    name: 'SurahDetail',
    component: () => import('@/views/SurahDetail.vue'),
    props: route => ({
      number: Number(route.params.number),
      scrollTo: Number(route.params.scrollTo)
    })
  },
  {
    path: '/search',
    name: 'search',
    component: () => import('@/views/SearchPage.vue')
  },
  {
    path: '/list',
    name: 'SurahList',
    component: () => import('@/views/SurahList.vue')
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
