<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>{{ surah?.name }}</ion-title>
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
          <ion-button @click="goToSearch" title="بحث">
            <ion-icon :icon="searchOutline" />
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
      <ion-toolbar v-if="showFontMenu">
        <ion-segment v-model="fontFamily" @ionChange="saveFont">
          <ion-segment-button value="UthmaniFont">عثماني</ion-segment-button>
          <ion-segment-button value="AmiriFont">أميري</ion-segment-button>
          <ion-segment-button value="MeQuranFont">MeQuran</ion-segment-button>
        </ion-segment>
      </ion-toolbar>
    </ion-header>

    <ion-content :class="{ 'dark-theme': isDark }">
      <div v-if="surah">
        <span v-for="ayah in surah.ayahs" :key="ayah.numberInSurah">
          <span :style="{
            fontSize: fontSize + 'px',
            fontFamily: fontFamily,
            color: isDark ? 'white' : 'black'
          }">
            {{ ayah.text }}
          </span>
          <span :style="{ color: 'gray', fontSize: fontSize - 2 + 'px' }"> ۝{{ ayah.numberInSurah }} </span>
        </span>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  textOutline,
  textSharp,
  sunny,
  moon,
  colorPalette,
  searchOutline,
} from 'ionicons/icons'

const route = useRoute()
const router = useRouter()

const surah = ref(null)
const fontSize = ref(22)
const fontFamily = ref('UthmaniFont')
const isDark = ref(false)
const showFontMenu = ref(false)

onMounted(async () => {
  const res = await fetch('/assets/quran.json')
  const allSurahs = await res.json()
  const number = parseInt(route.params.number)
  surah.value = allSurahs.find(s => s.number === number)

  // Load saved settings
  fontSize.value = parseFloat(localStorage.getItem('fontSize')) || 22
  fontFamily.value = localStorage.getItem('fontFamily') || 'UthmaniFont'
  isDark.value = localStorage.getItem('isDark') === 'true'
})

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

const goToSearch = () => {
  // لاحقاً بنعمل صفحة بحث منفصلة
  alert('ميزة البحث قيد الإنشاء 🔍')
}
</script>

<style scoped>
.dark-theme {
  --ion-background-color: #000;
  --ion-text-color: #fff;
}
</style>
