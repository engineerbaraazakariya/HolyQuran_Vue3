<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  isOpen: Boolean,
  surahNumber: Number,
  ayahNumber: Number,
  type: String // 'tafsir' or 'translation'
})

const emit = defineEmits(['close'])

const content = ref('')
const isLoading = ref(false)

watch(() => [props.surahNumber, props.ayahNumber, props.isOpen, props.type], async ([sura, aya, open, type]) => {
  if (open && sura && aya) {
    isLoading.value = true

    const filePath =
      type === 'translation'
        ? '/assets/tarajem/en_sahih.json'
        : '/assets/tafasir/katheer.json'

    const res = await fetch(filePath)
    const data = await res.json()

    const match = data.find(item => item.sura === sura && item.aya === aya)
    content.value = match ? match.text : 'لم يتم العثور على محتوى'
    isLoading.value = false
  }
})
</script>

<template>
  <ion-modal :is-open="isOpen" @didDismiss="emit('close')">
    <ion-header>
      <ion-toolbar color="primary">
        <ion-title>{{ type === 'translation' ? 'الترجمة' : 'التفسير' }}</ion-title>
        <ion-buttons slot="end">
          <ion-button @click="emit('close')">إغلاق</ion-button>
        </ion-buttons>
      </ion-toolbar>
    </ion-header>

    <ion-content class="ion-padding">
      <div v-if="isLoading">جاري التحميل...</div>
      <div v-else>
        <div v-if="type === 'tafsir'" v-html="content" />
        <div v-else>{{ content }}</div>
      </div>
    </ion-content>
  </ion-modal>
</template>
