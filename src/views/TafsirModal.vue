<script setup>

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


import { ref, computed, watch } from 'vue'
import { IonModal, IonSelect, IonSelectOption, IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonButton } from '@ionic/vue';

// تعريف props
const props = defineProps({
  type: String, // نوع المحتوى (تفسير أو ترجمة)
  surahNumber: Number,
  ayahNumber: Number,
  isOpen: Boolean
})

// أسماء الملفات المفضلة بشكل تلقائي
const DEFAULT_TAFSIR = 'katheer.json'
const DEFAULT_TRANSLATION = 'en_sahih.json'

const selectedFile = ref('')



// عند تغيير نوع المحتوى (تفسير/ترجمة)
watch(() => props.type, () => {
  const saved = localStorage.getItem(localStorageKey.value)
  selectedFile.value = saved || (props.type === 'tafsir' ? DEFAULT_TAFSIR : DEFAULT_TRANSLATION)
})

// حفظ الملف المختار تلقائياً عند تغييره
watch(selectedFile, (newFile) => {
  if (newFile) {
    localStorage.setItem(localStorageKey.value, newFile)
  }
})


const emit = defineEmits(['close'])



const availableOptions = computed(() =>
  props.type === 'tafsir' ? tafsirOptions : translationOptions
)

// مفتاح لتخزين البيانات في localStorage
const localStorageKey = computed(() =>
  props.type === 'tafsir' ? 'preferredTafsir' : 'preferredTranslation'
)

// عند تغيير نوع المحتوى (تفسير/ترجمة)
watch(() => props.type, () => {
  const saved = localStorage.getItem(localStorageKey.value)
  selectedFile.value = saved || (props.type === 'tafsir' ? DEFAULT_TAFSIR : DEFAULT_TRANSLATION)
})

// حفظ الملف المختار تلقائياً عند تغييره
watch(selectedFile, (newFile) => {
  if (newFile) {
    localStorage.setItem(localStorageKey.value, newFile)
  }
})

// تحميل المحتوى عند تغيير أحد المتغيرات
const content = ref('')
const isLoading = ref(false)

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
</script>

<template>
  <ion-modal :is-open="isOpen" @didDismiss="emit('close')">
    <ion-header>
      <ion-toolbar>
        <ion-title>
          {{ props.type === 'tafsir' ? 'التفسير' : 'الترجمة' }}
        </ion-title>
        <ion-buttons slot="end">
          <ion-button @click="emit('close')">إغلاق</ion-button>
        </ion-buttons>
      </ion-toolbar>
      <ion-toolbar>
        <ion-select v-model="selectedFile" interface="popover" placeholder="اختر ملف" :disabled="!isOpen">
          <ion-select-option v-for="file in availableOptions" :key="file" :value="file">
            {{ file.replace('.json', '') }}
          </ion-select-option>
        </ion-select>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <div v-if="isLoading">جارٍ التحميل...</div>
      <div v-else>
        <div v-if="props.type === 'tafsir'" v-html="content" />
        <div v-else>{{ content }}</div>
      </div>
    </ion-content>
  </ion-modal>
</template>
