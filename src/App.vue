<template>
  <ion-app class="!mt-8">
    <router-view v-slot="{ Component, route }">
      <keep-alive :max="3">
        <component :is="Component" :key="route.path.includes('/surah/') ? route.fullPath : route.path" />
      </keep-alive>
    </router-view>
  </ion-app>
</template>

<script setup lang="ts">
import { IonApp, IonRouterOutlet } from '@ionic/vue';
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
onMounted(() => {
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
  font-family: 'GoldenLotus';
  src: url('/assets/fonts/AAAGoldenLotus_Stg1_Ver1_Regular.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}
@font-face {
  font-family: 'Kamel_med';
  src: url('/assets/fonts/Kamel_med.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'Amiri';
  src: url('/assets/fonts/AmiriQuran-Regular.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'Deco_Type';
  src: url('/assets/fonts/Deco_Type.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'KFGQPC';
  src: url('/assets/fonts/KFGQPC_Uthman_Taha_Naskh_Regular.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'Muhammadi';
  src: url('/assets/fonts/MUHAMMADI_QURANIC_FONT.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'MeQuran';
  src: url('/assets/fonts/MeQuran.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}


@font-face {
  font-family: 'Nabi';
  src: url('/assets/fonts/Nabi.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'Sada';
  src: url('/assets/fonts/Sada-Regular_.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'Samim';
  src: url('/assets/fonts/Samim_Regular.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'MyLotus';
  src: url('/assets/fonts/mylotus_Regular.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
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
</style>