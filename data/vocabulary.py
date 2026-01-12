import logging
import re

try:
    from data.jejer_list import JEJER_VOCAB
    from data.wasesa_list import WASESA_TRANSITIVE, WASESA_INTRANSITIVE
    from data.lesan_list import LESAN_VOCAB
    from data.ks_list import KS_VOCAB
    from data.kw_list import KW_VOCAB
    from data.konj_list import KONJ_VOCAB
    from data.ket_list import KET_VOCAB
except ImportError as e:
    print(f"Error import kosakata: {e}")
    # Data fallback minimal
    JEJER_VOCAB = ['aku', 'kowe', 'bapak', 'ibu', 'adik']
    WASESA_TRANSITIVE = ['mangan', 'ngombe', 'maca', 'nulis', 'tuku']
    WASESA_INTRANSITIVE = ['turu', 'mlaku', 'nangis', 'lunga', 'seneng']
    LESAN_VOCAB = ['sego', 'banyu', 'buku', 'omah', 'pitik']
    KS_VOCAB = ['gedhe', 'pinter', 'anyar', 'banget', 'tenan']
    KW_VOCAB = ['siji', 'loro', 'telu', 'papat', 'lima']
    KONJ_VOCAB = ['lan', 'utawa']
    KET_VOCAB = ['wingi', 'sesuk', 'ing omah']

class Vocabulary:
    def __init__(self):
        # Inisialisasi semua kosakata dari file data
        self.jejer = JEJER_VOCAB
        self.wasesa_transitive = WASESA_TRANSITIVE
        self.wasesa_intransitive = WASESA_INTRANSITIVE
        self.lesan = LESAN_VOCAB
        self.ks = KS_VOCAB
        self.kw = KW_VOCAB
        self.konj = KONJ_VOCAB
        self.ket = KET_VOCAB
        
        # Regex untuk mendeteksi kata kepemilikan
        self.possessive_pattern = re.compile(r'^(.*?)(ku|mu|ne|e)$')
        
        # Kata-kata yang TIDAK boleh dipisah (kata dasar yang berakhiran sama)
        self.no_split_words = {'aku', 'kowe', 'sira', 'rika', 'dheweke', 'kita'}
        
        # Mapping khusus untuk kata umum yang ambigu
        self.special_mapping = {
            'banget': 'KS',      # Prioritas sebagai KS
            'tenan': 'KS',
            'pisan': 'KS',
            'moco': 'WASESA_TRANS',  # Sinonim maca
            'maos': 'WASESA_TRANS',  # Sinonim maca
        }
        
        self.word_types = {}
        self._build_word_types()
        
        print(f"\n[VOCAB] 📚 Kosakata dimuat:")
        print(f"  🔵 Jejer: {len(self.jejer)} kata")
        print(f"  🔴 Wasesa Transitif: {len(self.wasesa_transitive)} kata")
        print(f"  🟠 Wasesa Intransitif: {len(self.wasesa_intransitive)} kata")
        print(f"  🟢 Lesan: {len(self.lesan)} kata")
        print(f"  🟣 KS: {len(self.ks)} kata")
        print(f"  🟡 KW: {len(self.kw)} kata")
        print(f"  ⚫ Konjungsi: {len(self.konj)} kata")
        print(f"  ⚪ Keterangan: {len(self.ket)} kata")
        print(f"  📊 Total unik: {len(self.word_types)} kata")

    def _build_word_types(self):
        """Bangun mapping kata ke tipe token dengan prioritas"""
        self.word_types = {}
        
        # PRIORITAS 1: Kata khusus (special mapping)
        for word, word_type in self.special_mapping.items():
            self.word_types[word.lower()] = word_type
        
        # PRIORITAS 2: KS (Kata Sifat)
        for word in self.ks:
            word_lower = word.lower()
            if word_lower not in self.word_types:
                self.word_types[word_lower] = 'KS'
        
        # PRIORITAS 3: KETRANGAN
        for word in self.ket:
            word_lower = word.lower()
            if word_lower not in self.word_types:
                self.word_types[word_lower] = 'KETRANGAN'
        
        # PRIORITAS 4: JEJER (Subjek)
        for word in self.jejer:
            word_lower = word.lower()
            if word_lower not in self.word_types:
                self.word_types[word_lower] = 'JEJER'
        
        # PRIORITAS 5: WASESA TRANSITIF
        for word in self.wasesa_transitive:
            word_lower = word.lower()
            if word_lower not in self.word_types:
                self.word_types[word_lower] = 'WASESA_TRANS'
        
        # PRIORITAS 6: WASESA INTRANSITIF
        for word in self.wasesa_intransitive:
            word_lower = word.lower()
            if word_lower not in self.word_types:
                self.word_types[word_lower] = 'WASESA_INTRANS'
        
        # PRIORITAS 7: LESAN (Objek)
        for word in self.lesan:
            word_lower = word.lower()
            if word_lower not in self.word_types:
                self.word_types[word_lower] = 'LESAN'
        
        # PRIORITAS 8: KW (Kata Bilangan)
        for word in self.kw:
            word_lower = word.lower()
            if word_lower not in self.word_types:
                self.word_types[word_lower] = 'KW'
        
        # PRIORITAS 9: KONJUNGSI
        for word in self.konj:
            word_lower = word.lower()
            if word_lower not in self.word_types:
                self.word_types[word_lower] = 'KONJ'

    def normalize_word(self, word):
        """
        Normalisasi kata dengan handling kepemilikan.
        Mengembalikan: (kata_dasar, marker_kepemilikan, is_possessive)
        """
        word_lower = word.lower()
        
        # Cek apakah kata termasuk dalam no_split
        if word_lower in self.no_split_words:
            return word_lower, None, False
        
        # Cek pola kepemilikan
        match = self.possessive_pattern.match(word_lower)
        if match:
            base_word = match.group(1)
            marker = match.group(2)
            
            # Validasi: base_word harus ada dalam kosakata
            if base_word and base_word in self.word_types:
                # Kata seperti "omahe" (e) vs "omah" + "e"
                if marker == 'e' and len(base_word) >= 2:
                    return base_word, marker, True
                elif marker in ['ku', 'mu', 'ne']:
                    return base_word, marker, True
        
        # Tidak ada kepemilikan
        return word_lower, None, False

    def get_word_type(self, word):
        """
        Dapatkan tipe token untuk kata dengan normalisasi.
        """
        # Normalisasi kata terlebih dahulu
        normalized, marker, is_possessive = self.normalize_word(word)
        
        # Cari tipe untuk kata yang sudah dinormalisasi
        result = self.word_types.get(normalized)
        
        if result:
            info = f"'{word}'"
            if is_possessive:
                info += f" → '{normalized}' (kepemilikan: {marker})"
            info += f" → {result}"
            print(f"[VOCAB] {info}")
            return result
        else:
            # Coba langsung tanpa normalisasi
            direct_result = self.word_types.get(word.lower())
            if direct_result:
                print(f"[VOCAB] '{word}' → {direct_result}")
                return direct_result
        
        print(f"[VOCAB] '{word}' → TIDAK DIKENAL")
        return None

    def get_possessive_info(self, word):
        """
        Mendapatkan informasi kepemilikan untuk kata.
        """
        normalized, marker, is_possessive = self.normalize_word(word)
        word_type = self.word_types.get(normalized) or self.word_types.get(word.lower())
        
        return {
            'original': word,
            'normalized': normalized,
            'marker': marker,
            'is_possessive': is_possessive,
            'type': word_type
        }

    def suggest_corrections(self, word, max_distance=2):
        """Saran koreksi untuk kata yang tidak dikenal"""
        suggestions = []
        word_lower = word.lower()
        
        # Coba normalisasi dulu
        normalized, _, _ = self.normalize_word(word)
        if normalized in self.word_types:
            suggestions.append((normalized, 0))
        
        # Cek Levenshtein distance
        for known_word in self.word_types.keys():
            distance = self._levenshtein_distance(word_lower, known_word)
            if distance <= max_distance:
                suggestions.append((known_word, distance))
        
        # Cek tanpa normalisasi
        for known_word in self.word_types.keys():
            if word_lower in known_word or known_word in word_lower:
                suggestions.append((known_word, 1))
        
        # Hapus duplikat dan urutkan
        unique_suggestions = []
        seen = set()
        for word_sug, dist in suggestions:
            if word_sug not in seen:
                unique_suggestions.append((word_sug, dist))
                seen.add(word_sug)
        
        unique_suggestions.sort(key=lambda x: x[1])
        return [word for word, _ in unique_suggestions[:5]]

    def _levenshtein_distance(self, s1, s2):
        """Menghitung jarak Levenshtein"""
        if len(s1) < len(s2):
            return self._levenshtein_distance(s2, s1)
        
        if len(s2) == 0:
            return len(s1)
        
        previous_row = range(len(s2) + 1)
        
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        
        return previous_row[-1]
    
    def get_vocabulary_stats(self):
        """Statistik kosakata"""
        return {
            'jejer': len(self.jejer),
            'wasesa_transitive': len(self.wasesa_transitive),
            'wasesa_intransitive': len(self.wasesa_intransitive),
            'lesan': len(self.lesan),
            'ks': len(self.ks),
            'kw': len(self.kw),
            'konj': len(self.konj),
            'ket': len(self.ket),
            'total_unique': len(self.word_types)
        }
    
    def find_word_by_type(self, word_type):
        """Cari semua kata dengan tipe tertentu"""
        words = []
        for word, w_type in self.word_types.items():
            if w_type == word_type:
                words.append(word)
        return words
    
    def is_word_in_vocab(self, word):
        """Cek apakah kata ada dalam kosakata"""
        normalized, _, _ = self.normalize_word(word)
        return normalized in self.word_types or word.lower() in self.word_types