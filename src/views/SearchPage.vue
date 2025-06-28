<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>البحث في القرآن</ion-title>
      </ion-toolbar>
      <ion-toolbar>
        <ion-searchbar
          v-model="searchTerm"
          @ionInput="handleSearch"
          placeholder="أدخل كلمة للبحث" />
      </ion-toolbar>
    </ion-header>

    <ion-content>
      <ion-list v-if="results.length > 0">
        <ion-item
          v-for="(result, index) in results"
          :key="index"
          button
          @click="goToSurah(result)">
          <ion-label>
            <h3>{{ result.surahName }} - آية {{ result.ayahNumber }}</h3>
            <p>{{ result.text }}</p>
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
import { ref } from 'vue'
import { useQuranSearch } from '@/composables/useQuranSearch'
import { useRouter } from 'vue-router'
import { IonContent, IonHeader, IonPage, IonIcon, IonItem, IonTitle, IonSegment, IonSegmentButton, IonToolbar, IonButtons, IonButton, IonText, IonList, IonLabel, IonSearchbar } from "@ionic/vue";

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
