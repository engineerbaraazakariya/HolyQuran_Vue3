import { ref, onMounted } from 'vue'

export function useQuranSearch() {
  const quranData = ref<any[]>([])  // تخزين البيانات هنا
  const lastSurahNumber = ref<number | null>(null)  // تخزين رقم السورة الأخيرة
  const lastAyahNumber = ref<number | null>(null)  // تخزين رقم الآية الأخيرة

  // تحميل البيانات من الملف عند التهيئة
  async function loadData() {
    const res = await fetch('/assets/quran.json')
    quranData.value = await res.json()
  }

  // دالة البحث التي تعتمد على رقم السورة ورقم الآية
  function search(term: string, startSurahNumber: number, startAyahNumber: number, limit: number) {
    const cleanTerm = term.trim()
    const results: any[] = []
    let foundCount = 0

    // نبحث عبر السور ابتداءً من السورة المحددة
    outerLoop: for (let surahIndex = startSurahNumber - 1; surahIndex < quranData.value.length; surahIndex++) {
      const surah = quranData.value[surahIndex]

      // إذا كانت السورة التي نبحث فيها تبدأ بعد السورة المحددة، ننتقل إليها مباشرة
      let startAyahIndex = (surahIndex === startSurahNumber - 1) ? startAyahNumber - 1 : 0;

      // نبحث داخل الآيات بدءًا من رقم الآية المحدد
      for (let ayahIndex = startAyahIndex; ayahIndex < surah.ayahs.length; ayahIndex++) {
        const ayah = surah.ayahs[ayahIndex]

        lastSurahNumber.value = surah.number  // حفظ رقم السورة التي وصلنا عندها
        lastAyahNumber.value = ayah.numberInSurah  // حفظ رقم الآية التي وصلنا عندها

        // نتأكد إذا كانت الآية تحتوي على الكلمة المطلوبة
        if (ayah.no_Tashkeel_text && ayah.no_Tashkeel_text.includes(cleanTerm)) {
          // إذا وجدنا نتيجة، نضيفها للنتائج
          results.push({
            surahName: surah.name,
            surahNumber: surah.number,
            ayahNumber: ayah.numberInSurah,
            text: ayah.text,
          })
          foundCount++

          // إذا وصلنا لعدد النتائج المحدد (20 نتيجة)، نتوقف
          if (foundCount >= limit) {
            break outerLoop
          }
        }
      }
    }

    // لما يتم الانتهاء من البحث ولم يبق المزيد من امكانية البحث يتم تحديث هذه
    if (lastSurahNumber.value === 114 && lastAyahNumber.value === 6) {
      results[results.length - 1].noMoreResults = true;
    }
    // إرجاع النتائج بعد التوقف عند أول 20 نتيجة
    return results
  }

  onMounted(loadData)

  return {
    search,
    quranData,
    lastSurahNumber,
    lastAyahNumber
  }
}
