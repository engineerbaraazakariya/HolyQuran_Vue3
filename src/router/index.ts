import { createRouter, createWebHashHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/list'
  },
  {
  path: '/surah/:surahNumber/:ayahNumber/:pageNumber/:scrollTo?/:isReciting?',
  name: 'SurahDetailFull',
  redirect: to => ({
    name: 'SurahDetail',
    params: {
      pageNumber: to.params.pageNumber
    },
    query: {
      surahNumber: to.params.surahNumber,
      ayahNumber: to.params.ayahNumber !== '0' ? to.params.ayahNumber : undefined,
      isReciting: to.params.isReciting === 'true' ? '1' : undefined
    }
  })
},
{
  path: '/page/:pageNumber',
  name: 'SurahDetail',
  meta: { keepAlive: true },
  component: () => import('@/views/SurahDetail.vue'),
  props: route => ({
    pageNumber: Number(route.params.pageNumber),
    surahNumber: route.query.surahNumber ? Number(route.query.surahNumber) : null,
    ayahNumber: route.query.ayahNumber ? Number(route.query.ayahNumber) : null,
    isReciting: route.query.isReciting === '1'
  })
},
  {
    path: '/search',
    meta: { keepAlive: true },
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
  history: createWebHashHistory(import.meta.env.BASE_URL),
  routes
})

export default router
