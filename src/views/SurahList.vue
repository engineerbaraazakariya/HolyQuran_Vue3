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

    <ion-content :class="{ 'dark-theme': isDark, 'white-theme': !isDark }" ref="mainScrollContainer"
      scroll-events=" true" @ionScroll="saveMainScrollPosition">
      <ion-list v-if="surahs.length">
        <ion-item v-for="surah in surahs" :key="surah.number"
          :style="{ fontSize: fontSize + 'px', fontFamily: fontFamily, color: isDark ? 'white' : 'black' }"
          @click="goToSurah(surah)" :id="'surah-' + surah.number"
          :class="{ 'last-opened': lastSurah === surah.number }">
          {{ surah.name }}
        </ion-item>
      </ion-list>
      <ion-toast :is-open="toastIsOpen" :message="toastMessage" :duration="2000"
        @didDismiss="toastIsOpen = false"></ion-toast>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { IonContent, IonHeader, IonPage, IonIcon, IonItem, IonTitle, IonSegment, IonSegmentButton, IonToolbar, IonButtons, IonButton, IonList, IonToast } from "@ionic/vue";
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
async function saveMainScrollPosition() {
  const el = mainScrollContainer.value?.$el || mainScrollContainer.value
  const scrollEl = await el?.getScrollElement?.()
  const scrollTop = scrollEl?.scrollTop || 0
  localStorage.setItem('mainScrollOffset', scrollTop.toString())
}
const initData = async () => {
  const res = await fetch('/assets/quran.json');
  const data = await res.json();
  surahs.value = data;
  fontSize.value = parseInt(localStorage.getItem('fontSize')) || 22;
  fontFamily.value = localStorage.getItem('fontFamily') || 'UthmaniFont';
  isDark.value = JSON.parse(localStorage.getItem('isDark')) || false;
  document.documentElement.style.setProperty('--ion-background-color', isDark.value ? '#000' : '#fff');
}

let lastBackPressed = -1, toastMessage = ref(''), toastIsOpen = ref(false);

useBackButton(10, () => {
  if (lastBackPressed + 2000 >= Date.now()) {
    App.exitApp();
  } else {
    toastIsOpen.value = true;
    toastMessage.value = 'اضغط مرة أخرى للخروج';
    lastBackPressed = Date.now();
  }
});
import { useBackButton } from '@ionic/vue';
import { App } from '@capacitor/app';

const lastSurah = ref(null)

const mainScrollContainer = ref(null)

onMounted(async () => {
  await initData();
  const stored = localStorage.getItem('lastSurah')
  if (stored.length > 0) {
    lastSurah.value = parseInt(stored)
  }

  await nextTick();

  const savedMainOffset = localStorage.getItem('mainScrollOffset')

  setTimeout(async () => {
    const el = mainScrollContainer.value?.$el || mainScrollContainer.value;
    const scrollEl = await el?.getScrollElement?.();
    if (scrollEl && savedMainOffset) {
      scrollEl.scrollTo({ top: Number(savedMainOffset), behavior: 'auto' });
    } else {
      console.warn("scrollEl not found or no offset");
    }
  }, 300);
})

const goToSurah = (surah) => {
  lastSurah.value = surah.number
  localStorage.setItem('lastSurah', surah.number.toString())
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

<style scoped>
.last-opened {
  background-color: #cce7ff !important;
  font-weight: bold;
}
</style>