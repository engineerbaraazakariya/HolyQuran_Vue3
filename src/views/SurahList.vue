<template>
  <ion-page :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
    <ion-header>
      <TopToolbar :isDark="isDark" title="القرآن الكريم" :showBack="false" :showFontSizeButtons="true"
        :showThemeToggle="true" :showFontSelector="true" :showSearch="true" :showRibbon="false" />

      <IonPopover :is-open="showFontPopover" :event="fontPopoverEvent" @didDismiss="showFontPopover = false"
        style="--backdrop-background: transparent;">
        <ion-list :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
          <ion-item button @click="setFont('Uthmani')" class="!p-2 rounded-md my-1 transition-all" :class="[
            fontFamily === 'Uthmani'
              ? isDark
                ? 'bg-gray-700 text-white ring-2 ring-green-500'
                : 'bg-gray-200 text-black ring-2 ring-green-600'
              : isDark
                ? 'text-white hover:bg-gray-700'
                : 'text-black hover:bg-gray-100'
          ]" :style="{ fontFamily: 'Uthmani' }">
            عثماني
          </ion-item>

          <ion-item button @click="setFont('Amiri')" class="!p-2 rounded-md my-1 transition-all" :class="[
            fontFamily === 'Amiri'
              ? isDark
                ? 'bg-gray-700 text-white ring-2 ring-green-500'
                : 'bg-gray-200 text-black ring-2 ring-green-600'
              : isDark
                ? 'text-white hover:bg-gray-700'
                : 'text-black hover:bg-gray-100'
          ]" :style="{ fontFamily: 'Amiri' }">
            أميري
          </ion-item>

          <ion-item button @click="setFont('MeQuran')" class="!p-2 rounded-md my-1 transition-all" :class="[
            fontFamily === 'MeQuran'
              ? isDark
                ? 'bg-gray-700 text-white ring-2 ring-green-500'
                : 'bg-gray-200 text-black ring-2 ring-green-600'
              : isDark
                ? 'text-white hover:bg-gray-700'
                : 'text-black hover:bg-gray-100'
          ]" :style="{ fontFamily: 'MeQuran' }">
            مي قرآن
          </ion-item>

          <ion-item button @click="setFont('DecoType')" class="!p-2 rounded-md my-1 transition-all" :class="[
            fontFamily === 'DecoType'
              ? isDark
                ? 'bg-gray-700 text-white ring-2 ring-green-500'
                : 'bg-gray-200 text-black ring-2 ring-green-600'
              : isDark
                ? 'text-white hover:bg-gray-700'
                : 'text-black hover:bg-gray-100'
          ]" :style="{ fontFamily: 'DecoType' }">
            زخرفي
          </ion-item>

          <ion-item button @click="setFont('Hafs')" class="!p-2 rounded-md my-1 transition-all" :class="[
            fontFamily === 'Hafs'
              ? isDark
                ? 'bg-gray-700 text-white ring-2 ring-green-500'
                : 'bg-gray-200 text-black ring-2 ring-green-600'
              : isDark
                ? 'text-white hover:bg-gray-700'
                : 'text-black hover:bg-gray-100'
          ]" :style="{ fontFamily: 'Hafs' }">
            حفص
          </ion-item>

          <ion-item button @click="setFont('Nabi')" class="!p-2 rounded-md my-1 transition-all" :class="[
            fontFamily === 'Nabi'
              ? isDark
                ? 'bg-gray-700 text-white ring-2 ring-green-500'
                : 'bg-gray-200 text-black ring-2 ring-green-600'
              : isDark
                ? 'text-white hover:bg-gray-700'
                : 'text-black hover:bg-gray-100'
          ]" :style="{ fontFamily: 'Nabi' }">
            رقع
          </ion-item>

        </ion-list>
      </IonPopover>
    </ion-header>

    <ion-content ref="mainScrollContainer" scroll-events=" true" @ionScroll="saveMainScrollPosition"
      :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
      <ion-list v-if="surahs.length" :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
        <ion-item v-for="surah in surahs" :key="surah.number"
          :style="{ fontSize: fontSize + 'px', fontFamily: fontFamily }" @click="goToSurah(surah)"
          :id="'surah-' + surah.number"
          :class="{ 'last-opened': lastSurah === surah.number, 'dark-theme': isDark, 'white-theme': !isDark }">
          {{ surah.name }}
        </ion-item>
      </ion-list>
      <ion-toast :is-open="toastIsOpen" :message="toastMessage" :duration="2000"
        @didDismiss="toastIsOpen = false"></ion-toast>
    </ion-content>
  </ion-page>
</template>

<script setup>
import TopToolbar from './TopToolbar.vue'
import { provide } from 'vue'
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { IonContent, IonHeader, IonPage, IonItem, IonList, IonToast } from "@ionic/vue";

const isDark = ref(false)
const surahs = ref([])
const router = useRouter()
import { onActivated } from 'vue'

onActivated(async () => {
  console.log('🚀 onActivated fired!')
  await nextTick()
  const savedOffset = localStorage.getItem('mainScrollOffset')
  if (!savedOffset) return

  const el = mainScrollContainer.value?.$el || mainScrollContainer.value
  const scrollEl = await el?.getScrollElement?.()
  if (scrollEl) {
    scrollEl.scrollTo({ top: parseInt(savedOffset), behavior: 'auto' })
  }
})

async function saveMainScrollPosition() {
  const el = mainScrollContainer.value?.$el || mainScrollContainer.value
  const scrollEl = await el?.getScrollElement?.()
  const scrollTop = scrollEl?.scrollTop || 0
  mainScrollOffset.value = scrollEl.scrollTop
  localStorage.setItem('mainScrollOffset', scrollTop.toString())
}
const initData = async () => {
  const res = await fetch('/assets/quran.json');
  const data = await res.json();
  surahs.value = data;
  fontSize.value = parseInt(localStorage.getItem('fontSize')) || 22;
  fontFamily.value = localStorage.getItem('fontFamily') || 'UthmaniFont';
  isDark.value = JSON.parse(localStorage.getItem('isDark')) || false;
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
const showFontPopover = ref(false)
const fontPopoverEvent = ref(null)


function openFontPopover(event) {
  const rect = event.target.getBoundingClientRect();
  fontPopoverEvent.value = {
    clientX: rect.left + rect.width / 2,
    clientY: rect.top + rect.height / 2
  };
  showFontPopover.value = true;
}


import { IonPopover } from '@ionic/vue'
function setFont(font) {
  fontFamily.value = font;
  localStorage.setItem('fontFamily', font);
  showFontPopover.value = false;
}


onMounted(async () => {
  await initData();
  const stored = localStorage.getItem('lastSurah')
  if (stored) {
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

const fontSize = ref(22)
const fontFamily = ref('UthmaniFont')
const mainScrollOffset = ref(0)

provide('increaseFontSize', increaseFontSize)
provide('decreaseFontSize', decreaseFontSize)
provide('toggleTheme', toggleTheme)
provide('openFontPopover', openFontPopover)
provide('isDark', isDark)
</script>

<style scoped>
.last-opened {
  background-color: #cce7ff !important;
  font-weight: bold;
}
</style>