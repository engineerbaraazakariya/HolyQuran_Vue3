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
  font-family: "Arabic Regular";
  src: url("@@/assets/fonts/Arabic Regular.ttf") format("truetype");
}

@font-face {
  font-family: "FS_Arabic Regular";
  src: url("@@/assets/fonts/FS_Arabic Regular.ttf") format("truetype");
}

@font-face {
  font-family: "KFGQPC Uthman Taha Naskh Regular";
  src: url("@@/assets/fonts/KFGQPC Uthman Taha Naskh Regular.ttf") format("truetype");
}

@font-face {
  font-family: "Kamel_med";
  src: url("@@/assets/fonts/Kamel_med.otf") format("truetype");
}

@font-face {
  font-family: "MUHAMMADI_QURANIC_FONT";
  src: url("@@/assets/fonts/MUHAMMADI_QURANIC_FONT.ttf") format("truetype");
}

@font-face {
  font-family: "Nabi";
  src: url("@@/assets/fonts/Nabi.ttf") format("truetype");
}

@font-face {
  font-family: "Sada_Regular";
  src: url("@@/assets/fonts/Sada-Regular_.ttf") format("truetype");
}

@font-face {
  font-family: "Samim_Regular";
  src: url("@@/assets/fonts/Samim_Regular.ttf") format("truetype");
}

@font-face {
  font-family: "UthmanTNB";
  src: url("@@/assets/fonts/UthmanTNB_v2-0.ttf") format("truetype");
}

@font-face {
  font-family: "UthmanTN";
  src: url("@@/assets/fonts/UthmanTN_v2-0.ttf") format("truetype");
}

@font-face {
  font-family: "mylotus_Regular";
  src: url("@@/assets/fonts/mylotus_Regular.ttf") format("truetype");
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

.plt-mobile {
  margin-top: 2rem !important;
}
.plt-mobile body {
  max-height: calc(100vh - 2rem) !important;
}
</style>