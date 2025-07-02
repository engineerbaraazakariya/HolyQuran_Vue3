<template>
  <ion-page :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
    <ion-header :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
      <ion-toolbar :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
        <ion-title>البحث في القرآن</ion-title>
      </ion-toolbar>
      <ion-toolbar :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
        <ion-searchbar v-model="searchTerm" @ionInput="handleSearch" placeholder="أدخل كلمة للبحث"
          :class="{ 'dark-theme': isDark, 'white-theme': !isDark }" />
      </ion-toolbar>
    </ion-header>

    <ion-content :class="{ 'dark-theme': isDark, 'white-theme': !isDark }" @ionInfinite="loadMoreResults"
      scroll-events="true">
      <ion-list v-if="results.length > 0" :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
        <ion-item v-for="(result, index) in results" :key="index" button @click="goToSurah(result)"
          :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
          <ion-label :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
            <h3 :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">{{ result.surahName }} - آية {{
              result.ayahNumber }}</h3>
            <p :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">{{ result.text }}</p>
          </ion-label>
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



  </ion-page>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useQuranSearch } from '@/composables/useQuranSearch'
import { useRouter } from 'vue-router'
import { IonContent, IonHeader, IonPage, IonItem, IonTitle, IonToolbar, IonText, IonList, IonLabel, IonSearchbar, IonInfiniteScrollContent, IonInfiniteScroll } from "@ionic/vue";

import debounce from 'lodash.debounce'


const isDark = ref(false)
const { search, lastSurahNumber, lastAyahNumber } = useQuranSearch()
const searchTerm = ref('')
const results = ref<any[]>([])  // لتخزين النتائج الحالية
const isLoading = ref(false)  // لتتبع حالة التحميل
const page = ref(1)  // الصفحة الحالية (مبدئيًا من 1)
// الدالة التي يتم تفعيلها بعد كل كتابة (debounced)
const handleSearch = debounce(() => {
  if (searchTerm.value.trim().length >= 2) {
    results.value = []  // إفراغ النتائج السابقة
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

  results.value = [...results.value, ...newResults];

  isLoading.value = false;
}

function loadMoreResults(event: any) {
  loadResults();  // تحميل المزيد من النتائج
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
</script>
