<script setup>


import { ref, computed, watch } from 'vue'
import { IonModal, IonSelect, IonSelectOption, IonContent, IonHeader, IonTitle, IonToolbar, IonButtons, IonButton } from '@ionic/vue';
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

onMounted(() => {
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
  return ltrLanguages.includes(selectedFile.value) ? 'ltr-text' : 'rtl-text';
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
            {{ languageDisplay[file] || file.replace('.json', '') }}
          </ion-select-option>
        </ion-select>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <div v-if="isLoading">جارٍ التحميل...</div>
      <div v-else>
        <div :class="contentClass" v-if="props.type === 'tafsir'" v-html="content" />
        <div :class="contentClass" v-else>{{ content }}</div>
      </div>
    </ion-content>
  </ion-modal>
</template>
