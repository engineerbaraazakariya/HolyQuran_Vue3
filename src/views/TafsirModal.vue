<template>
  <ion-modal :is-open="isOpen" @didDismiss="emit('close')" :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
    <ion-header>
      <ion-toolbar :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
        <ion-title>
          {{ props.type === 'tafsir' ? 'التفسير' : 'الترجمة' }}
        </ion-title>
        <ion-buttons slot="end">
          <ion-button @click="emit('close')">إغلاق</ion-button>
        </ion-buttons>
      </ion-toolbar>

      <!-- أزرار تكبير الخط، تصغير الخط، الوضع الليلي، تغيير الخط -->

      <TopToolbar v-model:selectedFile="selectedFile" :showBack="false" :showFontSizeButtons="true"
        :showFontSelector="true" :showSearch="false" :showLanguageSelect="true" />
    </ion-header>
    <ion-content class="ion-padding" :style="{ fontSize: fontSize + 'px', fontFamily: fontFamily }">
      <div v-if="isLoading">جارٍ التحميل...</div>
      <div v-else>
        <div :class="contentClass" v-if="props.type === 'tafsir'" v-html="content" />
        <div :class="contentClass" v-else>{{ content }}</div>
      </div>
      <IonPopover :is-open="showFontPopover" :event="fontPopoverEvent" @didDismiss="showFontPopover = false"
        style="--backdrop-background: transparent; max-height: 80vh;">
        <ion-content :scroll-y="true">
          <ion-list class="max-h-[70vh] overflow-y-auto" :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
            <ion-item v-for="font in fonts" :key="font.value" button @click="setFont(font.value)"
              class="!p-2 rounded-md my-1 transition-all" :class="[
                fontFamily === font.value
                  ? isDark
                    ? 'bg-gray-700 text-white ring-2 ring-green-500'
                    : 'bg-gray-200 text-black ring-2 ring-green-600'
                  : isDark
                    ? 'text-white hover:bg-gray-700'
                    : 'text-black hover:bg-gray-100'
              ]" :style="{ fontFamily: font.value }">
              {{ font.label }}
            </ion-item>
          </ion-list>
        </ion-content>
      </IonPopover>
    </ion-content>
  </ion-modal>
</template>

<script setup>

import TopToolbar from './TopToolbar.vue'
import { ref, computed, watch, provide } from 'vue'
import { IonModal, IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonButton, IonList, IonItem } from "@ionic/vue";
import { fonts, languageDisplay, tafsirOptions, translationOptions } from '@/composables/fonts.ts'
import { onMounted } from 'vue';



// تعريف props
const props = defineProps({
  type: String,
  surahNumber: Number,
  ayahNumber: Number,
  isOpen: Boolean,
  selectedFile: String // الجديد!
})

// أسماء الملفات المفضلة بشكل تلقائي
const DEFAULT_TAFSIR = 'tabary.json'
const DEFAULT_TRANSLATION = 'en_sahih.json'


// عند تغيير نوع المحتوى (تفسير/ترجمة)
watch(() => props.type, () => {
  const saved = localStorage.getItem(localStorageKey.value)
  selectedFile.value = saved || (props.type === 'tafsir' ? DEFAULT_TAFSIR : DEFAULT_TRANSLATION)
})


const emit = defineEmits(['close', 'update:selectedFile'])

const availableOptions = computed(() =>
  props.type === 'tafsir' ? tafsirOptions : translationOptions
)

// مفتاح لتخزين البيانات في localStorage
const localStorageKey = computed(() =>
  props.type === 'tafsir' ? 'preferredTafsir' : 'preferredTranslation'
)

const localStorageKeyFontSize = 'TafsirFontSize';
const localStorageKeyFontFamily = 'TafsirFontFamily';

onMounted(() => {
  // استرجاع الإعدادات المحفوظة من localStorage
  fontSize.value = JSON.parse(localStorage.getItem(localStorageKeyFontSize)) || 22;
  fontFamily.value = localStorage.getItem(localStorageKeyFontFamily) || 'Uthmani';

  // تحميل الحالة المظلمة
  isDark.value = JSON.parse(localStorage.getItem('isDark')) || false;

  // في حال كان الـ selectedFile فارغًا، قم بتعيين التفسير الافتراضي.
  if (!selectedFile.value) {
    selectedFile.value = (props.type === 'tafsir' ? DEFAULT_TAFSIR : DEFAULT_TRANSLATION)
  }

  loadFileContent(props.surahNumber, props.ayahNumber, props.isOpen, selectedFile.value);

});
let selectedFile = ref(props.selectedFile || (props.type === 'tafsir' ? DEFAULT_TAFSIR : DEFAULT_TRANSLATION));


// حفظ الملف المختار تلقائياً عند تغييره
watch(selectedFile, (newFile) => {
  console.log('Selected file changed:', newFile)
  loadFileContent(props.surahNumber, props.ayahNumber, props.isOpen, newFile);
  if (newFile) {
    localStorage.setItem(localStorageKey.value, newFile)
  }
})

// تحميل المحتوى عند تغيير أحد المتغيرات
const content = ref('')
const isLoading = ref(false)

const contentClass = computed(() => {
  // إذا كانت الترجمة هي الإنجليزية أو أي لغة من اليسار لليمين
  const ltrLanguages = ['en_sahih.json', 'en_tafheem.json', 'fr_hamidullah.json', 'de_bubenheim.json', 'it_piccardo.json', 'es_navio.json', 'sv_bernstrom.json', 'pt_elhayek.json', 'nl_siregar.json', 'in_indonesian.json', 'id_indonesian.json', 'ms_basmeih.json', 'zh_jian.json', 'ru_russian.json', 'ru_kuliev.json', 'tr_diyanet.json', 'bn_bengali.json', 'ha_gumi.json', 'ta_tamil.json', 'th_thai.json', 'ml_abdulhameed.json', 'uz_sodik.json', 'bosnian.json', 'bs_korkut.json', 'so_abduh.json', 'sq_nahi.json', 'sw_barwani.json'];

  // إذا كانت اللغة الإنجليزية أو أي من اللغات LTR
  const classTextDirection = ltrLanguages.includes(selectedFile.value) ? 'ltr-text' : 'rtl-text';

  return {
    classTextDirection,
  };
})


watch(() => [props.surahNumber, props.ayahNumber, props.isOpen, props.selectedFile], async ([sura, aya, open, file]) => {
  await loadFileContent(sura, aya, open, file);
})


const loadFileContent = async (sura, aya, open, file) => {
  if (open && sura && aya && file) {
    isLoading.value = true
    const folder = props.type === 'tafsir' ? 'tafasir' : 'tarajem'
    try {
      console.log('loading content for', `assets/${folder}/${file}`)
      const res = await fetch(`assets/${folder}/${file}`)
      if (!res.ok) {
        throw new Error('حدث خطأ في تحميل البيانات')
      }
      const data = await res.json()
      const match = data.find(item => item.sura === sura && item.aya === aya)
      content.value = match ? match.text : 'لم يتم العثور على المحتوى.'
    } catch (err) {
      content.value = 'حدث خطأ أثناء تحميل المحتوى.'
      console.error(err)
    } finally {
      isLoading.value = false
    }
  }
}

watch(() => props.selectedFile, (newVal) => {
  console.log('selectedFile changed in modal:', newVal)
  if (newVal) {
    localStorage.setItem(localStorageKey.value, newVal)
  }
})
// تم تكرار الكود الخاص بالأزرار هنا
const isDark = ref(true);
const fontSize = ref(22);
const fontFamily = ref('Uthmani');

const increaseFontSize = () => {
  fontSize.value += 2;
  localStorage.setItem(localStorageKeyFontSize, fontSize.value);  // تخزين الحجم المشترك
};

const decreaseFontSize = () => {
  fontSize.value = Math.max(12, fontSize.value - 2);
  localStorage.setItem(localStorageKeyFontSize, fontSize.value);  // تخزين الحجم المشترك
};

function setFont(font) {
  fontFamily.value = font;
  localStorage.setItem(localStorageKeyFontFamily, font);
  showFontPopover.value = false;
}

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

// توفيرهم للمكون الفرعي
provide('selectedFile', selectedFile)
provide('setFont', setFont)
provide('availableOptions', availableOptions)
provide('languageDisplay', languageDisplay)
provide('increaseFontSize', increaseFontSize)
provide('decreaseFontSize', decreaseFontSize)
provide('openFontPopover', openFontPopover)
provide('isDark', isDark)
</script>
