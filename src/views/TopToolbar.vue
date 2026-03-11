<template>
  <ion-toolbar :class="[{ 'dark-theme': isDark, 'white-theme': !isDark, 'vertical-toolbar': vertical }]">
    <ion-title v-if="title">{{ title }}</ion-title>

    <!-- النسخة العمودية -->
    <div v-if="vertical" class="vertical-buttons z-50 flex flex-wrap gap-2">
      <ion-back-button v-if="showBack" defaultHref="/"></ion-back-button>

      <ion-button class="max-w-10" v-if="showSearch" router-link="/search">
        <ion-icon slot="icon-only" :icon="searchOutline" />
      </ion-button>

      <ion-button class="max-w-10" v-if="showFontSizeButtons" @click="increaseFontSize" title="تكبير الخط">
        <ion-icon slot="icon-only" :icon="addCircle" />
      </ion-button>
      <ion-button class="max-w-10" v-if="showFontSizeButtons" @click="decreaseFontSize" title="تصغير الخط">
        <ion-icon slot="icon-only" :icon="removeCircle" />
      </ion-button>

      <ion-button class="max-w-10" v-if="showThemeToggle" @click="toggleTheme" title="الوضع الليلي">
        <ion-icon slot="icon-only" :icon="isDark ? moon : sunny" />
      </ion-button>

      <ion-button class="max-w-10" v-if="showFontSelector" @click="openFontPopover($event)" title="تغيير الخط">
        <ion-icon slot="icon-only" :icon="colorPalette" />
      </ion-button>

      <ion-button class="max-w-10" v-if="showRibbon" @click="toggleUpperSurahInfo">
        <ion-icon :icon="ribbon" />
      </ion-button>

      <ion-button class="max-w-10 !p-0" v-if="showScrollUpButton" @click="scrollToTop" title="أول السورة">
        <ion-icon slot="icon-only" :icon="arrowUpCircleOutline" style="width: 32px; height: 32px;" />
      </ion-button>

      <ion-button class="max-w-10 !p-0" v-if="showScrollDownButton" @click="scrollToBottom" title="أدنى السورة">
        <ion-icon slot="icon-only" :icon="arrowDownCircleOutline" style="width: 32px; height: 32px;" />
      </ion-button>


        <ion-button class="max-w-10 !p-0"  v-if="showNextSurahButton" @click="goToNextSurah" title="السورة التالية">
          <ion-icon  style="width: 32px; height: 32px;"  slot="icon-only" :icon="arrowForwardCircleOutline" />
        </ion-button>

        <ion-button class="max-w-10 !p-0"  v-if="showPreviousSurahButton" @click="goToPreviousSurah" title="السورة السابقة">
          <ion-icon  style="width: 32px; height: 32px;"  slot="icon-only" :icon="arrowBackCircleOutline" />
        </ion-button>

    </div>

    <!-- النسخة الأفقية -->
    <div v-else  class="min-h-8 min-w-4 flex justify-center px-2 horizonal-buttons">
      <ion-buttons slot="start" v-if="showBack">
        <ion-back-button defaultHref="/"></ion-back-button>
      </ion-buttons>

      <ion-buttons slot="end">
        <ion-button v-if="showScrollDownButton" @click="scrollToBottom" title="أدنى السورة">
          <ion-icon :icon="arrowDownCircleOutline" />
        </ion-button>

        <ion-button v-if="showPreviousSurahButton" @click="goToPreviousSurah" title="السورة السابقة">
          <ion-icon :icon="arrowForwardCircleOutline" />
        </ion-button>

        <ion-button v-if="showScrollUpButton" @click="scrollToTop" title="أول السورة">
          <ion-icon :icon="arrowUpCircleOutline" />
        </ion-button>

        <ion-button v-if="showNextSurahButton" @click="goToNextSurah" title="السورة التالية">
          <ion-icon :icon="arrowBackCircleOutline" />
        </ion-button>

        <ion-button v-if="showFontSizeButtons" @click="increaseFontSize" title="تكبير الخط">
          <ion-icon :icon="addCircle" />
        </ion-button>

        <ion-button v-if="showFontSizeButtons" @click="decreaseFontSize" title="تصغير الخط">
          <ion-icon :icon="removeCircle" />
        </ion-button>

        <ion-button v-if="showThemeToggle" @click="toggleTheme" title="الوضع الليلي">
          <ion-icon :icon="!isDark ? moon : sunny" />
        </ion-button>

        <ion-button v-if="showFontSelector" @click="openFontPopover($event)" title="تغيير الخط">
          <ion-icon :icon="colorPalette" />
        </ion-button>

        <ion-button v-if="showSearch" router-link="/search">
          <ion-icon slot="icon-only" :icon="searchOutline" />
        </ion-button>

        <ion-button v-if="showRibbon" @click="toggleUpperSurahInfo">
          <ion-icon :icon="ribbon" />
        </ion-button>
      </ion-buttons>
    </div>

    <!-- قائمة اختيار اللغة -->
    <select v-show="showLanguageSelect" v-model="selectedFile" interface="popover" placeholder="اختر ملف">
      <option v-for="file in availableOptions" :key="file" :value="file">
        {{ languageDisplay[file] || file.replace('.json', '') }}
      </option>
    </select>
  </ion-toolbar>
</template>

<script setup>
import {
  IonToolbar,
  IonButtons,
  IonButton,
  IonIcon,
  IonBackButton,
  IonTitle,
} from '@ionic/vue';

import {
  addCircle, arrowDownCircleOutline,
  arrowUpCircleOutline,arrowForwardCircleOutline,arrowBackCircleOutline, removeCircle, ribbon, moon, sunny, colorPalette, searchOutline
} from 'ionicons/icons'
import { inject, computed, watch } from 'vue';

const props = defineProps({
  title: String,
  isDark: Boolean,
  vertical: Boolean,
  showLanguageSelect: Boolean,
  showBack: Boolean,
  showScrollDownButton: Boolean,
  showScrollUpButton: Boolean,
  showFontSizeButtons: Boolean,
  showPreviousSurahButton: Boolean,
  showNextSurahButton: Boolean,
  showFontSelector: Boolean,
  showThemeToggle: Boolean,
  showSearch: Boolean,
  showRibbon: Boolean,
  selectedFile: String
});

const emit = defineEmits(['update:selectedFile'])

// Injected functions and values
const increaseFontSize = inject('increaseFontSize')
const decreaseFontSize = inject('decreaseFontSize')
const goToNextSurah = inject('goToNextSurah')
const goToPreviousSurah = inject('goToPreviousSurah')
const toggleTheme = inject('toggleTheme')
const openFontPopover = inject('openFontPopover')
const toggleUpperSurahInfo = inject('toggleUpperSurahInfo')
const isDark = inject('isDark')
const availableOptions = inject('availableOptions', [])
const languageDisplay = inject('languageDisplay', [])

// LocalStorage key
const localStorageKey = 'your-key'

// v-model computed
const selectedFile = computed({
  get: () => props.selectedFile,
  set: (value) => emit('update:selectedFile', value)
})
// Scroll to top
const scrollToTop = () => {
  const content = document.querySelector('ion-content')
  if (content && content.scrollToTop) {
    content.scrollToTop(500) // 500ms animation
  } else {
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

// Scroll to bottom
const scrollToBottom = () => {
  const content = document.querySelector('ion-content')
  if (content && content.scrollToBottom) {
    content.scrollToBottom(500)
  } else {
    window.scrollTo({
      top: document.body.scrollHeight,
      behavior: 'smooth'
    })
  }
}

// Watch for saving to localStorage only
watch(selectedFile, (newFile) => {
  if (!newFile) return
  localStorage.setItem(localStorageKey, newFile)
}, { immediate: true })
</script>

<style scoped>
ion-toolbar {
  /* تفعيل stacking context داخل transform */
  transform-style: preserve-3d;
  backface-visibility: hidden;
  z-index: 10;
}

.vertical-buttons,
.horizonal-buttons {
  /* تأكد أن كل العناصر فوقية وتظهر مع التحريك */
  position: relative;
  z-index: 20;
}
</style>
