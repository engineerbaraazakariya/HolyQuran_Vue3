<template>
  <ion-page :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
    <ion-header :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
      <ion-toolbar :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
        <ion-title>البحث في القرآن الكريم</ion-title>
      </ion-toolbar>
      <ion-toolbar :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
        <ion-searchbar class="searchbar" v-model="searchTerm" @ionInput="handleSearch" placeholder="أدخل كلمة للبحث"
          :class="{ 'dark-theme': isDark, 'white-theme': !isDark }" />
      </ion-toolbar>
    </ion-header>

    <ion-content :class="{ 'dark-theme': isDark, 'white-theme': !isDark }" @ionInfinite="loadMoreResults"
      :scroll-events="true">
      <ion-list v-if="results.length" :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
        <ion-item v-for="(result, index) in results" :key="index"
          :class="{ 'dark-theme': isDark, 'white-theme': !isDark }" class="cursor-pointer">
          <!-- الحاوي الكامل -->
          <div class="flex justify-between w-full" @click="handleResultClick(result)">

            <!-- نصّ النتيجة -->
            <ion-label class="flex-1 truncate" :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
              <h3 class="truncate">
                {{ getResultTitle(result) }}
              </h3>

              <p class="truncate" v-html="highlightSearchTerm(result.text, result.no_Tashkeel_text)" />
              <div class="flex !items-center" @click.stop>
                <ion-button size="small" fill="clear"
                  class="rounded-full h-8 min-h-[1.5rem] px-2 text-white text-[0.65rem] font-semibold bg-gradient-to-r from-blue-500 to-blue-700"
                  @click="openTafsir(result)">

                  <div class="flex flex-col justify-between h-6">
                    <div>📖 </div>
                    <div>تفسير</div>
                  </div>
                </ion-button>

                <ion-button size="small" fill="clear"
                  class="rounded-full h-8 min-h-[1.5rem] px-2 text-white text-[0.65rem] font-semibold bg-gradient-to-r from-blue-500 to-blue-700"
                  @click="openTranslation(result)">

                  <div class="flex flex-col justify-between h-6">
                    <div>🌐</div>
                    <div>ترجمة</div>
                  </div>


                </ion-button>
                <div
                  class="md button button-small button-clear ion-activatable ion-focusable hydrated rounded-full h-8 min-h-[1.5rem] px-2 text-white text-[0.65rem] font-semibold transition bg-gradient-to-r from-blue-500 to-blue-700 cursor-pointer relative min-w-14 flex justify-center items-center">
                  <div class="absolute float-left flex flex-col justify-between h-full gap-0 p-0 m-0"
                    @click="copyAyah(result); showPopover = false">
                    <div>📋</div>
                    <div>نسخ</div>
                  </div>
                  <div class="hover:text-blue-500 absolute left-1 float-left h-full flex items-center"
                    @click="showPopover = true; currentAyah = result;">
                    ◀
                  </div>
                </div>
                <ion-button size="small" fill="clear"
                  class="rounded-full h-8 min-h-[1.5rem] px-2 text-white text-[0.65rem] font-semibold transition"
                  :class="currentAudio == null
                    ? 'bg-gradient-to-r from-blue-500 to-blue-700 cursor-pointer'
                    : 'bg-gray-400 opacity-50 cursor-not-allowed'"
                  @click=" playAyahAudio(result.surahNumber, result.ayahNumber)">
                  <div class="flex flex-col justify-between h-6">
                    <div>{{ isPlaying ? "⏸️" : "▶️" }}</div>
                    <div>تلاوة</div>
                  </div>
                </ion-button>



                <ion-button size="small" fill="clear"
                  class="rounded-full h-8 min-h-[1.5rem] px-2 text-white text-[0.65rem] font-semibold bg-gradient-to-r from-blue-500 to-blue-700"
                  @click="shareAyahText(result.text, result.surahName)">
                  <div class="flex flex-col justify-between h-6">
                    <div>📤</div>
                    <div>مشاركة</div>
                  </div>
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
    <IonPopover :is-open="showPopover" :event="popoverEvent" @didDismiss="showPopover = false" class="cursor-pointer">
      <ion-item @click="copyAyah(currentAyah); showPopover = false" :value="true">مع التشكيل</ion-item>
      <ion-item @click="copyAyah(currentAyah, false); showPopover = false" :value="false">بدون تشكيل</ion-item>
    </IonPopover>

    <TafsirModal v-if="modalOpen" :is-open="modalOpen" :surah-number="selectedSurah" :ayah-number="selectedAyah"
      :type="modalType" @close="modalOpen = false" />

  </ion-page>
</template>

<script setup lang="ts">
interface BaseResult {
  type: 'ayah' | 'surah';
}

interface AyahResult extends BaseResult {
  type: 'ayah';
  text: string;
  no_Tashkeel_text: string;
  surahNumber: number;
  ayahNumber: number;
  surahName: string;
}

interface SurahResult extends BaseResult {
  type: 'surah';
  surahNumber: number;
  surahName: string;
  firstAyahText: string;
  firstAyahNoTashkeelText: string;
  ayahNumber?: number; // يمكن إضافة الآية الأولى إذا حبيت
}

type SearchResult = AyahResult | SurahResult;

import TafsirModal from './TafsirModal.vue'


import { IonPopover } from '@ionic/vue'
import { onMounted, ref } from 'vue'
import { useQuranSearch } from '@/composables/useQuranSearch'


import { useRouter } from 'vue-router'
import { IonButton, IonContent, IonHeader, IonPage, IonItem, IonTitle, IonToolbar, IonText, IonList, IonLabel, IonSearchbar, IonInfiniteScrollContent, IonInfiniteScroll } from "@ionic/vue";

import debounce from 'lodash.debounce'

let currentAudio = ref<HTMLAudioElement | null>(null);
const currentAyah = ref({ text: '', no_Tashkeel_text: '' })
const showPopover = ref(false)
const popoverEvent = ref(null)

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


function copyAyah(result: any, withTashkeel = true) {
  let ayahText = '';

  // 🔹 نتيجة آية
  if (result.text) {
    ayahText = withTashkeel
      ? result.text
      : result.no_Tashkeel_text;
  }

  // 🔹 نتيجة سورة → ننسخ الآية الأولى (موجودة في result.text)
  else if (result.type === 'surah' && result.firstAyah) {
    ayahText = withTashkeel
      ? result.firstAyah.text
      : result.firstAyah.no_Tashkeel_text;
  }

  if (!ayahText) {
    console.warn('❗ لا يوجد نص للنسخ', result);
    return;
  }

  const toBeCopied = `﷽ ﴿ ${ayahText} ﴾`;

  navigator.clipboard
    .writeText(toBeCopied)
    .then(() => console.log('✅ تم نسخ الآية!'))
    .catch(() => console.log('❌ فشل النسخ.'));
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
const { search, searchSurahs, lastSurahNumber, lastAyahNumber } = useQuranSearch()
const searchTerm = ref('')
const results = ref<any[]>([])  // لتخزين النتائج الحالية
const isLoading = ref(false)  // لتتبع حالة التحميل
const noMoreResults = ref(false)  // لتتبع حالة التحميل
// الدالة التي يتم تفعيلها بعد كل كتابة (debounced)
const handleSearch = debounce(() => {
  const term = searchTerm.value.trim();

  results.value = [];
  noMoreResults.value = false;

  if (term.length < 2) return;

  // 🔹 أولًا: نتائج السور
  const surahResults = searchSurahs(term);

  // نضيفها أعلى النتائج
  results.value.push(...surahResults);

  // 🔹 ثانيًا: نتائج الآيات
  lastSurahNumber.value = 1;
  lastAyahNumber.value = 1;
  loadResults();
}, 500);


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
  // set focus to searchbar input field
  setTimeout(() => {

    const searchbar = document.querySelectorAll('input.searchbar-input')[0] as HTMLElement
    searchbar.autofocus = true;
    searchbar.focus();

  }, 0);
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

function getContextSnippet(
  text: string | undefined,
  term: string,
  contextWordsBefore = 5,
  contextWordsAfter = 5
) {
  if (!text || !term) return '';

  const words = text.split(/\s+/);

  const lowerWords = words.map(w => w.toLowerCase());
  const lowerTerm = term.toLowerCase();

  let index = -1;
  for (let i = 0; i < lowerWords.length; i++) {
    if (lowerWords[i].includes(lowerTerm)) {
      index = i;
      break;
    }
  }

  if (index === -1) return text;

  const start = Math.max(0, index - contextWordsBefore);
  const end = Math.min(words.length - 1, index + contextWordsAfter);

  const snippetWords = words.slice(start, end + 1);

  const prefix = start > 0 ? '... ' : '';
  const suffix = end < words.length - 1 ? ' ...' : '';

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

  return snippet.replace(re, '<strong class=\'text-blue-500\'>$1</strong>');
}

function handleResultClick(result: SearchResult) {
  if (result.type === 'surah') {
    router.push({
      name: 'SurahDetail',
      params: {
        number: result.surahNumber,
        scrollTo: 1
      }
    });
  } else {
    goToSurah(result);
  }
}

function getResultTitle(result: SearchResult) {
  if (result.type === 'surah') {
    return `${result.surahName}`;
  }
  return `سُورَةُ ${result.surahName} - آية ${result.ayahNumber}`;
}


</script>