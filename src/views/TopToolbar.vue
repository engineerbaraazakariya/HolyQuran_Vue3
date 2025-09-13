<template>
  <ion-toolbar :class="[{ 'dark-theme': isDark, 'white-theme': !isDark, 'vertical-toolbar': vertical }]">
    <ion-title v-if="title">{{ title }}</ion-title>

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

    <!-- النسخة العادية (أفقية) -->
    <div v-else class="flex justify-between px-2 horizonal-buttons">
      <ion-buttons slot="start" v-if="showBack">
        <ion-back-button defaultHref="/"></ion-back-button>
      </ion-buttons>

      <ion-buttons slot="end">
        <!-- نفس الأزرار -->
        <ion-button v-if="showFontSizeButtons" @click="increaseFontSize" title="تكبير الخط">
          <ion-icon :icon="addCircle" />
        </ion-button>
        <ion-button v-if="showFontSizeButtons" @click="decreaseFontSize" title="تصغير الخط">
          <ion-icon :icon="removeCircle" />
        </ion-button>
        <ion-button v-if="showThemeToggle" @click="toggleTheme" title="الوضع الليلي">
          <ion-icon :icon="isDark ? moon : sunny" />
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

    <!-- ✅ عنصر اختيار اللغة -->
    <ion-select v-if="showLanguageSelect" v-model="selectedFile" interface="popover" placeholder="اختر ملف">
      <ion-select-option v-for="file in availableOptions" :key="file" :value="file">
        {{ languageDisplay[file] || file.replace('.json', '') }}
      </ion-select-option>
    </ion-select>
  </ion-toolbar>
</template>


<script setup>
import {
  IonToolbar,
  IonButtons,
  IonSelect,
  IonSelectOption,
  IonButton,
  IonIcon,
  IonBackButton,
  IonTitle,
} from '@ionic/vue';

import { addCircle, removeCircle, ribbon, moon, sunny, colorPalette, searchOutline } from 'ionicons/icons'

import { inject } from 'vue'
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
});

// جلب القيم من provide
const increaseFontSize = inject('increaseFontSize')
const decreaseFontSize = inject('decreaseFontSize')
const toggleTheme = inject('toggleTheme')
const openFontPopover = inject('openFontPopover')
const toggleUpperSurahInfo = inject('toggleUpperSurahInfo')
const isDark = inject('isDark')

const selectedFile = inject('selectedFile', null)
const availableOptions = inject('availableOptions', [])
const languageDisplay = inject('languageDisplay', [])

</script>