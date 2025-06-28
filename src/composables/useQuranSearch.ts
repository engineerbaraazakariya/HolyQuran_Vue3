import { ref, onMounted } from 'vue'

export function useQuranSearch() {
  const quranData = ref<any[]>([])

  async function loadData() {
    const res = await fetch('/assets/quran.json')
    quranData.value = await res.json()
  }

  function search(term: string) {
    const cleanTerm = term.trim()

    return quranData.value.flatMap(surah =>
      surah.ayahs
        .filter(ayah =>
          ayah.no_Tashkeel_text && ayah.no_Tashkeel_text.includes(cleanTerm)
        )
        .map(ayah => ({
          surahName: surah.name,
          surahNumber: surah.number,
          ayahNumber: ayah.numberInSurah,
          text: ayah.text
        }))
    )
  }


  onMounted(loadData)

  return {
    search, // ✅ لازم تكون مرجّعة هي الدالة
    quranData
  }
}
