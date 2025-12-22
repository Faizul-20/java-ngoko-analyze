import re
from data.vocabulary import Vocabulary

class RegexValidator:

    def __init__(self):
        self.patterns = self._compile_patterns()
        # membangun pola regex untuk kalimat lengkap berdasarkan urutan token.
        self.sentence_pattern = re.compile(
            r'^\s*({jejer})\s+({wasesa})\s+({lesan})\s*$'.format(
                jejer='|'.join(self.patterns['JEJER']),
                wasesa='|'.join(self.patterns['WASESA']),
                lesan='|'.join(self.patterns['LESAN'])
            ),
            flags=re.IGNORECASE
        )

    def _token_to_pattern(self, token):
       # pisahkan token menjadi bagian-bagian (untuk multi-kata)
        parts = token.strip().split()
        escaped_parts = [re.escape(p) for p in parts]
        return r"\s+".join(escaped_parts)

    def _compile_patterns(self):
        """
        Mengompilasi pola regex untuk setiap kategori token berdasarkan kosakata.
        """
        vocab = Vocabulary()
        raw = {
            'JEJER': vocab.jejer,
            'WASESA': vocab.wasesa,
            'LESAN': vocab.lesan
        }

        compiled = {}
        for k, items in raw.items():
            patterns = [self._token_to_pattern(item) for item in items]
            # Urutkan pola berdasarkan panjang (dari yang terpanjang ke terpendek)
            patterns.sort(key=lambda x: -len(x))
            compiled[k] = patterns
        return compiled

    def validate_sentence_structure(self, sentence):
        """
        Memvalidasi struktur kalimat menggunakan pola regex.
        Mengembalikan True jika sesuai pola, False jika tidak.
        """
        if not sentence or not sentence.strip():
            return False

        # Normalisasi spasi
        normalized = re.sub(r"\s+", " ", sentence.strip())
        match = self.sentence_pattern.match(normalized)
        return match is not None

