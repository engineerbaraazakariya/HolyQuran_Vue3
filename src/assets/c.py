import json
import re
import unicodedata

class QuranExplanationsProcessor:
    def __init__(self):
        # علامات التشكيل
        self.tashkeel_pattern = re.compile(r'[\u0610-\u061A\u064B-\u065F\u0670]')
        # الرموز الخاصة في القرآن
        self.special_chars = re.compile(r'[﴿﴾۝۞﻿]')
        # علامات الوقف في القرآن
        self.stop_marks = ['ۛ', 'ۖ', 'ۗ', 'ۘ', 'ۙ', 'ۚ', 'ۛ', 'ۜ', '۞', '۩']
        
    def normalize_arabic(self, text):
        """تطبيع النص العربي للمقارنة"""
        if not text:
            return ""
        text = self.tashkeel_pattern.sub('', text)
        return text.strip()
    
    def remove_stop_marks(self, text):
        """إزالة علامات الوقف من النص"""
        if not text:
            return text
        for mark in self.stop_marks:
            text = text.replace(mark, '')
        return text
    
    def load_quran_file(self, filename):
        """تحميل ملف القرآن الكريم"""
        with open(filename, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    def load_meanings_file(self, filename):
        """تحميل ملف الشروحات"""
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            content = re.sub(r'^(const|let|var)\s+meanings\s*=\s*', '', content)
            content = re.sub(r'export\s+default\s+meanings\s*;?\s*$', '', content)
            content = re.sub(r';\s*$', '', content)
            content = content.strip()
            return json.loads(content)
    
    def save_meanings_file(self, filename, data, all_ayah_words):
        """حفظ ملف الشروحات المحدث مع التعليقات"""
        with open(filename, 'w', encoding='utf-8') as file:
            file.write('const meanings = [\n')
            
            for surah_idx, surah in enumerate(data):
                file.write(f'  [ // سورة {surah_idx + 1}\n')
                
                for ayah_idx, ayah in enumerate(surah):
                    file.write(f'    [ // آية {ayah_idx + 1}\n')
                    
                    words = all_ayah_words.get(f"{surah_idx}_{ayah_idx}", [])
                    
                    for word_idx, word in enumerate(ayah):
                        if word:
                            file.write(f'      {json.dumps(word, ensure_ascii=False)}')
                        else:
                            file.write('      []')
                        
                        if word_idx < len(ayah) - 1:
                            file.write(',')
                        
                        if word_idx < len(words):
                            word_text = words[word_idx]
                            file.write(f' // {word_text}\n')
                        else:
                            file.write(f' // كلمة {word_idx + 1}\n')
                    
                    file.write('    ]')
                    if ayah_idx < len(surah) - 1:
                        file.write(',\n')
                    else:
                        file.write('\n')
                
                file.write('  ]')
                if surah_idx < len(data) - 1:
                    file.write(',\n')
                else:
                    file.write('\n')
            
            file.write('];\n\n')
            file.write('export default meanings;\n')
    
    def get_clean_ayah_text(self, ayah):
        """الحصول على نص الآية"""
        if isinstance(ayah, dict):
            if 'text' in ayah and ayah['text']:
                return ayah['text'].strip()
            elif 'no_Tashkeel_text' in ayah and ayah['no_Tashkeel_text']:
                return ayah['no_Tashkeel_text'].strip()
        elif isinstance(ayah, str):
            return ayah.strip()
        return ""
    
    def split_ayah_into_words(self, ayah_text):
        """تقسيم الآية إلى كلمات"""
        if not ayah_text:
            return []
        
        # إزالة البسملة
        ayah_text = re.sub(r'^بِسۡمِ ٱللَّهِ ٱلرَّحۡمَـٰنِ ٱلرَّحِيمِ', '', ayah_text)
        ayah_text = re.sub(r'^﷽', '', ayah_text)
        
        # إزالة علامات الوقف
        ayah_text = self.remove_stop_marks(ayah_text)
        
        # إزالة الرموز الخاصة
        ayah_text = self.special_chars.sub('', ayah_text)
        
        # تقسيم على المسافات
        words = [word.strip() for word in ayah_text.split() if word.strip()]
        
        return words
    
    def extract_explanations_from_source(self, meanings_data):
        """استخراج الشروحات من المصدر مع تفاصيلها"""
        explanations = []
        
        print("\n🔍 جاري استخراج الشروحات من المصدر...")
        
        for surah_idx, surah in enumerate(meanings_data):
            if not isinstance(surah, list):
                continue
                
            for ayah_idx, ayah_meanings in enumerate(surah):
                if not isinstance(ayah_meanings, list):
                    continue
                
                for word_idx, meaning in enumerate(ayah_meanings):
                    if meaning and isinstance(meaning, list) and len(meaning) > 0:
                        meaning_text = meaning[0]
                        if isinstance(meaning_text, str) and ':' in meaning_text:
                            word, explanation = meaning_text.split(':', 1)
                            word = word.strip()
                            explanation = explanation.strip()
                            
                            explanations.append({
                                'surah': surah_idx,
                                'ayah': ayah_idx,
                                'position': word_idx,
                                'word': word,
                                'explanation': explanation,
                                'full_text': meaning_text,
                                'word_parts': word.split()  # تقسيم الكلمة المركبة
                            })
                            
                            print(f"  ✓ شرح في سورة {surah_idx+1}, آية {ayah_idx+1}, موقع {word_idx}: '{word}'")
        
        print(f"\n📊 إجمالي الشروحات: {len(explanations)}")
        return explanations
    
    def find_sequences_in_ayah(self, words, explanations):
        """البحث عن جميع تسلسلات الكلمات المركبة في الآية"""
        found_positions = set()
        
        for exp in explanations:
            if len(exp['word_parts']) > 1:  # كلمة مركبة
                parts = exp['word_parts']
                parts_clean = [self.normalize_arabic(p) for p in parts]
                
                # البحث عن التسلسل
                for i in range(len(words) - len(parts) + 1):
                    sequence = words[i:i + len(parts)]
                    sequence_clean = [self.normalize_arabic(w) for w in sequence]
                    
                    if sequence_clean == parts_clean:
                        # وجدنا تسلسل - نضع الشرح على كل كلمة في التسلسل
                        print(f"      ✓ وجد تسلسل '{exp['word']}' في المواقع {i} إلى {i + len(parts) - 1}")
                        return i, i + len(parts) - 1, exp
        
        return None, None, None
    
    def process_ayah(self, ayah_text, surah_idx, ayah_idx, all_explanations):
        """معالجة آية واحدة ووضع الشروحات على كل الكلمات المستحقة"""
        # تقسيم الآية إلى كلمات
        words = self.split_ayah_into_words(ayah_text)
        
        # إنشاء مصفوفة النتائج
        result = [[] for _ in range(len(words))]
        
        # الحصول على شروحات هذه الآية
        ayah_explanations = [
            exp for exp in all_explanations 
            if exp['surah'] == surah_idx and exp['ayah'] == ayah_idx
        ]
        
        if not ayah_explanations:
            return result, words
        
        print(f"\n  📝 آية {ayah_idx + 1}: {len(words)} كلمة, {len(ayah_explanations)} شرح")
        
        # معالجة كل شرح
        for exp in ayah_explanations:
            if len(exp['word_parts']) > 1:
                # كلمة مركبة - نبحث عن التسلسل الكامل
                parts = exp['word_parts']
                parts_clean = [self.normalize_arabic(p) for p in parts]
                
                for i in range(len(words) - len(parts) + 1):
                    sequence = words[i:i + len(parts)]
                    sequence_clean = [self.normalize_arabic(w) for w in sequence]
                    
                    if sequence_clean == parts_clean:
                        # نضع نفس الشرح على كل كلمة في التسلسل
                        for j in range(len(parts)):
                            result[i + j] = [exp['full_text']]
                            print(f"      ✓ '{words[i + j]}' (موقع {i + j}) -> شرح: '{exp['word']}'")
                        break
            else:
                # كلمة مفردة
                word_clean = self.normalize_arabic(exp['word'])
                for i, word in enumerate(words):
                    if self.normalize_arabic(word) == word_clean and not result[i]:
                        result[i] = [exp['full_text']]
                        print(f"      ✓ '{word}' (موقع {i}) -> شرح: '{exp['word']}'")
                        break
        
        return result, words
    
    def run(self):
        """تشغيل المعالج"""
        try:
            # تحميل الملفات
            print("📖 جاري تحميل ملف القرآن...")
            quran_data = self.load_quran_file('quran.json')
            
            print("📚 جاري تحميل ملف الشروحات...")
            meanings_data = self.load_meanings_file('meanings_source.js')
            
            # استخراج الشروحات
            all_explanations = self.extract_explanations_from_source(meanings_data)
            
            # تجهيز هيكل البيانات
            new_meanings = []
            all_ayah_words = {}
            
            # الحصول على قائمة السور
            if isinstance(quran_data, dict) and 'surahs' in quran_data:
                surahs = quran_data['surahs']
            elif isinstance(quran_data, list):
                surahs = quran_data
            else:
                surahs = [quran_data]
            
            print(f"\n📖 عدد السور: {len(surahs)}")
            
            # معالجة كل سورة
            total_explanations_placed = 0
            
            for surah_idx, surah in enumerate(surahs):
                surah_meanings = []
                
                if isinstance(surah, dict) and 'ayahs' in surah:
                    ayahs = surah['ayahs']
                    surah_name = surah.get('name', f'السورة {surah_idx + 1}')
                elif isinstance(surah, list):
                    ayahs = surah
                    surah_name = f'السورة {surah_idx + 1}'
                else:
                    continue
                
                print(f"\n🔄 معالجة {surah_name} ({len(ayahs)} آية)")
                
                for ayah_idx, ayah in enumerate(ayahs):
                    ayah_text = self.get_clean_ayah_text(ayah)
                    
                    if not ayah_text:
                        surah_meanings.append([])
                        all_ayah_words[f"{surah_idx}_{ayah_idx}"] = []
                        continue
                    
                    # معالجة الآية
                    processed_ayah, words = self.process_ayah(
                        ayah_text, surah_idx, ayah_idx, all_explanations
                    )
                    
                    # تخزين الكلمات
                    all_ayah_words[f"{surah_idx}_{ayah_idx}"] = words
                    
                    # التأكد من تطابق الأطوال
                    if len(processed_ayah) != len(words):
                        if len(processed_ayah) < len(words):
                            processed_ayah.extend([[] for _ in range(len(words) - len(processed_ayah))])
                        else:
                            processed_ayah = processed_ayah[:len(words)]
                    
                    surah_meanings.append(processed_ayah)
                    
                    # إحصائيات
                    explained = sum(1 for w in processed_ayah if w)
                    total_explanations_placed += explained
                    
                    if explained > 0:
                        print(f"    الآية {ayah_idx + 1}: {explained}/{len(words)} كلمات مفسرة")
                
                new_meanings.append(surah_meanings)
            
            # حفظ الملف
            print("\n💾 جاري حفظ الملف...")
            self.save_meanings_file('meanings_nested.js', new_meanings, all_ayah_words)
            
            # إحصائيات نهائية
            total_words = sum(len(ayah) for surah in new_meanings for ayah in surah)
            
            print(f"\n✅ تم الانتهاء بنجاح!")
            print(f"📊 إجمالي الكلمات: {total_words}")
            print(f"📊 الشروحات الموضوعة: {total_explanations_placed}")
            print(f"📊 الشروحات في المصدر: {len(all_explanations)}")
            if total_words > 0:
                print(f"📊 نسبة التفسير: {total_explanations_placed/total_words*100:.2f}%")
            
        except Exception as e:
            print(f"❌ خطأ: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    processor = QuranExplanationsProcessor()
    processor.run()