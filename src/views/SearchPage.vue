<template>
  <ion-page :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
    <ion-header :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
      <ion-toolbar :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
        <ion-title>البحث في القرآن الكريم</ion-title>
      </ion-toolbar>
      <ion-toolbar :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
        <ion-searchbar v-model="searchTerm" @ionInput="handleSearch" placeholder="أدخل كلمة للبحث"
          :class="{ 'dark-theme': isDark, 'white-theme': !isDark }" />
      </ion-toolbar>
    </ion-header>

    <ion-content :class="{ 'dark-theme': isDark, 'white-theme': !isDark }" @ionInfinite="loadMoreResults"
      :scroll-events="true">
      <ion-list v-if="results.length" :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
        <ion-item v-for="(result, index) in results" :key="index"
          :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
          <!-- الحاوي الكامل -->
          <div class="flex items-center justify-between w-full" @click="goToSurah(result)">
            <!-- نصّ النتيجة -->
            <ion-label class="flex-1 truncate" :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
              <h3 class="truncate">
                {{ result.surahName }} - آية {{ result.ayahNumber }}
              </h3>

              <p class="truncate" v-html="highlightSearchTerm(result.text, result.no_Tashkeel_text)" />
              <div class="flex px-2" @click.stop>
                <ion-button size="small" fill="clear"
                  class="rounded-full h-6 min-h-[1.5rem] px-2 text-white text-[0.65rem] font-semibold bg-gradient-to-r from-blue-500 to-blue-700"
                  @click="openTafsir(result)">
                  📖 تفسير
                </ion-button>

                <ion-button size="small" fill="clear"
                  class="rounded-full h-6 min-h-[1.5rem] px-2 text-white text-[0.65rem] font-semibold bg-gradient-to-r from-blue-500 to-blue-700"
                  @click="openTranslation(result)">
                  🌐 ترجمة
                </ion-button>

                <ion-button size="small" fill="clear"
                  class="rounded-full h-6 min-h-[1.5rem] px-2 text-white text-[0.65rem] font-semibold bg-gradient-to-r from-blue-500 to-blue-700"
                  @click="copyAyah(result.text)">
                  📋 نسخ
                </ion-button>

                <ion-button size="small" fill="clear"
                  class="rounded-full h-6 min-h-[1.5rem] px-2 text-white text-[0.65rem] font-semibold transition"
                  :class="currentAudio == null
                    ? 'bg-gradient-to-r from-blue-500 to-blue-700 cursor-pointer'
                    : 'bg-gray-400 opacity-50 cursor-not-allowed'"
                  @click=" playAyahAudio(result.surahNumber, result.ayahNumber)">
                  {{ isPlaying ? "⏸️" : "▶️" }} تلاوة
                </ion-button>



                <ion-button size="small" fill="clear"
                  class="rounded-full h-6 min-h-[1.5rem] px-2 text-white text-[0.65rem] font-semibold bg-gradient-to-r from-blue-500 to-blue-700"
                  @click="shareAyahText(result.text, result.surahName)">
                  📤 مشاركة
                </ion-button>

              </div>
            </ion-label>

          </div>
        </ion-item>
      </ion-list>

      <ion-text v-else class="ion-padding">
        لا توجد نتائج
      </ion-text>

      <ion-infinite-scroll threshold="100px" @ionInfinite="loadMoreResults">
        <ion-infinite-scroll-content loading-spinner="bubbles"
          loading-text="جاري تحميل المزيد..."></ion-infinite-scroll-content>
      </ion-infinite-scroll>
    </ion-content>


    <TafsirModal v-if="modalOpen" :is-open="modalOpen" :surah-number="selectedSurah" :ayah-number="selectedAyah"
      :type="modalType" @close="modalOpen = false" />

  </ion-page>
</template>

<script setup lang="ts">
import TafsirModal from './TafsirModal.vue'
import { onMounted, ref } from 'vue'
import { useQuranSearch } from '@/composables/useQuranSearch'
import { useRouter } from 'vue-router'
import { IonButton, IonContent, IonHeader, IonPage, IonItem, IonTitle, IonToolbar, IonText, IonList, IonLabel, IonSearchbar, IonInfiniteScrollContent, IonInfiniteScroll } from "@ionic/vue";

import debounce from 'lodash.debounce'

let currentAudio = ref<HTMLAudioElement | null>(null);

function getAudioPath(surahNumber: number, ayahNumber: number) {
  const surahStr = String(surahNumber).padStart(3, '0');
  const ayahStr = String(ayahNumber).padStart(3, '0');
  return `assets/sounds/Sa3d_Alghamdy/${surahStr}/${surahStr}${ayahStr}.opus`;
}


async function playAyahAudio(surahNumber: number, ayahNumber: number) {

  if (currentAudio.value) {
    return;
  }

  const path = getAudioPath(surahNumber, ayahNumber);
  currentAudio.value = new Audio(path);

  currentAudio.value.onended = () => {
    isPlaying.value = false;
    currentAudio.value = null;
  };

  currentAudio.value.onerror = (e) => {
    console.error('❌ خطأ في تشغيل الصوت:', e);
    isPlaying.value = false;
  };

  try {
    await currentAudio.value.play();
    isPlaying.value = true;
  } catch (err) {
    console.error('❌ فشل التشغيل:', err);
    isPlaying.value = false;
  }
}


function copyAyah(ayahText: string) {
  if (ayahText) {
    navigator.clipboard.writeText(ayahText)
      .then(() => console.log('✅ تم نسخ الآية!'))
      .catch(() => console.log('❌ فشل النسخ.'));
  }
}

import { Share } from '@capacitor/share';

const shareAyahText = async (ayahText: string, surahName: string) => {
  if (ayahText) {
    try {
      await Share.share({
        title: `📖 ${surahName}`,
        text: ayahText,
        dialogTitle: 'مشاركة الآية'
      });
    } catch (err) {
      console.error('خطأ في المشاركة:', err);
    }
  }
}



const isPlaying = ref(false)

function openTafsir(result: any) {
  selectedSurah.value = result.surahNumber;
  selectedAyah.value = result.ayahNumber;
  modalType.value = 'tafsir';
  modalOpen.value = true;
}

function openTranslation(result: any) {
  selectedSurah.value = result.surahNumber;
  selectedAyah.value = result.ayahNumber;
  modalType.value = 'translation';
  modalOpen.value = true;
}

const modalOpen = ref(false);
const selectedSurah = ref<number | null>(null);
const selectedAyah = ref<number | null>(null);
const modalType = ref<'tafsir' | 'translation'>('tafsir');

const isDark = ref(true)
const { search, lastSurahNumber, lastAyahNumber } = useQuranSearch()
const searchTerm = ref('')
const results = ref<any[]>([])  // لتخزين النتائج الحالية
const isLoading = ref(false)  // لتتبع حالة التحميل
const noMoreResults = ref(false)  // لتتبع حالة التحميل
// الدالة التي يتم تفعيلها بعد كل كتابة (debounced)
const handleSearch = debounce(() => {
  if (searchTerm.value.trim().length >= 2) {
    results.value = []  // إفراغ النتائج السابقة
    noMoreResults.value = false;
    lastSurahNumber.value = 1;
    lastAyahNumber.value = 1;
    loadResults()  // تحميل أول 20 نتيجة
  } else {
    results.value = []  // إفراغ النتائج إذا لم يتم إدخال كلمة بحث
  }
}, 500)  // تأخير البحث نصف ثانية

// دالة لتحميل النتائج
async function loadResults() {
  if (isLoading.value) return;
  isLoading.value = true;


  const startSurahNumber = lastSurahNumber.value || 1  // إذا لم يكن هناك رقم سورة أخير، نبدأ من السورة الأولى
  const startAyahNumber = lastAyahNumber.value || 1  // إذا لم يكن هناك رقم آية أخير، نبدأ من الآية الأولى

  // تحميل نتائج جديدة بناءً على رقم السورة والآية الأخيرين
  const newResults = await search(searchTerm.value.trim(), startSurahNumber, startAyahNumber, 20);

  noMoreResults.value = newResults[newResults.length - 1] && newResults[newResults.length - 1].noMoreResults;
  results.value = [...results.value, ...newResults];


  isLoading.value = false;
}

function loadMoreResults(event: any) {
  if (!noMoreResults.value) {
    loadResults();  // تحميل المزيد من النتائج
  }

  event.target.complete();  // إتمام عملية التحميل
}

const router = useRouter()


onMounted(() => {
  isDark.value = localStorage.getItem('isDark') === 'true'
})

function goToSurah(result: any) {
  router.push({
    name: 'SurahDetail',
    params: {
      number: result.surahNumber,
      scrollTo: result.ayahNumber
    }
  });
}
function escapeRegExp(str: string) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function getContextSnippet(text: string, term: string, contextWordsBefore = 5, contextWordsAfter = 5) {
  // تقسيم النص لكلمات (نستخدم فراغ كفاصل)
  const words = text.split(/\s+/);

  // البحث عن أول ظهور للكلمة (تجاهل حالة الحروف)
  const lowerWords = words.map(w => w.toLowerCase());
  const lowerTerm = term.toLowerCase();

  // إيجاد موضع أول تطابق للكلمة (يمكن تعديل لتطابق كلمة كاملة أو جزء)
  // هنا نبحث عن كلمة تحتوي term كجزء (مثل "النور" و "نور")
  let index = -1;
  for (let i = 0; i < lowerWords.length; i++) {
    if (lowerWords[i].includes(lowerTerm)) {
      index = i;
      break;
    }
  }

  if (index === -1) {
    // الكلمة غير موجودة، نرجع النص كامل
    return text;
  }

  // حساب حدود القطعة المراد عرضها
  const start = Math.max(0, index - contextWordsBefore);
  const end = Math.min(words.length - 1, index + contextWordsAfter);

  // تجميع الكلمات المختارة مع ...
  const snippetWords = words.slice(start, end + 1);

  let prefix = start > 0 ? '... ' : '';
  let suffix = end < words.length - 1 ? ' ...' : '';

  return prefix + snippetWords.join(' ') + suffix;
}

import { useBackButton } from '@ionic/vue';
useBackButton(10, () => {
  router.back();
});

function highlightSearchTerm(text: string, noTashkeelText?: string) {
  if (!searchTerm.value.trim()) return text;

  const term = searchTerm.value.trim();

  // لو noTashkeelText غير معرف أو فارغ، نستعمل النص الأصلي بدل
  const sourceText = noTashkeelText && noTashkeelText.length > 0 ? noTashkeelText : text;

  const snippet = getContextSnippet(sourceText, term, 5, 5);

  const escapedTerm = escapeRegExp(term);
  const re = new RegExp(`(${escapedTerm})`, 'gi');

  return snippet.replace(re, '<strong>$1</strong>');
}


</script>
