import { ref, onMounted } from 'vue'

export function useQuranSearch() {
  const quranData = ref<any[]>([])
  const lastSurahNumber = ref<number | null>(null)
  const lastAyahNumber = ref<number | null>(null)

  async function loadData() {
    const res = await fetch('assets/quran.json')
    quranData.value = await res.json()
  }

  function removeTashkeel(text: string) {
    return text
      .replace(/[\u064B-\u065F\u0670\u06D6-\u06ED]/g, '')
      .replace(/ٱ/g, 'ا')
      .trim()
  }

  function searchSurahs(term: string) {
    const t = removeTashkeel(term)
    if (!t) return []

    return quranData.value
      .filter((s: any) => removeTashkeel(s.name).includes(t))
      .map((s: any) => ({
        type: 'surah',
        surahNumber: s.number,
        surahName: s.name,
        ayahNumber: s.ayahs?.[0]?.numberInSurah || 1,
        text: s.ayahs?.[0]?.text || '',
        no_Tashkeel_text: s.ayahs?.[0]?.no_Tashkeel_text || ''
      }))
  }

  function search(term: string, startSurahNumber: number, startAyahNumber: number, limit: number) {
    const cleanTerm = term.trim()
    const results: any[] = []
    let foundCount = 0

    outerLoop: for (let surahIndex = startSurahNumber - 1; surahIndex < quranData.value.length; surahIndex++) {
      const surah = quranData.value[surahIndex]
      let startAyahIndex = (surahIndex === startSurahNumber - 1) ? startAyahNumber - 1 : 0

      for (let ayahIndex = startAyahIndex; ayahIndex < surah.ayahs.length; ayahIndex++) {
        const ayah = surah.ayahs[ayahIndex]
        lastSurahNumber.value = surah.number
        lastAyahNumber.value = ayah.numberInSurah

        if (ayah.no_Tashkeel_text && ayah.no_Tashkeel_text.includes(cleanTerm)) {
          results.push({
            surahName: surah.name,
            surahNumber: surah.number,
            ayahNumber: ayah.numberInSurah,
            text: ayah.text,
            no_Tashkeel_text: ayah.no_Tashkeel_text
          })
          foundCount++
          if (foundCount >= limit) break outerLoop
        }
      }
    }

    if (results[results.length - 1] && lastSurahNumber.value === 114 && lastAyahNumber.value === 6) {
      results[results.length - 1].noMoreResults = true
    }

    return results
  }

  onMounted(loadData)

  return {
    quranData,
    lastSurahNumber,
    lastAyahNumber,
    loadData,
    search,
    searchSurahs,
    removeTashkeel
  }
}
