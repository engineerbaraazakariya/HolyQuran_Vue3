<template>
  <ion-app :class="{ 'isApp': isApp }">
    <router-view v-slot="{ Component, route }">
      <keep-alive :max="10">
        <component :is="Component" :key="route.path.includes('/surah/') ? route.path : route.path" />
      </keep-alive>
    </router-view>
  </ion-app>
</template>

<script setup lang="ts">
import { IonApp } from '@ionic/vue';
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
let isApp = false;
onMounted(() => {
  isApp = document.getElementsByTagName('html')[0].classList.contains('plt-mobile');
  // !document.URL.startsWith('http') || document.URL.startsWith('http://localhost');
  const lastSurah = localStorage.getItem('lastSurah')
  const stored = JSON.parse(localStorage.getItem('surahVariables') + '');
  if (stored && lastSurah && stored[Number(lastSurah)]) {
    router.replace({
      name: 'SurahDetail',
      params: {
        number: Number(lastSurah),
        scrollTo: stored[Number(lastSurah)].scrollPosition,
      },
    })
  }
})


</script>


<style>
@font-face {
  font-family: "UthmanicHafs_V22";
  src: url("@@/assets/fonts/uthmanic_hafs_v22.ttf") format("truetype");
}

@font-face {
  font-family: "UthmanTSVer1";
  src: url("@@/assets/fonts/UthmanTSVer1.ttf") format("truetype");
}

@font-face {
  font-family: "Mushaf_Font_7";
  src: url("@@/assets/fonts/خط المصحف(7).ttf") format("truetype");
}


.dark-theme {
  --ion-background-color: #000 !important;
  --background: #000 !important;
  background: #000 !important;
  --ion-text-color: #fff !important;
  --color: #fff !important;
  color: #fff !important;
  fill: #fff !important;
}

.white-theme {
  --ion-background-color: #fff !important;
  --background: #fff !important;
  background: #fff !important;
  --ion-text-color: #000 !important;
  --color: #000 !important;
  color: #000 !important;
  fill: #000 !important;
}

/* إضافة هذا في الـ <style> */
.ltr-text {
  direction: ltr;
  text-align: left;
}

.rtl-text {
  direction: rtl;
  text-align: right;
}

/* Hide scrollbar for Chrome, Safari and Opera */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}

/* Hide scrollbar for IE, Edge and Firefox */
.no-scrollbar {
  -ms-overflow-style: none;
  /* IE and Edge */
  scrollbar-width: none;
  /* Firefox */
}

.android .ion-app {
  margin-top: 2rem !important;
}

.android body {
  max-height: calc(100vh - 2rem) !important;
}
</style>