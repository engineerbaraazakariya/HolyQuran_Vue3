<template>
  <ion-page>
    <ion-header>
      <ion-toolbar>
        <ion-title>القرآن الكريم</ion-title>
      </ion-toolbar>
    </ion-header>

    <ion-content>
      <ion-list v-if="surahs.length">
        <ion-item
          v-for="surah in surahs"
          :key="surah.number"
          @click="goToSurah(surah)"
        >
          {{ surah.name }}
        </ion-item>
      </ion-list>
    </ion-content>
  </ion-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const surahs = ref([])
const router = useRouter()

const fetchSurahs = async () => {
  const res = await fetch('/assets/quran.json')
  const data = await res.json()
  surahs.value = data
}

onMounted(fetchSurahs)

const goToSurah = (surah) => {
  router.push({ name: 'SurahDetail', params: { number: surah.number } })
}
</script>
