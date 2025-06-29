<template>
  <ion-page :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
    <ion-header>
      <ion-toolbar :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
        <ion-buttons slot="start">
          <ion-back-button defaultHref="/list"></ion-back-button>
        </ion-buttons>
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
      <ion-toolbar v-if="showFontMenu" :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
        <ion-segment v-model="fontFamily" @ionChange="saveFont" scrollable
          :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
          <ion-segment-button :class="{ 'dark-theme': isDark, 'white-theme': !isDark }"
            value="Uthmani">عثماني</ion-segment-button>
          <ion-segment-button :class="{ 'dark-theme': isDark, 'white-theme': !isDark }"
            value="Amiri">أميري</ion-segment-button>
          <ion-segment-button :class="{ 'dark-theme': isDark, 'white-theme': !isDark }" value="MeQuran">مي
            قرآن</ion-segment-button>
          <ion-segment-button :class="{ 'dark-theme': isDark, 'white-theme': !isDark }"
            value="DecoType">زخرفي</ion-segment-button>
          <ion-segment-button :class="{ 'dark-theme': isDark, 'white-theme': !isDark }"
            value="Hafs">حفص</ion-segment-button>
          <ion-segment-button :class="{ 'dark-theme': isDark, 'white-theme': !isDark }"
            value="Nabi">رقع</ion-segment-button>
        </ion-segment>
      </ion-toolbar>
    </ion-header>

    <ion-content :class="{ 'dark-theme': isDark, 'white-theme': !isDark }" @ionScroll="saveScrollPosition"
      ref="scrollContainer" scroll-events="true">
      <span class="flex flex-wrap justify-around px-2">
        <template v-if="surah">
          <div class="text-center mb-4 flex justify-center items-center w-full mt-2" :style="{
              fontSize: fontSize + 'px',
              fontFamily: fontFamily,
              color: isDark ? 'white' : 'black'
            }">
            <span class="relative inline-flex items-center justify-center" :style="{
              minHeight: fontSize / 1.012 + 'px',
              minWidth: '100%',
              backgroundImage: `url(/assets/surah_name_frame.png)`,
              backgroundSize: 'auto',
              backgroundRepeat: 'no-repeat',
              backgroundPosition: 'center',
              fontSize: fontSize + 'px',
              Width: '100%',
              height: fontSize / 1.2 + 'px',
              fontWeight: 'bold',
              color: isDark ? 'white' : 'black'
            }">
              {{ surah.name }}
            </span>
          </div>
          <div v-if="![1, 9].includes(surah.number)"
            class="text-center mb-4 flex justify-center items-center w-full mt-2" :style="{
              fontSize: fontSize + 'px',
              fontFamily: fontFamily,
              color: isDark ? 'white' : 'black'
            }">
            ﷽
          </div>
          <template v-for="ayah in surah.ayahs" :key="ayah.numberInSurah">
            <span v-for="word in ayah.text.split(' ')" :key="word" :style="{
              fontSize: fontSize + 'px',
              fontFamily: fontFamily,
              color: isDark ? 'white' : 'black'
            }">
              {{ word }}&nbsp;
            </span>
            <span class="relative mx-1 flex justify-center items-center"
              @click="toggleAyah(surah.number, ayah.numberInSurah)"
              @contextmenu.prevent="toggleAyah(surah.number, ayah.numberInSurah)">
              <span class="relative inline-flex items-center justify-center" :style="{
                minHeight: fontSize / 1.012 + 'px',
                minWidth: fontSize / 1.012 + 'px',
                backgroundImage: `url(/assets/${selectedAyahs[surah.number]?.selectedAyahNumber === ayah.numberInSurah ? 'selected_ayah' : 'end_ayah'}.svg)`,
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
import { IonContent, IonHeader, IonPage, IonIcon, IonBackButton, IonTitle, IonSegment, IonSegmentButton, IonToolbar, IonButtons, IonButton, IonList } from "@ionic/vue";
const route = useRoute()
const selectedAyahs = ref({}) // { '1': {numberInSurah:5, scrollPosition:100}, '2': {numberInSurah:10, scrollPosition:200} }

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

  if (surah.value) {
    if (selectedAyahs.value[surah.value.number] === undefined) {
      selectedAyahs.value[surah.value.number] = { selectedAyahNumber: null, scrollPosition: null }
    }
    selectedAyahs.value[surah.value.number].scrollPosition = scrollTop.toString();
    localStorage.setItem('selectedAyahs', JSON.stringify(selectedAyahs.value))
  }
}
function toggleAyah(surahNumber, ayahNumber) {
  const current = selectedAyahs.value[surahNumber]?.selectedAyahNumber || null
  if (!selectedAyahs.value[surahNumber]) {
    selectedAyahs.value[surahNumber] = { selectedAyahNumber: null, scrollPosition: null }
  }

  if (current === ayahNumber) {
    // إلغاء التحديد
    delete selectedAyahs.value[surahNumber]
  } else {
    // تحديد جديد
    selectedAyahs.value[surahNumber].selectedAyahNumber = ayahNumber
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
  const savedOffset = selectedAyahs.value[surah.value.number]?.scrollPosition || '0'
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
