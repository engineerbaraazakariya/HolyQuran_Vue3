<template>
  <ion-page :key="$route.fullPath" :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
    <ion-header>
      <ion-toolbar @click="upperSurahNameShown = false" v-show="upperSurahNameShown"
        :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
        <!-- اسم السورة مع الزخرفة -->
        <div class="upperSurahName text-center flex justify-center items-center w-full h-12" :style="{
          fontSize: fontSize + 'px',
          fontFamily: fontFamily,
          color: isDark ? 'white' : 'black'
        }">
          <SurahInfo v-if="surah" :SurahName="surah.name" :isDark="isDark" :fontFamily="fontFamily" :pageNumber="Page"
            :JuzNumber="Juz" />
        </div>
      </ion-toolbar>
      <ion-toolbar v-if="!upperSurahNameShown" :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
        <ion-buttons slot="start">
          <ion-back-button defaultHref="/list"></ion-back-button>
        </ion-buttons>
        <ion-buttons slot="end">
          <ion-button @click="increaseFontSize" title="تكبير الخط">
            <ion-icon :icon="addCircle" />
          </ion-button>
          <ion-button @click="decreaseFontSize" title="تصغير الخط">
            <ion-icon :icon="removeCircle" />
          </ion-button>
          <ion-button @click="toggleTheme" title="الوضع الليلي">
            <ion-icon :icon="isDark ? moon : sunny" />
          </ion-button>
          <ion-button @click="showFontMenu = !showFontMenu" title="تغيير الخط">
            <ion-icon :icon="colorPalette" />
          </ion-button>
          <ion-button router-link="/search">
            <ion-icon slot="icon-only" :icon="searchOutline" />
          </ion-button>
          <ion-button @click="upperSurahNameShown = true" title="إظهار اسم السورة مع الزخرفة">
            <ion-icon :icon="ribbon" />
          </ion-button>
        </ion-buttons>
      </ion-toolbar>
      <ion-toolbar v-if="showFontMenu" :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
        <ion-segment v-model="fontFamily" @ionChange="saveFont" scrollable
          :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
          <ion-segment-button :class="{ 'dark-theme': isDark, 'white-theme': !isDark }"
            value="Uthmani">عثماني</ion-segment-button>
          <ion-segment-button :class="{ 'dark-theme': isDark, 'white-theme': !isDark }"
            value="Amiri">أميري</ion-segment-button>
          <ion-segment-button :class="{ 'dark-theme': isDark, 'white-theme': !isDark }" value="MeQuran">مي
            قرآن</ion-segment-button>
          <ion-segment-button :class="{ 'dark-theme': isDark, 'white-theme': !isDark }"
            value="DecoType">زخرفي</ion-segment-button>
          <ion-segment-button :class="{ 'dark-theme': isDark, 'white-theme': !isDark }"
            value="Hafs">حفص</ion-segment-button>
          <ion-segment-button :class="{ 'dark-theme': isDark, 'white-theme': !isDark }"
            value="Nabi">رقع</ion-segment-button>
        </ion-segment>
      </ion-toolbar>
    </ion-header>

    <ion-content :class="{ 'dark-theme': isDark, 'white-theme': !isDark }" @ionScroll="saveScrollPosition"
      ref="scrollContainer" scroll-events="true" style="overflow-y: auto;">
      <span class="flex flex-wrap justify-around px-2">
        <template v-if="surah">
          <!-- اسم السورة مع الزخرفة -->
          <SurahInfo @click="upperSurahNameShown = true" v-if="!upperSurahNameShown" :SurahName="surah.name"
            :fontFamily="fontFamily" :pageNumber="Page" :isDark="isDark" :JuzNumber="Juz" />

          <!-- البسملة -->
          <div v-if="![1, 9].includes(surah.number)"
            class="text-center mb-4 flex justify-center items-center w-full mt-2" :style="{
              fontSize: fontSize + 'px',
              fontFamily: fontFamily,
              color: isDark ? 'white' : 'black'
            }">
            ﷽
          </div>
          <template v-for="ayah in surah.ayahs" :key="ayah.numberInSurah">
            <span v-for="(word, index) in ayah.text.split(' ')" :key="index" :style="{
              fontSize: fontSize + 'px',
              fontFamily: fontFamily,
              color: isDark ? 'white' : 'black',
              wordSpacing: '0.25em',
              backgroundColor: surahVariables[surah.number]?.longPressedAyahNumber === ayah.numberInSurah ? 'green' : 'transparent',
              cursor: 'default',
              backgroundColor: surahVariables[surah.number]?.longPressedAyahNumber === ayah.numberInSurah ? 'green' : 'transparent'
            }" @touchstart="startLongPress($event, surah.number, ayah.numberInSurah)" @touchend="stopLongPress"
              @touchmove="stopLongPress">
              {{ word }}<span class="!w-2 !max-w-2 !min-w-2 flex" :style="{
                backgroundColor: surahVariables[surah.number]?.longPressedAyahNumber === ayah.numberInSurah ? 'green' : 'transparent'
              }" v-if="index !== ayah.text.split(' ').length - 1"></span>
            </span>
            <span :data-page="ayah.page" :data-hizbQuarter="ayah.hizbQuarter" :data-juz="ayah.juz"
              :id='"ayah-" + ayah.numberInSurah' class="relative flex justify-center items-center" :style="{
                minHeight: fontSize / 1.012 + 'px',
                minWidth: fontSize / 1.012 + 'px',
                backgroundImage: `url(/assets/${surahVariables[surah.number]?.selectedAyahNumber === ayah.numberInSurah ? 'bookmarked_ayah' : 'end_ayah'}.svg)`,
                backgroundSize: 'contain',
                backgroundRepeat: 'no-repeat',
                backgroundPosition: 'center',
                fontSize: fontSize / 2.75 + 'px',
                width: fontSize / 1.2 + 'px',
                fontWeight: 'bold',
                color: 'black',
              }" @click="toggleAyah(surah.number, ayah.numberInSurah)"
              @contextmenu.prevent="toggleAyah(surah.number, ayah.numberInSurah)">
              <span>
                {{ ayah.numberInSurah }}
              </span>
            </span>
          </template>
        </template>
        <template v-else>
          <p class="ion-padding">جارٍ تحميل السورة...</p>
        </template>
      </span>
      <IonPopover :is-open="showPopover" :event="popoverEvent"
        @didDismiss="surahVariables[selectedSurahNumber].longPressedAyahNumber = null; showPopover = false">
        <ion-list>
          <ion-item button @click="onOption('تفسير')">📖 تفسير</ion-item>
          <ion-item button @click="onOption('ترجمة')">🌐 ترجمة</ion-item>
          <ion-item button @click="onOption()">❌ إلغاء</ion-item>
        </ion-list>
      </IonPopover>


    </ion-content>
    <TafsirModal v-if="surah" :is-open="modalOpen" :surah-number="selectedSurah" :ayah-number="selectedAyah"
      :type="modalType" @close="modalOpen = false" />

  </ion-page>
</template>

<script setup>
import TafsirModal from './TafsirModal.vue'
import SurahInfo from './SurahInfo.vue';
const modalOpen = ref(false)
const upperSurahNameShown = ref(true)
const selectedSurah = ref(null)
const selectedAyah = ref(null)

import { IonPopover } from '@ionic/vue'
const showPopover = ref(false)
const popoverEvent = ref(null)  // لتخزين حدث النقر لتموضع النافذة
const selectedSurahNumber = ref(null)
const selectedAyahNumber = ref(null)

function onOption(choice) {
  // إغلاق الـ popover
  showPopover.value = false;

  if (!choice) {
    surahVariables.value[selectedSurahNumber.value].selectedAyahNumber = null;
    return;
  }

  // إذا كانت الآية محددة، افتح الـ popover تلقائيًا
  if (choice === 'تفسير' || choice === 'ترجمة') {
    selectedSurah.value = selectedSurahNumber.value;
    selectedAyah.value = selectedAyahNumber.value;
    modalType.value = choice === 'تفسير' ? 'tafsir' : 'translation';
    modalOpen.value = true;
  }
}


const modalType = ref('tafsir') // أو 'translation'

import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { addCircle, removeCircle, ribbon } from 'ionicons/icons'

import {
  sunny,
  moon,
  colorPalette,
  searchOutline
} from 'ionicons/icons'
import { IonContent, IonHeader, IonPage, IonIcon, IonBackButton, IonTitle, IonSegment, IonSegmentButton, IonToolbar, IonButtons, IonButton, IonList, IonItem } from "@ionic/vue";
const route = useRoute()
const surahVariables = ref({}) // { '1': {numberInSurah:5, scrollPosition:100}, '2': {numberInSurah:10, scrollPosition:200} }

const surah = ref(null)
const fontSize = ref(22)
const fontFamily = ref('Uthmani')
const isDark = ref(false)
const showFontMenu = ref(false)
const scrollContainer = ref(null)



import { useBackButton } from '@ionic/vue';
import router from '@/router';
useBackButton(10, () => {
  router.replace('/');
});


const pressTimer = ref(null)  // لتخزين المؤقت
const longPressThreshold = 200
const isPressing = ref(false)  // حالة الضغط المستمر


const isScrolling = ref(false);  // متغير لتتبع إذا كان المستخدم يمرر

function startLongPress(event, surahNumber, ayahNumber) {
  isPressing.value = true; // بدأ الضغط الطويل
  popoverEvent.value = event;

  pressTimer.value = setTimeout(() => {
    if (isPressing.value && !isScrolling.value) {
      // تأكد من أن الكائن موجود
      if (!surahVariables.value[surahNumber]) {
        surahVariables.value[surahNumber] = { longPressedAyahNumber: null, bookmarkedAyahNumber: null, scrollPosition: null };
      }

      // تعيين قيمة longPressedAyahNumber
      surahVariables.value[surahNumber].longPressedAyahNumber = ayahNumber;

      selectedSurahNumber.value = surahNumber;
      selectedAyahNumber.value = ayahNumber;
      showPopover.value = true;
    }
  }, longPressThreshold);
}


function stopLongPress() {
  isPressing.value = false; // إنهاء الضغط الطويل
  clearTimeout(pressTimer.value);

  // إعادة تعيين حالة التمرير
  isScrolling.value = false;
}

function getAyahAtScrollPosition() {
  // جمع جميع العناصر الخاصة بالآيات (التي تحتوي على المعرف "ayah-")
  const ayahs = document.querySelectorAll("[id^='ayah-']");

  let topAyah = null;
  let topOffset = Number.POSITIVE_INFINITY;

  ayahs.forEach(ayah => {
    // قياس المسافة بين العنصر وأعلى الصفحة
    const rect = ayah.getBoundingClientRect();

    // إذا كانت الآية في أعلى الصفحة (أقرب للموقع 0)
    if (rect.top >= 172 && rect.top < topOffset) {
      topOffset = rect.top;
      topAyah = ayah;
    }
  });

  // إذا كانت هناك آية قريبة من الأعلى، نقوم بإرجاع البيانات
  if (topAyah) {
    // استخراج القيم من الأتريبيوتس
    const page = topAyah.getAttribute('data-page');
    const hizbQuarter = topAyah.getAttribute('data-hizbQuarter');
    const juz = topAyah.getAttribute('data-juz');

    // إذا كانت القيم موجودة
    if (page && hizbQuarter && juz) {
      // إرجاع البيانات
      return {
        ayahNumber: topAyah.id.split('-')[1], // استخراج رقم الآية من الـ ID
        hizb: hizbQuarter,
        juz: juz,
        page: page
      };
    }
  }

  return null;

}

const AyahNumber = ref(null);
const Hizb = ref(null);
const Juz = ref(null);
const Page = ref(null);


async function saveScrollPosition() {
  const el = scrollContainer.value?.$el || scrollContainer.value
  const scrollEl = await el?.getScrollElement?.()
  const scrollTop = scrollEl?.scrollTop || 0

  if (surah.value) {
    if (surahVariables.value[surah.value.number] === undefined) {
      surahVariables.value[surah.value.number] = { bookmarkedAyahNumber: null, scrollPosition: null }
    }
    surahVariables.value[surah.value.number].scrollPosition = scrollTop.toFixed(2).toString();

    // الحصول على البيانات من الدالة
    const { ayahNumber, hizb, juz, page } = getAyahAtScrollPosition(scrollTop.toFixed(2).toString());

    // تحديث القيم باستخدام `value`
    AyahNumber.value = ayahNumber;
    Hizb.value = hizb;
    Juz.value = juz;
    Page.value = page;

    localStorage.setItem('surahVariables', JSON.stringify(surahVariables.value))
  }
}
function toggleAyah(surahNumber, ayahNumber) {
  // إذا كانت الآية محددة بالفعل، قم بإلغاء التحديد
  const current = surahVariables.value[surahNumber]?.selectedAyahNumber || null;

  if (!surahVariables.value[surahNumber]) {
    surahVariables.value[surahNumber] = { selectedAyahNumber: null, scrollPosition: null };
  }

  if (current === ayahNumber) {
    // إلغاء التحديد
    surahVariables.value[surahNumber].selectedAyahNumber = null;
  } else {
    // تحديد الآية
    surahVariables.value[surahNumber].selectedAyahNumber = ayahNumber;
  }

  // حفظ التغييرات في الذاكرة المحلية
  localStorage.setItem('surahVariables', JSON.stringify(surahVariables.value));
}

onMounted(async () => {
  isDark.value = localStorage.getItem('isDark') === 'true';
  fontSize.value = parseFloat(localStorage.getItem('fontSize')) || 22;
  fontFamily.value = localStorage.getItem('fontFamily') || 'Uthmani';

  const stored = localStorage.getItem('surahVariables');
  if (stored) {
    surahVariables.value = JSON.parse(stored);
  }

  // التعامل مع الحالة الأولية
  await handleRouteChange(route.params.number, route.params.scrollTo);
});

async function handleScrollTo(scrollTo, surahNumber) {
  if (!scrollTo) return;

  try {
    if (scrollTo.includes('.')) {
      // التمرير إلى موضع معين
      const scrollPos = parseFloat(scrollTo);
      await scrollToPosition(scrollPos);
    } else {
      // التمرير إلى آية محددة
      const ayahNumber = parseInt(scrollTo);
      await scrollToAyah(ayahNumber, surahNumber);
    }
  } catch (error) {
    console.error('فشل في التمرير:', error);
  }
}

async function scrollToPosition(position) {
  const ionContentElement = scrollContainer.value?.$el || scrollContainer.value;
  if (ionContentElement) {
    const scrollEl = await ionContentElement.getScrollElement();
    scrollEl.scrollTo({ top: position, behavior: 'smooth' });
  }
}

async function scrollToAyah(ayahNumber, surahNumber, attempt = 0) {
  const maxAttempts = 5;
  const element = document.getElementById('ayah-' + ayahNumber);

  if (element) {
    element.scrollIntoView({ behavior: 'smooth', block: 'center' });
    updateSelectedAyah(surahNumber, ayahNumber);
  } else if (attempt < maxAttempts) {
    await new Promise(resolve => setTimeout(resolve, 200 * (attempt + 1)));
    await scrollToAyah(ayahNumber, surahNumber, attempt + 1);
  } else {
    console.error('تعذر العثور على الآية بعد عدة محاولات');
  }
}
const autoSelectAyah = (ayahNumber) => {
  if (!surahVariables.value[surah.value.number]) {
    surahVariables.value[surah.value.number] = {
      selectedAyahNumber: null,
      longPressedAyahNumber: null,
      scrollPosition: null
    };
  }

  // تحديد الآية وكأنها مضغوطة ضغطة طويلة
  surahVariables.value[surah.value.number].longPressedAyahNumber = ayahNumber;
  selectedSurahNumber.value = surah.value.number;
  selectedAyahNumber.value = ayahNumber;

  // عرض قائمة الخيارات تلقائياً
  showPopoverForAyah(ayahNumber);
};

const showPopoverForAyah = (ayahNumber) => {
  const element = document.getElementById(`ayah-${ayahNumber}`);
  if (element) {
    // إنشاء حدث وهمي لتمريره إلى البوبوفر
    const fakeEvent = {
      target: element,
      clientX: element.getBoundingClientRect().left + element.offsetWidth / 2,
      clientY: element.getBoundingClientRect().top + element.offsetHeight / 2
    };

    popoverEvent.value = fakeEvent;
    showPopover.value = true;
  }
};
function updateSelectedAyah(surahNumber, ayahNumber) {
  if (!surahVariables.value[surahNumber]) {
    surahVariables.value[surahNumber] = {
      longPressedAyahNumber: null,
      scrollPosition: null
    };
  }
  surahVariables.value[surahNumber].longPressedAyahNumber = ayahNumber;
  localStorage.setItem('surahVariables', JSON.stringify(surahVariables.value));
}


async function handleRouteChange(surahNumberParam, scrollToParam) {
  const surahNumber = parseInt(surahNumberParam);

  // إعادة تعيين حالة السورة
  surah.value = null;
  await nextTick();

  // تحميل البيانات
  const res = await fetch('/assets/quran.json');
  const allSurahs = await res.json();
  surah.value = allSurahs.find(s => s.number === surahNumber);
  if (surah.value) {
    Juz.value = surah.value.ayahs[0].juz;
    Page.value = surah.value.ayahs[0].page;
    Hizb.value = surah.value.ayahs[0].hizb;
  }

  upperSurahNameShown.value = true;

  // الانتظار حتى يتم تحديث DOM
  await nextTick();

  if (scrollToParam) {
    await handleScrollTo(scrollToParam, surahNumber);
  }
}
// إعدادات المستخدم
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
const saveFont = () => {
  localStorage.setItem('fontFamily', fontFamily.value)
}
</script>
