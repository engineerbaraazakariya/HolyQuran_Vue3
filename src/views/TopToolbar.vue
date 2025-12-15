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
    </div>

    <!-- النسخة الأفقية -->
    <div v-else class="flex justify-between px-2 horizonal-buttons">
      <ion-buttons slot="start" v-if="showBack">
        <ion-back-button defaultHref="/"></ion-back-button>
      </ion-buttons>

      <ion-buttons slot="end">
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
    <select v-show="showLanguageSelect" v-model="selectedFile" interface="popover"
      placeholder="اختر ملف">
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

import { addCircle, removeCircle, ribbon, moon, sunny, colorPalette, searchOutline } from 'ionicons/icons'
import { inject, computed, watch } from 'vue';

const props = defineProps({
  title: String,
  isDark: Boolean,
  vertical: Boolean,
  showLanguageSelect: Boolean,
  showBack: Boolean,
  showFontSizeButtons: Boolean,
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

// Watch for saving to localStorage only
watch(selectedFile, (newFile) => {
  console.log('WTCH', newFile, selectedFile.value)
  if (!newFile) return
  localStorage.setItem(localStorageKey, newFile)
}, { immediate: true })
</script>
