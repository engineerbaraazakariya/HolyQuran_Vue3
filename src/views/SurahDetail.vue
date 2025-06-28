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

    <ion-content :class="{ 'dark-theme': isDark, 'white-theme': !isDark }" @ionScroll="saveScrollPosition"
      ref="scrollContainer" scroll-events="true">
      <span class="flex flex-wrap justify-around px-2">
        <template v-if="surah">
          <template v-for="ayah in surah.ayahs" :key="ayah.numberInSurah">
            <span v-for="word in ayah.text.split(' ')" :key="word" :style="{
              fontSize: fontSize + 'px',
              fontFamily: fontFamily,
              color: isDark ? 'white' : 'black'
            }">
              {{ word }}&nbsp;
            </span>
            <span class="relative mx-1 flex justify-center items-center" @click="toggleAyah(surah.value?.number, ayah.numberInSurah)"
              @contextmenu.prevent="toggleAyah(surah.value.number, ayah.numberInSurah)">
              <span class="relative inline-flex items-center justify-center" :style="{
                minHeight: fontSize / 1.012 + 'px',
                minWidth: fontSize / 1.012 + 'px',
                backgroundImage: `url(/assets/${selectedAyahs[surah.value?.number] === ayah.numberInSurah ? 'selected_ayah' : 'end_ayah'}.svg)`,
                backgroundSize: 'contain',
                backgroundRepeat: 'no-repeat',
                backgroundPosition: 'center',
                fontSize: fontSize / 2.75 + 'px',
                width: fontSize / 1.2 + 'px',
                height: fontSize / 1.2 + 'px',
                fontWeight: 'bold',
                color: 'black'
              }">
                {{ ayah.numberInSurah }}
              </span>

            </span>
          </template>
        </template>
        <template v-else>
          <p class="ion-padding">جارٍ تحميل السورة...</p>
        </template>
      </span>
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
const selectedAyahs = ref({}) // { '1': 5, '2': 12 } ← سورة 1 الآية 5 محددة، سورة 2 الآية 12

const surah = ref(null)
const fontSize = ref(22)
const fontFamily = ref('Uthmani')
const isDark = ref(false)
const showFontMenu = ref(false)
const scrollContainer = ref(null)



import { useBackButton } from '@ionic/vue';
import router from '@/router';
useBackButton(10, () => {
  router.replace('/');
});

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
function toggleAyah(surahNumber, ayahNumber) {
  const current = selectedAyahs.value[surahNumber]

  if (current === ayahNumber) {
    // إلغاء التحديد
    delete selectedAyahs.value[surahNumber]
  } else {
    // تحديد جديد
    selectedAyahs.value[surahNumber] = ayahNumber
  }

  localStorage.setItem('selectedAyahs', JSON.stringify(selectedAyahs.value))
}

onMounted(async () => {
  const res = await fetch('/assets/quran.json')
  const allSurahs = await res.json()
  const number = parseInt(route.params.number)
  surah.value = allSurahs.find(s => s.number === number)

  fontSize.value = parseFloat(localStorage.getItem('fontSize')) || 22
  fontFamily.value = localStorage.getItem('fontFamily') || 'Uthmani'
  isDark.value = localStorage.getItem('isDark') === 'true'

  const stored = localStorage.getItem('selectedAyahs')
  if (stored) {
    selectedAyahs.value = JSON.parse(stored)
  }

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
