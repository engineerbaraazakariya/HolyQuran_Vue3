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

      <TopToolbar :showBack="false" :showFontSizeButtons="true" :showFontSelector="true" :showSearch="false"
        :showLanguageSelect="true" />
    </ion-header>
    <ion-content class="ion-padding" :style="{ fontSize: fontSize + 'px', fontFamily: fontFamily }">
      <div v-if="isLoading">جارٍ التحميل...</div>
      <div v-else>
        <div :class="contentClass" v-if="props.type === 'tafsir'" v-html="content" />
        <div :class="contentClass" v-else>{{ content }}</div>
      </div>
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
    </ion-content>
  </ion-modal>
</template>

<script setup>

import TopToolbar from './TopToolbar.vue'
import { ref, computed, watch, provide } from 'vue'
import { IonModal, IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonButton, IonIcon, IonSelect, IonSelectOption, IonSegmentButton, IonSegment } from "@ionic/vue";
import {
  addCircle,
  removeCircle,
  sunny,
  moon,
  colorPalette,
} from 'ionicons/icons'
import { onMounted } from 'vue';


const languageDisplay = {
  'in_indonesian.json': '🇮🇩 الإندونيسية 1',
  'id_indonesian.json': '🇮🇩 الإندونيسية 2',
  'ru_russian.json': '🇷🇺 الروسية 1',
  'ru_kuliev.json': '🇷🇺 الروسية 2',
  'en_tafheem.json': '🇵🇰 الإنجليزية (تفهيم)',
  'en_sahih.json': '🇺🇸 الإنجليزية (صحيح)',
  'nl_siregar.json': '🇳🇱 الهولندية',
  'pr_tagi.json': '🇮🇷 الفارسية',
  'bn_bengali.json': '🇧🇩 البنغالية',
  'pt_elhayek.json': '🇵🇹 البرتغالية',
  'bs_korkut.json': '🇧🇦 البوسنية',
  'de_bubenheim.json': '🇩🇪 الألمانية',
  'so_abduh.json': '🇸🇴 الصومالية',
  'sq_nahi.json': '🇦🇱 الألبانية',
  'es_navio.json': '🇪🇸 الإسبانية',
  'sv_bernstrom.json': '🇸🇪 السويدية',
  'fr_hamidullah.json': '🇫🇷 الفرنسية',
  'sw_barwani.json': '🇹🇿 السواحلية',
  'ha_gumi.json': '🇳🇬 الهوسا',
  'ta_tamil.json': '🇮🇳 التاميلية',
  'th_thai.json': '🇹🇭 التايلاندية',
  'it_piccardo.json': '🇮🇹 الإيطالية',
  'tr_diyanet.json': '🇹🇷 التركية',
  'ku_asan.json': '🇮🇶 الكردية',
  'ur_jalandhry.json': '🇵🇰 الأردية',
  'ml_abdulhameed.json': '🇮🇳 الماليالامية',
  'uz_sodik.json': '🇺🇿 الأوزبكية',
  'ms_basmeih.json': '🇲🇾 الملايوية',
  'zh_jian.json': '🇨🇳 الصينية',

  // أسماء التفاسير بالعربية
  'ar_muyassar.json': 'التفسير الميسر',
  'ar_ma3any.json': 'تفسير المعاني',
  'baghawy.json': 'تفسير البغوي',
  'qortoby.json': 'تفسير القرطبي',
  'e3rab.json': 'إعراب القرآن',
  'tanweer.json': 'تفسير التنوير',
  'sa3dy.json': 'تفسير السعدي',
  'waseet.json': 'تفسير الوسيط',
  'katheer.json': 'تفسير ابن كثير',
  'tabary.json': 'تفسير الطبري'
}
const tafsirOptions = [
  'ar_muyassar.json', 'ar_ma3any.json', 'baghawy.json', 'qortoby.json', 'e3rab.json',
  'tanweer.json', 'sa3dy.json',
  'waseet.json', 'katheer.json', 'tabary.json'
]

const translationOptions = [
  'in_indonesian.json', 'ru_russian.json', 'en_tafheem.json', 'nl_siregar.json', 'pr_tagi.json',
  'bn_bengali.json', 'pt_elhayek.json', 'bs_korkut.json', 'ru_kuliev.json',
  'de_bubenheim.json', 'so_abduh.json', 'en_sahih.json', 'sq_nahi.json',
  'es_navio.json', 'sv_bernstrom.json', 'fr_hamidullah.json', 'sw_barwani.json',
  'ha_gumi.json', 'ta_tamil.json', 'id_indonesian.json', 'th_thai.json',
  'it_piccardo.json', 'tr_diyanet.json', 'ku_asan.json', 'ur_jalandhry.json',
  'ml_abdulhameed.json', 'uz_sodik.json', 'ms_basmeih.json', 'zh_jian.json'
]

// تعريف props
const props = defineProps({
  type: String, // نوع المحتوى (تفسير أو ترجمة)
  surahNumber: Number,
  ayahNumber: Number,
  isOpen: Boolean
})

// أسماء الملفات المفضلة بشكل تلقائي
const DEFAULT_TAFSIR = 'tabary.json'
const DEFAULT_TRANSLATION = 'en_sahih.json'

const selectedFile = ref('')

// عند تغيير نوع المحتوى (تفسير/ترجمة)
watch(() => props.type, () => {
  const saved = localStorage.getItem(localStorageKey.value)
  selectedFile.value = saved || (props.type === 'tafsir' ? DEFAULT_TAFSIR : DEFAULT_TRANSLATION)
})

const emit = defineEmits(['close'])

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
    selectedFile.value = DEFAULT_TAFSIR;
  }

});

// حفظ الملف المختار تلقائياً عند تغييره
watch(selectedFile, (newFile) => {
  console.log('Selected file changed:', newFile)
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


watch(() => [props.surahNumber, props.ayahNumber, props.isOpen, selectedFile.value], async ([sura, aya, open]) => {
  if (open && sura && aya && selectedFile.value) {
    isLoading.value = true
    const folder = props.type === 'tafsir' ? 'tafasir' : 'tarajem'
    try {
      const res = await fetch(`/assets/${folder}/${selectedFile.value}`)
      if (!res.ok) {
        throw new Error('حدث خطأ في تحميل البيانات')
      }
      const data = await res.json()
      const match = data.find(item => item.sura === sura && item.aya === aya)
      content.value = match ? match.text : 'لم يتم العثور على المحتوى.'
    } catch (err) {
      content.value = 'حدث خطأ أثناء تحميل المحتوى.'
      console.error(err)  // عرض الخطأ في الـ console للتنقيح
    } finally {
      isLoading.value = false
    }
  }
})


// تم تكرار الكود الخاص بالأزرار هنا
const isDark = ref(false);
const fontSize = ref(22);
const fontFamily = ref('Uthmani');
const showFontMenu = ref(false);

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
