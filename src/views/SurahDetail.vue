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

    <ion-content :class="{ 'dark-theme': isDark }" @ionScroll="saveScrollPosition" ref="scrollContainer"
      scroll-events="true">
      <div>
        <template v-if="surah">
          <span v-for="ayah in surah.ayahs" :key="ayah.numberInSurah">
            <span :style="{
              fontSize: fontSize + 'px',
              fontFamily: fontFamily,
              color: isDark ? 'white' : 'black'
            }">
              {{ ayah.text }}
            </span>
            <span class="px-4" :style="{ color: 'gray', fontSize: fontSize - 2 + 'px' }">
              {{ ayah.numberInSurah }}
            </span>
          </span>
        </template>
        <template v-else>
          <p class="ion-padding">جارٍ تحميل السورة...</p>
        </template>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import {
  textOutline,
  textSharp,
  sunny,
  moon,
  colorPalette,
  searchOutline
} from 'ionicons/icons'
import { IonContent, IonHeader, IonPage, IonIcon, IonItem, IonTitle, IonSegment, IonSegmentButton, IonToolbar, IonButtons, IonButton, IonList } from "@ionic/vue";
const route = useRoute()

const surah = ref(null)
const fontSize = ref(22)
const fontFamily = ref('Uthmani')
const isDark = ref(false)
const showFontMenu = ref(false)
const scrollContainer = ref(null)

async function saveScrollPosition() {
  const el = scrollContainer.value?.$el || scrollContainer.value
  const scrollEl = await el?.getScrollElement?.()
  const scrollTop = scrollEl?.scrollTop || 0

  // console.log('Saving scroll position:', scrollTop)

  if (surah.value) {
    localStorage.setItem('lastSurah', surah.value.number.toString())
    localStorage.setItem('scrollOffset', scrollTop.toString())
  }
}


onMounted(async () => {
  const res = await fetch('/assets/quran.json')
  const allSurahs = await res.json()
  const number = parseInt(route.params.number)
  surah.value = allSurahs.find(s => s.number === number)

  fontSize.value = parseFloat(localStorage.getItem('fontSize')) || 22
  fontFamily.value = localStorage.getItem('fontFamily') || 'Uthmani'
  isDark.value = localStorage.getItem('isDark') === 'true'

  await nextTick()


  const savedSurah = localStorage.getItem('lastSurah')
  const savedOffset = localStorage.getItem('scrollOffset')
  const el = scrollContainer.value?.$el || scrollContainer.value
  const scrollEl = await el?.getScrollElement?.()
  if (savedSurah === surah.value.number.toString() && scrollEl) {
    scrollEl.scrollTo({ top: Number(savedOffset), behavior: 'auto' })
  }
})



// إعدادات المستخدم
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
</script>

<style scoped>
.dark-theme {
  --ion-background-color: #000;
  --ion-text-color: #fff;
}
</style>
