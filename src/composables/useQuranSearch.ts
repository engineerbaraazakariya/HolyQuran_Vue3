import { ref, onMounted } from 'vue'

export function useQuranSearch() {
  const quranData = ref<any[]>([])  // تخزين البيانات هنا
  const lastAyahNumber = ref<number | null>(null)  // تخزين رقم الآية الأخيرة

  // تحميل البيانات من الملف عند التهيئة
  async function loadData() {
    const res = await fetch('/assets/quran.json')
    quranData.value = await res.json()
  }

  // دالة البحث التي تعتمد على رقم الآية الأخير
  function search(term: string, startAyahNumber: number, limit: number) {
    const cleanTerm = term.trim()
    const results: any[] = []

    // نبحث عبر السور والآيات باستخدام حلقة for
    outerLoop: for (const surah of quranData.value) {
      let foundCount = 0

      for (const ayah of surah.ayahs) {
        // نتأكد إذا كانت الآية تحتوي على الكلمة المطلوبة
        if (ayah.no_Tashkeel_text && ayah.no_Tashkeel_text.includes(cleanTerm)) {
          // إذا وجدنا نتيجة، نضيفها للنتائج
          results.push({
            surahName: surah.name,
            surahNumber: surah.number,
            ayahNumber: ayah.numberInSurah,
            text: ayah.text
          })
          foundCount++

          // إذا وصلنا لعدد النتائج المحدد (20 نتيجة)، نتوقف
          if (foundCount >= limit) {
            break outerLoop
          }
        }

        // إذا كانت الآية رقمها أكبر من الرقم الذي بدأنا منه، ننهي البحث في هذه السورة
        if (ayah.numberInSurah > startAyahNumber) {
          break
        }
      }
    }

    // إرجاع النتائج بعد التوقف عند أول 20 نتيجة
    return results
  }

  onMounted(loadData)

  return {
    search,
    quranData,
    lastAyahNumber // نرجع رقم الآية الأخيرة لتستخدمه في التطبيق
  }
}
