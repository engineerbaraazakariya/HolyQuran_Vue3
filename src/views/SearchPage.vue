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

    <ion-content :class="{ 'dark-theme': isDark, 'white-theme': !isDark }">
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
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useQuranSearch } from '@/composables/useQuranSearch'
import { useRouter } from 'vue-router'
import { IonContent, IonHeader, IonPage, IonItem, IonTitle, IonToolbar, IonText, IonList, IonLabel, IonSearchbar } from "@ionic/vue";
const isDark = ref(false)
const { search } = useQuranSearch()
const searchTerm = ref('')
const results = ref<any[]>([])

const router = useRouter()

function handleSearch() {
  if (searchTerm.value.trim().length >= 2) {
    results.value = search(searchTerm.value.trim())
  } else {
    results.value = []
  }
}

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
  })
}
</script>
