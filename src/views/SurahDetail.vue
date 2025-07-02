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
            <ion-icon :icon="addCircle" />
          </ion-button>
          <ion-button @click="decreaseFontSize" title="تصغير الخط">
            <ion-icon :icon="removeCircle" />
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
      ref="scrollContainer" scroll-events="true" style="overflow-y: auto;">
      <span class="flex flex-wrap justify-around px-2">
        <template v-if="surah">
          <div class="text-center mb-4 flex justify-center items-center w-full" :style="{
            fontSize: fontSize + 'px',
            fontFamily: fontFamily,
            color: isDark ? 'white' : 'black'
          }">
            <span class="relative inline-flex items-center justify-center p-8" :style="{
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
            <span v-for="(word, index) in ayah.text.split(' ')" :key="index" :style="{
              fontSize: fontSize + 'px',
              fontFamily: fontFamily,
              color: isDark ? 'white' : 'black',
              wordSpacing: '0.25em',
              backgroundColor: surahVariables[surah.number]?.longPressedAyahNumber === ayah.numberInSurah ? '#579758' : 'transparent',
              cursor: 'default',
              backgroundColor: surahVariables[surah.number]?.longPressedAyahNumber === ayah.numberInSurah ? '#579758' : 'transparent'
            }" @touchstart="startLongPress($event, surah.number, ayah.numberInSurah)" @touchend="stopLongPress"
              @touchmove="stopLongPress">
              {{ word }}<span class="!w-2 !max-w-2 !min-w-2 flex" :style="{
                backgroundColor: surahVariables[surah.number]?.longPressedAyahNumber === ayah.numberInSurah ? '#579758' : 'transparent'
              }" v-if="index !== ayah.text.split(' ').length - 1"></span>
            </span>
            <span class="relative flex justify-center items-center" :style="{
              minHeight: fontSize / 1.012 + 'px',
              minWidth: fontSize / 1.012 + 'px',
              backgroundImage: `url(/assets/${surahVariables[surah.number]?.bookmarkedAyahNumber === ayah.numberInSurah || surahVariables[surah.number]?.longPress ? 'bookmarked_ayah' : 'end_ayah'}.svg)`,
              backgroundSize: 'contain',
              backgroundRepeat: 'no-repeat',
              backgroundPosition: 'center',
              fontSize: fontSize / 2.75 + 'px',
              width: fontSize / 1.2 + 'px',
              fontWeight: 'bold',
              color: 'black',
            }" @click="toggleAyah(surah.number, ayah.numberInSurah)"
              @contextmenu.prevent="toggleAyah(surah.number, ayah.numberInSurah)">
              <span>
                {{ ayah.numberInSurah }}
              </span>
            </span>
          </template>
        </template>
        <template v-else>
          <p class="ion-padding">جارٍ تحميل السورة...</p>
        </template>
      </span>
      <IonPopover :is-open="showPopover" :event="popoverEvent"
        @didDismiss="surahVariables[selectedSurahNumber].longPressedAyahNumber = null; showPopover = false">
        <ion-list>
          <ion-item button @click="onOption('تفسير')">📖 تفسير</ion-item>
          <ion-item button @click="onOption('ترجمة')">🌐 ترجمة</ion-item>
          <ion-item button @click="onOption()">❌ إلغاء</ion-item>
        </ion-list>
      </IonPopover>


    </ion-content>
    <TafsirModal :is-open="modalOpen" :surah-number="selectedSurah" :ayah-number="selectedAyah" :type="modalType"
      @close="modalOpen = false" />

  </ion-page>
</template>

<script setup>
import TafsirModal from './TafsirModal.vue'

const modalOpen = ref(false)
const selectedSurah = ref(null)
const selectedAyah = ref(null)

import { IonPopover } from '@ionic/vue'
const showPopover = ref(false)
const popoverEvent = ref(null)  // لتخزين حدث النقر لتموضع النافذة
const selectedSurahNumber = ref(null)
const selectedAyahNumber = ref(null)
function onOption(choice) {
  showPopover.value = false
  if (!choice) {
    surahVariables.value[selectedSurahNumber.value].longPressedAyahNumber = null
    return
  }

  if (selectedSurahNumber.value && surahVariables.value[selectedSurahNumber.value]) {
    surahVariables.value[selectedSurahNumber.value].longPressedAyahNumber = null
  }

  if (choice === 'تفسير') {
    selectedSurah.value = selectedSurahNumber.value
    selectedAyah.value = selectedAyahNumber.value
    modalType.value = 'tafsir'
    modalOpen.value = true
  } else if (choice === 'ترجمة') {
    selectedSurah.value = selectedSurahNumber.value
    selectedAyah.value = selectedAyahNumber.value
    modalType.value = 'translation'
    modalOpen.value = true
  }
}

const modalType = ref('tafsir') // أو 'translation'

import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { addCircle, removeCircle } from 'ionicons/icons'

import {
  sunny,
  moon,
  colorPalette,
  searchOutline
} from 'ionicons/icons'
import { IonContent, IonHeader, IonPage, IonIcon, IonBackButton, IonTitle, IonSegment, IonSegmentButton, IonToolbar, IonButtons, IonButton, IonList, IonItem } from "@ionic/vue";
const route = useRoute()
const surahVariables = ref({}) // { '1': {numberInSurah:5, scrollPosition:100}, '2': {numberInSurah:10, scrollPosition:200} }

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


const pressTimer = ref(null)  // لتخزين المؤقت
const longPressThreshold = 200
const isPressing = ref(false)  // حالة الضغط المستمر


const isScrolling = ref(false);  // متغير لتتبع إذا كان المستخدم يمرر

function startLongPress(event, surahNumber, ayahNumber) {
  isPressing.value = true; // بدأ الضغط الطويل
  popoverEvent.value = event;

  pressTimer.value = setTimeout(() => {
    if (isPressing.value && !isScrolling.value) {
      // تأكد من أن الكائن موجود
      if (!surahVariables.value[surahNumber]) {
        surahVariables.value[surahNumber] = { longPressedAyahNumber: null, bookmarkedAyahNumber: null, scrollPosition: null };
      }

      // تعيين قيمة longPressedAyahNumber
      surahVariables.value[surahNumber].longPressedAyahNumber = ayahNumber;

      selectedSurahNumber.value = surahNumber;
      selectedAyahNumber.value = ayahNumber;
      showPopover.value = true;
    }
  }, longPressThreshold);
}


function stopLongPress() {
  isPressing.value = false; // إنهاء الضغط الطويل
  clearTimeout(pressTimer.value);

  // إعادة تعيين حالة التمرير
  isScrolling.value = false;
}

function handleTouchMove(event) {
  if (isPressing.value) {
    isScrolling.value = true; // بدأ التمرير
  }
}


// إضافة مستمع للتمرير أثناء اللمس
function setupTouchEvents(ayahNumber, surahNumber) {
  const element = document.getElementById(`ayah-${surahNumber}-${ayahNumber}`);
  if (element) {
    element.addEventListener('touchstart', (e) => startLongPress(e, surahNumber, ayahNumber));
    element.addEventListener('touchend', stopLongPress);
    element.addEventListener('touchmove', stopLongPress);  // لضمان إلغاء التفاعل عند التحرك
  }
}


async function saveScrollPosition() {
  const el = scrollContainer.value?.$el || scrollContainer.value
  const scrollEl = await el?.getScrollElement?.()
  const scrollTop = scrollEl?.scrollTop || 0

  if (surah.value) {
    if (surahVariables.value[surah.value.number] === undefined) {
      surahVariables.value[surah.value.number] = { bookmarkedAyahNumber: null, scrollPosition: null }
    }
    surahVariables.value[surah.value.number].scrollPosition = scrollTop.toString();
    localStorage.setItem('surahVariables', JSON.stringify(surahVariables.value))
  }
}
function toggleAyah(surahNumber, ayahNumber) {
  const current = surahVariables.value[surahNumber]?.bookmarkedAyahNumber || null
  if (!surahVariables.value[surahNumber]) {
    surahVariables.value[surahNumber] = { bookmarkedAyahNumber: null, scrollPosition: null }
  }

  if (current === ayahNumber) {
    // إلغاء التحديد
    delete surahVariables.value[surahNumber]
  } else {
    // تحديد جديد
    surahVariables.value[surahNumber].bookmarkedAyahNumber = ayahNumber
  }
  localStorage.setItem('surahVariables', JSON.stringify(surahVariables.value))
}

onMounted(async () => {
  const res = await fetch('/assets/quran.json')
  const allSurahs = await res.json()
  const number = parseInt(route.params.number)
  surah.value = allSurahs.find(s => s.number === number)

  fontSize.value = parseFloat(localStorage.getItem('fontSize')) || 22
  fontFamily.value = localStorage.getItem('fontFamily') || 'Uthmani'
  isDark.value = localStorage.getItem('isDark') === 'true'

  const stored = localStorage.getItem('surahVariables')
  if (stored) {
    surahVariables.value = JSON.parse(stored)
  }
  await nextTick()

  // استدعاء دالة setupTouchEvents لكل آية في السورة
  if (surah.value && surah.value.ayahs) {
    surah.value.ayahs.forEach((ayah) => {
      setupTouchEvents(ayah.numberInSurah, surah.value.number)
    });
  }

  const savedSurah = localStorage.getItem('lastSurah')
  const savedOffset = surahVariables.value[surah.value.number]?.scrollPosition || '0'
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
