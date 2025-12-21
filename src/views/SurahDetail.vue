<template>
  <ion-page :key="$route.fullPath" :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
    <ion-header>
      <ion-toolbar @click="upperSurahNameShown = false" v-show="upperSurahNameShown"
        :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
        <!-- اسم السورة مع الزخرفة -->
        <div class="SurahInfo flex w-full overflow-hidden "
          :style="{ transform: `scaleY(${scaleYSurahInfo}) scaleX(1.4)` }">
          <SurahInfo v-if="surah" :fontSize="fontSize" :SurahName="surah.name" :isDark="isDark" :fontFamily="fontFamily"
            :pageNumber="Page" :JuzNumber="Juz" />

        </div>
      </ion-toolbar>
      <TopToolbar v-show="!upperSurahNameShown" :isDark="isDark" v-model:selectedFile="selectedFile" title=""
        :showBack="true" :showFontSizeButtons="true" :showThemeToggle="true" :showFontSelector="true" :showSearch="true"
        :showRibbon="true" />
    </ion-header>

    <ion-content :class="{ 'dark-theme': isDark, 'white-theme': !isDark }" @ionScroll="saveScrollPosition"
      ref="scrollContainer" scroll-events="true" style="overflow-y: auto;">
      <div class="flex flex-row justify-between">

        <div v-if="OnlyOnOrientationLandscape" class="flex !w-16 !min-w-16">
          <TopToolbar :vertical="true" :isDark="isDark" title="" :showBack="true" :showFontSizeButtons="true"
            :showThemeToggle="true" :showFontSelector="true" :showSearch="true" :showRibbon="false" />
        </div>
        <div ref="ayahContainer" class="relative">
          <svg v-if="svgRect" class="opacity-60 z-[0]" :style="{
            position: 'absolute',
            left: svgRect.left + 'px',
            top: svgRect.top + 'px',
            pointerEvents: 'none'
          }" :width="svgRect.width" :height="svgRect.height">
            <rect v-for="(r, i) in wordRects" :key="i" :x="r.x" :y="r.y" :width="r.width" :height="r.height" rx="4"
              ry="4" fill="currentColor" class="text-blue-500" />
          </svg>

        </div>
        <span class="flex flex-wrap justify-around px-2">
          <template v-if="surah">
            <!-- اسم السورة مع الزخرفة -->
            <div class="flex w-full SurahInfo" :style="{ transform: `scaleY(${scaleYSurahInfo}) scaleX(1.4)` }"
              v-if="!upperSurahNameShown || OnlyOnOrientationLandscape">
              <SurahInfo @click="!OnlyOnOrientationLandscape.value ? upperSurahNameShown = true : null"
                :SurahName="surah.name" :fontFamily="fontFamily" :pageNumber="Page" :isDark="isDark" :JuzNumber="Juz" />
            </div>

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
              <span v-for="(word, index) in ayah.text.split(' ')" :data-ayah-group="ayah.numberInSurah" :key="index"
                :style="{
                  fontSize: fontSize + 'px',
                  fontFamily: fontFamily,
                  color: basicMeaning[surah.number - 1][ayah.numberInSurah - 1][index]?.length > 0 ? '#6363f9' : isDark ? 'white' : 'black',
                  wordSpacing: '0.25em',
                  cursor: 'default',
                }" @touchstart="startLongPress($event, surah.number, ayah.numberInSurah)"
                @click="basicMeaning[surah.number - 1][ayah.numberInSurah - 1][index]?.length > 0 && setMaany(surah, ayah, index)"
                @touchend="stopLongPress" @touchmove="stopLongPress"
                @contextmenu.prevent="startLongPress($event, surah.number, ayah.numberInSurah, 0)"
                class="relative inline-block">
                {{ word }}<span class="!w-2 !max-w-2 !min-w-2 flex" :style="{
                  backgroundColor: surahVariables[surah.number]?.longPressedAyahNumber === ayah.numberInSurah ? 'green' : !isDark ? 'white' : 'black',
                }" v-if="index !== ayah.text.split(' ').length - 1"></span>
              </span>
              <span :data-page="ayah.page" :data-hizbQuarter="ayah.hizbQuarter" :data-juz="ayah.juz"
                :id='"ayah-" + ayah.numberInSurah' class="relative flex justify-center items-center" :style="{
                  minHeight: fontSize / 1.012 + 'px',
                  minWidth: fontSize / 1.012 + 'px',
                  backgroundImage: `url(assets/${surahVariables[surah.number]?.selectedAyahNumber === ayah.numberInSurah ? 'bookmarked_ayah' : 'end_ayah'}.svg)`,
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

      </div>
      <!-- start of dialog -->

      <div v-if="showCurrentMaany.length > 0" class="fixed inset-0 flex items-center justify-center bg-black/50 z-[1]"
        @click="showCurrentMaany = ''">
        <div class="w-max h-max max-w-[75vw] overflow-scroll opacity-100 rounded-xl shadow-lg p-6 relative no-scrollbar"
          :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">

          <!-- النص -->
          <div :class="{ 'dark-theme': isDark, 'white-theme': !isDark }" class="overflow-scroll no-scrollbar" :style="{
            fontSize: fontSize * .7 + 'px',
            fontFamily: fontFamily,
            color: isDark ? 'white' : 'black'
          }">
            {{ showCurrentMaany }}
          </div>
          <div class="flex justify-between pt-6">
            <div class="cursor-pointer text-blue-500 hover:text-blue-500"
              @click="onOption('تفسير', selectedTafsir, false)">
              تفسير الآية</div>
            <div class="cursor-pointer text-blue-500 hover:text-blue-500" @click="goToI3raab();">إعراب الآية</div>
          </div>
        </div>
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


      <IonPopover :is-open="showPopover" :event="popoverEvent" @didDismiss="showPopover = false">
        <ion-list>

          <!-- تفسير - مع اختيار -->
          <ion-item button lines="full" @click="onOption('تفسير', selectedTafsir)">
            <ion-icon slot="start" :icon="bookOutline" />
            <ion-label>تفسير</ion-label>

            <ion-select interface="popover" :value="selectedTafsir" @click.stop
              @ionChange="val => { selectedTafsir = val.detail.value; onOption('تفسير', selectedTafsir); }">
              <ion-select-option v-for="(option, index) in tafsirOptions" :key="option" :value="option">
                {{ languageDisplay[option] }}
              </ion-select-option>
            </ion-select>
          </ion-item>

          <!-- إعراب -->
          <ion-item button lines="full" @click="goToI3raab(); showPopover = false">
            <ion-icon slot="start" :icon="bookOutline" />
            <ion-label>إعراب</ion-label>
          </ion-item>
          <!-- ترجمة - مع اختيار -->
          <ion-item button lines="full" @click="onOption('ترجمة', selectedTranslation)">
            <ion-icon slot="start" :icon="globeOutline" />
            <ion-label>ترجمة</ion-label>

            <ion-select interface="popover" :value="selectedTranslation" @click.stop
              @ionChange="val => { selectedTranslation = val.detail.value; onOption('ترجمة', selectedTranslation); }">
              <ion-select-option :selected="index === 0" v-for="(option, index) in translationOptions" :key="option"
                :value="option">
                {{ languageDisplay[option] }}
              </ion-select-option>
            </ion-select>
          </ion-item>



          <!-- تلاوة -->
          <ion-item button lines="full"
            @click="isPlaying ? stopAyahAudio() : playAyahAudio(selectedSurahNumber, selectedAyahNumber, selectedRecitingWay)">
            <ion-icon slot="start" :icon="isPlaying ? pauseOutline : playOutline" />
            <ion-label>{{ isPlaying ? 'ايقاف' : 'تلاوة' }}</ion-label>

            <ion-select interface="popover" :value="selectedRecitingWay" @click.stop
              @ionChange="val => playAyahAudio(selectedSurahNumber, selectedAyahNumber, val.detail.value)">
              <ion-select-option value="الآية فقط">الآية فقط</ion-select-option>
              <ion-select-option value="إلى ختم السورة">إلى ختم السورة</ion-select-option>
              <ion-select-option value="إلى ختم القرآن الكريم">إلى ختم القرآن الكريم</ion-select-option>
            </ion-select>
          </ion-item>

          <!-- نسخ -->
          <ion-item button lines="full" @click="copyAyah(copyAyahWithTashkeel); showPopover = false">
            <ion-icon slot="start" :icon="copyOutline" />
            <ion-label>نسخ</ion-label>

            <ion-select interface="popover" :value="copyAyahWithTashkeel" @click.stop
              @ionChange="val => copyAyah(val.detail.value)">
              <ion-select-option :value="true">مع التشكيل</ion-select-option>
              <ion-select-option :value="false">بدون تشكيل</ion-select-option>
            </ion-select>
          </ion-item>

          <!-- مشاركة -->
          <ion-item v-if="!isDesktop" button lines="full" @click="shareAyahText(); showPopover = false">
            <ion-icon slot="start" :icon="shareSocialOutline" />
            <ion-label>مشاركة</ion-label>
          </ion-item>

        </ion-list>
      </IonPopover>



    </ion-content>
    <TafsirModal v-if="surah" :is-open="modalOpen" :surah-number="selectedSurah" :ayah-number="selectedAyah"
      :type="modalType" :selectedFile="modalType === 'tafsir' ? selectedTafsir : selectedTranslation"
      @close="modalOpen = false" />

  </ion-page>
</template>

<script setup>
import { IonIcon, IonLabel, IonSelectOption, IonSelect } from '@ionic/vue'
import {
  shareSocialOutline, copyOutline, playOutline, pauseOutline, bookOutline
  , globeOutline
} from 'ionicons/icons'
import { onActivated, unref } from "vue";
const svgRect = ref(null);
const wordRects = ref(null);

const ayahContainer = ref(null);

function highlightAyah(ayahNumber) {
  nextTick(() => {
    const spans = document.querySelectorAll(
      `[data-ayah-group="${ayahNumber}"]`
    );
    if (!spans.length || !ayahContainer.value) return;

    const containerRect =
      ayahContainer.value.getBoundingClientRect();

    // rect لكل كلمة
    const rects = [...spans].map(el => {
      const r = el.getBoundingClientRect();
      return {
        left: r.left - containerRect.left,
        top: r.top - containerRect.top,
        width: r.width,
        height: r.height
      };
    });

    // ===============================
    // دمج الكلمات في نفس السطر
    // ===============================
    const tolerance = 5;
    const lineRects = [];

    rects.forEach(r => {
      // هل يوجد سطر قريب؟
      let line = lineRects.find(l =>
        Math.abs(l.top - r.top) <= tolerance
      );

      if (!line) {
        // سطر جديد
        lineRects.push({
          left: r.left,
          top: r.top,
          right: r.left + r.width,
          bottom: r.top + r.height
        });
      } else {
        // توسعة السطر الحالي
        line.left = Math.min(line.left, r.left);
        line.right = Math.max(line.right, r.left + r.width);
        line.top = Math.min(line.top, r.top);
        line.bottom = Math.max(line.bottom, r.top + r.height);
      }
    });

    // تحويل إلى rects نهائية
    const mergedRects = lineRects.map(l => ({
      left: l.left,
      top: l.top,
      width: l.right - l.left,
      height: l.bottom - l.top
    }));

    // ===============================
    // حساب حجم SVG
    // ===============================
    const minX = Math.min(...mergedRects.map(r => r.left));
    const minY = Math.min(...mergedRects.map(r => r.top));
    const maxX = Math.max(...mergedRects.map(r => r.left + r.width));
    const maxY = Math.max(...mergedRects.map(r => r.top + r.height));

    svgRect.value = {
      left: minX,
      top: minY,
      width: maxX - minX,
      height: maxY - minY
    };

    // rects داخل الـ SVG
    wordRects.value = mergedRects.map(r => ({
      x: r.left - minX,
      y: r.top - minY,
      width: r.width,
      height: r.height
    }));
  });
}


let selectedTafsir = ref('qortoby.json')
let selectedTranslation = ref('en_tafheem.json')
let selectedRecitingWay = ref('الآية فقط')
let copyAyahWithTashkeel = ref(true)
onActivated(async () => {
  await handleRouteChange(route.params.number, route.params.scrollTo);
});

const modalType = ref('tafsir') // أو 'translation'


const emit = defineEmits(['update:selectedFile'])
let selectedFile = computed({
  get: () => modalType.value === 'tafsir' ? selectedTafsir.value : selectedTranslation.value,
  set: (value) => {
    if (modalType.value === 'tafsir') selectedTafsir.value = value
    else selectedTranslation.value = value
    emit('update:selectedFile', value)
  }
})
const localStorageKey = 'your-key'

watch(selectedFile, (newFile) => {
  console.log('PARENT Selected file changed:', newFile)
  if (newFile) {
    localStorage.setItem(localStorageKey, newFile)
  }
})

import { computed, watch } from 'vue'


const isPlaying = ref(false)
let currentAudio = null;

function getAudioPath(surahNumber, ayahNumber) {
  const surahStr = String(surahNumber).padStart(3, '0');
  const ayahStr = String(ayahNumber).padStart(3, '0');
  return `assets/sounds/Sa3d_Alghamdy/${surahStr}/${surahStr}${ayahStr}.opus`;
}



function stopAyahAudio() {

  // أوقف الصوت السابق إذا كان شغال
  if (currentAudio) {
    currentAudio.onended = () => {
      currentAudio.pause();
      currentAudio = null;
      isPlaying.value = false;
      surahVariables.value[surah.value.number].longPressedAyahNumber = null;
      return;
    }
  }
}

const goToSurah = (surahNumber) => {
  localStorage.setItem('lastSurah', surahNumber.toString())
  router.replace({ name: 'SurahDetail', params: { number: surahNumber.toString(), scrollTo: 0.0, isReciting: true } })
}


async function waitForSurah() {
  // محاكاة عملية غير متزامنة، مثل استرجاع البيانات من API أو غيرها
  await new Promise((resolve) => {
    const interval = setInterval(() => {
      if (surah.value !== null) {
        clearInterval(interval);
        resolve();
      }
    }, 100); // تحقق كل 100 ملي ثانية إذا صار المتغير غير null
  });

  console.log("تم تحميل السورة: ", surah.value);
}


async function playAyahAudio(surahNumber, ayahNumber, selectedRecitingWay) {
  await handleScrollTo(ayahNumber.toString(), surahNumber);

  const path = getAudioPath(surahNumber, ayahNumber);
  currentAudio = new Audio(path);

  currentAudio.onended = async () => {

    if (selectedRecitingWay === 'الآية فقط') {
      // الوضع الحالي بدون تعديل
    }
    else if (selectedRecitingWay === 'إلى ختم السورة') {
      // عندما يكون يوجد آية إضافية بعد الاية الحالية عينها كآية مختارة وابدأ من جديد
      if (ayahNumber < surah.value.ayahs.length) {
        ayahNumber++;
        surahVariables.value[surahNumber].longPressedAyahNumber = ayahNumber;
        // selectedSurahNumber.value = surahNumber;
        selectedAyahNumber.value = ayahNumber;
        highlightAyah(ayahNumber);
        playAyahAudio(surahNumber, ayahNumber, selectedRecitingWay)
      } else {
        surahVariables.value[surah.value.number].longPressedAyahNumber = null;

      }
    }
    else if (selectedRecitingWay === 'إلى ختم القرآن الكريم') {
      // عندما يكون يوجد آية إضافية بعد الاية الحالية عينها كآية مختارة وابدأ من جديد
      if (ayahNumber < surah.value.ayahs.length) {
        ayahNumber++;
        surahVariables.value[surahNumber].longPressedAyahNumber = ayahNumber;
        // selectedSurahNumber.value = surahNumber;
        selectedAyahNumber.value = ayahNumber;
        highlightAyah(ayahNumber);
        playAyahAudio(surahNumber, ayahNumber, selectedRecitingWay)
      } else {
        if (surah.value.number === 114) {
          stopAyahAudio();
          return;
        }
        const newSurahNumber = surah.value.number + 1;
        surah.value = null;
        goToSurah(newSurahNumber);
        await waitForSurah();
        ayahNumber = 1;
        surahVariables.value[surahNumber].longPressedAyahNumber = ayahNumber;
        selectedSurahNumber.value = surahNumber;
        selectedAyahNumber.value = ayahNumber;
        highlightAyah(ayahNumber);
        playAyahAudio(surahNumber, ayahNumber, selectedRecitingWay)
        // surahVariables.value[surah.value.number].longPressedAyahNumber = null;
      }

    }

    isPlaying.value = false;
  };

  currentAudio.onerror = (e) => {
    console.error('❌ خطأ في تشغيل الصوت:', e);
    isPlaying.value = false;
  };

  try {
    await currentAudio.play();
    isPlaying.value = true;
  } catch (err) {
    console.error('❌ فشل التشغيل:', err);
    isPlaying.value = false;
  }

  showPopover.value = false;
}

function getAyahText(copyAyahWithTashkeel = true) {
  const ayah = surah.value?.ayahs.find(a => a.numberInSurah === selectedAyahNumber.value)
  const ayahText = "﷽ ﴿ " + ayah[copyAyahWithTashkeel ? 'text' : 'no_Tashkeel_text'] + " ﴾";
  return ayahText;
}

function copyAyah(copyAyahWithTashkeel) {
  const ayahText = getAyahText(copyAyahWithTashkeel);
  if (ayahText) {
    navigator.clipboard.writeText(ayahText)
      .then(() => console.log('✅ تم نسخ الآية!'))
      .catch(() => console.log('❌ فشل النسخ.'));
  }
  showPopover.value = false;
}

import basicMeaning from '@/assets/meanings_nested.js';


import { Share } from '@capacitor/share';

const shareAyahText = async () => {
  const copyAyahWithTashkeel = true; // لجلب النص مع تشكيل
  const ayahText = getAyahText(copyAyahWithTashkeel);
  if (ayahText) {
    try {
      await Share.share({
        title: `📖 ${surah.value.name}`,
        text: ayahText,
        dialogTitle: 'مشاركة الآية'
      });
    } catch (err) {
      console.error('خطأ في المشاركة:', err);
    }
  }
}


import TafsirModal from './TafsirModal.vue'
import SurahInfo from './SurahInfo.vue';
import { fonts, languageDisplay, tafsirOptions, translationOptions } from '@/composables/fonts.ts'

const modalOpen = ref(false)
const upperSurahNameShown = ref(true)
const selectedSurah = ref(null)
const selectedAyah = ref(null)


import { IonPopover } from '@ionic/vue'
const showPopover = ref(false)
const popoverEvent = ref(null)  // لتخزين حدث النقر لتموضع النافذة
const selectedSurahNumber = ref(null)
const selectedAyahNumber = ref(null)
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



function setFont(font) {
  fontFamily.value = font;
  localStorage.setItem('fontFamily', font);
  showFontPopover.value = false;
}


function goToI3raab() {
  showPopover.value = false;
  selectedSurah.value = selectedSurahNumber.value;
  selectedAyah.value = selectedAyahNumber.value;
  modalType.value = 'tafsir';
  selectedTafsir.value = 'e3rab.json'; // ← اسم ملف الإعراب عندك
  modalOpen.value = true;
}


function onOption(choice, file, keepOld = false) {

  // إغلاق الـ popover
  showPopover.value = false;

  if (!choice) {
    surahVariables.value[selectedSurahNumber.value].selectedAyahNumber = null;
    return;
  }

  // إذا كانت الآية محددة، افتح الـ popover تلقائيًا
  selectedSurah.value = selectedSurahNumber.value;
  selectedAyah.value = selectedAyahNumber.value;
  modalType.value = choice === 'تفسير' ? 'tafsir' : 'translation';
  modalOpen.value = true;
  if (choice === 'تفسير') {
    selectedTafsir.value = file;
  } else if (choice === 'ترجمة') {
    selectedTranslation.value = file;
  }
  if (!keepOld) {
    selectedFile = file;
  }
}

import { ref, onMounted, nextTick, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import { IonContent, IonHeader, IonPage, IonToolbar, IonList, IonItem } from "@ionic/vue";
import TopToolbar from './TopToolbar.vue'
import { provide } from 'vue'
const route = useRoute()
const surahVariables = ref({}) // { '1': {numberInSurah:5, scrollPosition:100}, '2': {numberInSurah:10, scrollPosition:200} }

const surah = ref(null)
const fontSize = ref(22)
const fontFamily = ref('Uthmani')
const isDark = ref(true)
const scaleYSurahInfo = ref(1.2)
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

function startLongPress(event, surahNumber, ayahNumber, forceTime = null) {
  isPressing.value = true; // بدأ الضغط الطويل
  popoverEvent.value = event;

  pressTimer.value = setTimeout(() => {
    if (isPressing.value && !isScrolling.value) {
      // تأكد من أن الكائن موجود
      if (!surahVariables.value[surahNumber]) {
        surahVariables.value[surahNumber] = { longPressedAyahNumber: null, bookmarkedAyahNumber: null, scrollPosition: null };
      }

      // تعيين قيمة longPressedAyahNumber
      highlightAyah(ayahNumber);
      surahVariables.value[surahNumber].longPressedAyahNumber = ayahNumber;

      selectedSurahNumber.value = surahNumber;
      selectedAyahNumber.value = ayahNumber;
      showPopover.value = true;
    }
  }, forceTime ?? longPressThreshold);
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
  console.log('toggleAyah')
  // إذا كانت الآية محددة بالفعل، قم بإلغاء التحديد
  const current = surahVariables.value[surahNumber]?.selectedAyahNumber || null;

  highlightAyah(ayahNumber);

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

let showCurrentMaany = ref('');
let currentMaanyAyah = ref('');
function setMaany(surah, ayah, index) {
  selectedSurahNumber.value = surah.number;
  selectedAyahNumber.value = ayah.numberInSurah;
  currentMaanyAyah.value = ayah;
  showCurrentMaany.value = basicMeaning[surah.number - 1][ayah.numberInSurah - 1][index][0];
}



onBeforeUnmount(() => {
  window.removeEventListener("resize", checkOrientation);
});

onMounted(async () => {
  checkOrientation(); // أول مرة
  window.addEventListener("resize", checkOrientation);

  isDark.value = localStorage.getItem('isDark') === 'true';
  fontSize.value = parseFloat(localStorage.getItem('fontSize')) || 22;
  scaleYSurahInfo.value = parseFloat(localStorage.getItem('scaleYSurahInfo')) || 1;
  fontFamily.value = localStorage.getItem('fontFamily') || 'Uthmani';

  const stored = localStorage.getItem('surahVariables');
  if (stored) {
    surahVariables.value = JSON.parse(stored);
  }

  // التعامل مع الحالة الأولية
  await handleRouteChange(route.params.number, route.params.scrollTo, route.params.isReciting);
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
  console.log('showPopoverForAyah')
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

async function handleRouteChange(surahNumberParam, scrollToParam, isRecitingParam) {
  const surahNumber = parseInt(surahNumberParam);

  // إعادة تعيين حالة السورة
  surah.value = null;
  await nextTick();

  try {
    // تحميل ملف السورة المناسب
    const res = await fetch(`assets/surahs/surah_${surahNumber}.json`);
    if (!res.ok) throw new Error('Failed to load surah file');

    surah.value = await res.json();

    if (surah.value) {
      Juz.value = surah.value.ayahs[0].juz;
      Page.value = surah.value.ayahs[0].page;
      Hizb.value = surah.value.ayahs[0].hizbQuarter; // تأكد من الاسم الصحيح
    }

    upperSurahNameShown.value = true;

    // الانتظار حتى يتم تحديث DOM
    await nextTick();

    if (scrollToParam) {
      await handleScrollTo(scrollToParam, surahNumber);
    }

    if (isRecitingParam) {
      if (!surahVariables.value[surahNumber]) {
        surahVariables.value[surahNumber] = {
          longPressedAyahNumber: 1,
          bookmarkedAyahNumber: null,
          scrollPosition: null
        };
      }
      selectedSurahNumber.value = surahNumber;
      selectedAyahNumber.value = 1;
      playAyahAudio(surahNumber, selectedAyahNumber.value, "إلى ختم القرآن الكريم");
    }

  } catch (error) {
    console.error("Error loading surah:", error);
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
const toggleUpperSurahInfo = () => {
  upperSurahNameShown.value = !upperSurahNameShown.value
}

provide('increaseFontSize', increaseFontSize)
provide('decreaseFontSize', decreaseFontSize)
provide('toggleTheme', toggleTheme)
provide('toggleUpperSurahInfo', toggleUpperSurahInfo)
provide('openFontPopover', openFontPopover)
provide('isDark', isDark)


const OnlyOnOrientationLandscape = ref(false);
const isDesktop = ref(false);

function checkOrientation() {
  const userAgent = navigator.userAgent || navigator.vendor || window.opera;

  // تحقق إذا كان المتصفح على كمبيوتر (ويندوز أو ماك)
  if (/Windows|Macintosh/i.test(userAgent)) {
    isDesktop.value = true;
  } else {
    isDesktop.value = false;
  }
  OnlyOnOrientationLandscape.value = window.innerWidth > window.innerHeight;
}

</script>

<style scoped>
.vertical-toolbar {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  height: auto;
  padding: 8px;
  height: 30rem;
  position: fixed;
  width: 4rem;
  top: 0;
}

.vertical-toolbar ion-buttons {
  display: flex;
  flex-direction: column;
}

.vertical-toolbar ion-button {
  width: 100%;
  min-width: 100%;
  max-width: 100%;
  margin: 4px 0;
}

@media (orientation: landscape) {

  .ion-header,
  ion-header ion-toolbar:first-of-type,
  ion-toolbar:not(.vertical-toolbar),
  .toolbar-container,
  .horizonal-buttons {
    display: none !important;
  }

  /* .SurahInfo {
    display: none;
  } */

}


@media (orientation: portrait) {

  .vertical-buttons {
    display: none !important;
  }

}
</style>