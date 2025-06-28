<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>القرآن الكريم</ion-title>
        <ion-buttons slot="end">
          <ion-button @click="increaseFontSize" title="تكبير الخط">
            <ion-icon :icon="textOutline" />
          </ion-button>
          <ion-button @click="decreaseFontSize" title="تصغير الخط">
            <ion-icon :icon="textSharp" />
          </ion-button>
          <ion-button @click="toggleTheme" title="الوضع الليلي">
            <ion-icon :icon="isDark ? moon : sunny" />
          </ion-button>
          <ion-button @click="showFontMenu = !showFontMenu" title="تغيير الخط">
            <ion-icon :icon="colorPalette" />
          </ion-button>
          <ion-button router-link="/search">
            <ion-icon slot="icon-only" :icon="searchOutline" />
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
      <ion-toolbar v-if="showFontMenu">
        <ion-segment v-model="fontFamily" @ionChange="saveFont" scrollable>
          <ion-segment-button value="Uthmani">عثماني</ion-segment-button>
          <ion-segment-button value="Amiri">أميري</ion-segment-button>
          <ion-segment-button value="MeQuran">مي قرآن</ion-segment-button>
          <ion-segment-button value="DecoType">زخرفي</ion-segment-button>
          <ion-segment-button value="Hafs">حفص</ion-segment-button>
          <ion-segment-button value="Nabi">رقع</ion-segment-button>
        </ion-segment>
      </ion-toolbar>
    </ion-header>

    <ion-content :style="{ backgroundColor: isDark ? '#333' : '#fff' }">
      <ion-list v-if="surahs.length">
        <ion-item v-for="surah in surahs" :key="surah.number"
          :style="{ fontSize: fontSize + 'px', fontFamily: fontFamily, color: isDark ? 'white' : 'black' }"
          @click="goToSurah(surah)">
          {{ surah.name }}
        </ion-item>
      </ion-list>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { IonContent, IonHeader, IonPage, IonIcon, IonItem, IonTitle, IonSegment, IonSegmentButton, IonToolbar, IonButtons, IonButton, IonList } from "@ionic/vue";
import {
  textOutline,
  textSharp,
  sunny,
  moon,
  colorPalette,
  searchOutline,
} from 'ionicons/icons'
const isDark = ref(false)
const surahs = ref([])
const router = useRouter()

const initData = async () => {
  const res = await fetch('/assets/quran.json');
  const data = await res.json();
  surahs.value = data;
  fontSize.value = parseInt(localStorage.getItem('fontSize')) || 22;
  fontFamily.value = localStorage.getItem('fontFamily') || 'UthmaniFont';
  isDark.value = JSON.parse(localStorage.getItem('isDark')) || false;
  document.documentElement.style.setProperty('--ion-background-color', isDark.value ? '#000' : '#fff');
}

onMounted(initData)

const goToSurah = (surah) => {
  router.push({ name: 'SurahDetail', params: { number: surah.number } })
}

const increaseFontSize = () => {
  fontSize.value += 2
  localStorage.setItem('fontSize', fontSize.value)
}

const decreaseFontSize = () => {
  fontSize.value = Math.max(12, fontSize.value - 2)
  localStorage.setItem('fontSize', fontSize.value)
}

const toggleTheme = () => {
  isDark.value = !isDark.value
  localStorage.setItem('isDark', isDark.value)
}

const saveFont = () => {
  localStorage.setItem('fontFamily', fontFamily.value)
}


const surah = ref(null)
const fontSize = ref(22)
const fontFamily = ref('UthmaniFont')
const showFontMenu = ref(false)
</script>

<style scoped></style>