import logging


try:
    from data.jejer_list import JEJER_VOCAB
    from data.wasesa_list import WASESA_VOCAB
    from data.lesan_list import LESAN_VOCAB
except ImportError:
    print("Error: gagal import daftar kosakata dari modul data.")
    JEJER_VOCAB = ['aku', 'kowe', 'panjenengan', 'dheweke', 'kita', 'sampeyan', 'bapak', 'ibu', 'adik', 'mas', 'mbak']
    WASESA_VOCAB = ['mangan', 'ngombe', 'tuku', 'maca', 'nulis', 'nggawa', 'nyapu', 'ndelok', 'ngomong', 'turun']
    LESAN_VOCAB = ['sego', 'roti', 'banyu', 'buku', 'layang', 'tas', 'latar', 'klambi', 'pitik', 'iwak']


class Vocabulary:
    def __init__(self):
        
        # Daftar kosakata untuk setiap kategori token

        # Jejer (subjek)
        self.jejer = JEJER_VOCAB
        # Wasesa (predikat)
        self.wasesa = WASESA_VOCAB
        
        # Lesan (objek)
        self.lesan = LESAN_VOCAB

        self.word_types={}
        self._word_mapping()

    def _word_mapping(self):
        for word in self.jejer:
            self.word_types[word] = 'JEJER'
        
        for word in self.wasesa:
            self.word_types[word] = 'WASESA'
        
        for word in self.lesan:
            self.word_types[word] = 'LESAN'

    def get_word_type(self, word):
        """
        Mengembalikan tipe token berdasarkan kata yang diberikan.
        """
        wt = self.word_types.get(word.lower(), None)
        return wt

    def suggest_corrections(self, word, max_distance=2):
        """
        Memberikan saran koreksi untuk kata yang tidak dikenali.
        """
        suggestions = []
        word_lower = word.lower()

        for know_word in self.word_types.keys():
            
            distance = self._levenshtein_distance(word_lower, know_word)

            if distance <= max_distance:
                suggestions.append((know_word, distance))
        
        suggestions.sort(key=lambda x: x[1])
        return [word for word, distance in suggestions]

    def _levenshtein_distance(self, s1, s2):
        """
        Menghitung jarak Levenshtein antara dua string.
        """
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
        """
        Mengembalikan statistik kosakata.
        """
        return {
            'jejer': len(self.jejer),
            'wasesa': len(self.wasesa),
            'lesan': len(self.lesan),
            'total': len(self.word_types)
        }


if __name__ == "__main__":
    vocab = Vocabulary()
    vocab.get_vocabulary_stats()
    
    # Test beberapa kata (output di level INFO)
    test_words = ['aku', 'mangan', 'sego', 'ing', 'python']
    for word in test_words:
        word_type = vocab.get_word_type(word)
        if word_type:
            print(f"'{word}' -> {word_type}")
        else:
            suggestions = vocab.suggest_corrections(word)
            print(f"'{word}' tidak dikenal. Saran: {suggestions}")
