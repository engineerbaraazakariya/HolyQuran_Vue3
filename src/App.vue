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
  font-family: "AlQuranAli";
  src: url("assets/fonts/AlQuranAli-L3A83.ttf") format("truetype");
}

@font-face {
  font-family: "Arabic";
  src: url("assets/fonts/Arabic Regular.ttf") format("truetype");
}

@font-face {
  font-family: "FS_Arabic";
  src: url("assets/fonts/FS_Arabic Regular.ttf") format("truetype");
}

@font-face {
  font-family: "KFGQPCUthmanTaha";
  src: url("assets/fonts/KFGQPC Uthman Taha Naskh Regular.ttf") format("truetype");
}

@font-face {
  font-family: "KFGQPCDot";
  src: url("assets/fonts/KFGQPCDotFont.otf") format("opentype");
}

@font-face {
  font-family: "Kamel";
  src: url("assets/fonts/Kamel_med.otf") format("opentype");
}

@font-face {
  font-family: "MuhammadiQuranic";
  src: url("assets/fonts/MUHAMMADI_QURANIC_FONT.ttf") format("truetype");
}

@font-face {
  font-family: "Outlined";
  src: url("assets/fonts/Outlinedv001.otf") format("opentype");
}

@font-face {
  font-family: "Sada";
  src: url("assets/fonts/Sada-Regular_.ttf") format("truetype");
}

@font-face {
  font-family: "Samim";
  src: url("assets/fonts/Samim_Regular.ttf") format("truetype");
}

@font-face {
  font-family: "UthmanTNB";
  src: url("assets/fonts/UthmanTNB_v2-0.ttf") format("truetype");
}

@font-face {
  font-family: "UthmanTN";
  src: url("assets/fonts/UthmanTN_v2-0.ttf") format("truetype");
}

@font-face {
  font-family: "UthmanTSB";
  src: url("assets/fonts/UthmanTSBVer1.ttf") format("truetype");
}

@font-face {
  font-family: "UthmanTS";
  src: url("assets/fonts/UthmanTSVer1.ttf") format("truetype");
}

@font-face {
  font-family: "Zakhrfa";
  src: url("assets/fonts/Zakhrfa.ttf") format("truetype");
}

@font-face {
  font-family: "ZakhrfaOutline";
  src: url("assets/fonts/ZakhrfaOutline.ttf") format("truetype");
}

@font-face {
  font-family: "MyLotus";
  src: url("assets/fonts/mylotus_Regular.ttf") format("truetype");
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