<template>
  <ion-app class="!mt-4">
    <ion-router-outlet />
  </ion-app>
</template>

<script setup lang="ts">
import { IonApp, IonRouterOutlet } from '@ionic/vue';
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
onMounted(() => {
  const lastSurah = localStorage.getItem('lastSurah')
  const scrollOffset = localStorage.getItem('scrollOffset')

  if (lastSurah) {
    router.replace({
      name: 'SurahDetail',
      params: {
        number: Number(lastSurah),
        scrollTo: Number(scrollOffset || 0),
      },
    })
  }
})


</script>


<style>
@font-face {
  font-family: 'Amiri';
  src: url('/assets/AmiriQuran-Regular.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'Uthmani';
  src: url('/assets/uthmani.otf') format('opentype');
  font-weight: normal;
  font-style: normal;
}


@font-face {
  font-family: 'MeQuran';
  src: url('/assets/MeQuran.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'DecoType';
  src: url('/assets/DecoType.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'Hafs';
  src: url('/assets/Hafs.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}

@font-face {
  font-family: 'Nabi';
  src: url('/assets/Nabi.ttf') format('truetype');
  font-weight: normal;
  font-style: normal;
}
</style>