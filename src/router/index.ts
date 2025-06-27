import { createRouter, createWebHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';
import SurahListView from '../views/SurahList.vue'
import SurahDetailView from '../views/SurahDetail.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/list'
  },
  {
    path: '/surah/:number',
    name: 'SurahDetail',
    component: SurahDetailView
  },
  {
    path: '/list',
    name: 'SurahList',
    component: SurahListView
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
