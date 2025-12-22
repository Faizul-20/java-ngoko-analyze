
import re

class Patterns:

    def __init__(self):

        from .vocabulary import Vocabulary
        vocab = Vocabulary()
        self.base_patterns = {
            'JEJER': r'\b(' + '|'.join(vocab.jejer) + r')\b',
            'WASESA': r'\b(' + '|'.join(vocab.wasesa) + r')\b',
            'LESAN': r'\b(' + '|'.join(vocab.lesan) + r')\b',
        }

        self.sentence_pattern = self._build_sentence_pattern()

    def _build_sentence_pattern(self):
            """
            Membangun pola regex untuk kalimat lengkap berdasarkan urutan token.
            """
            jejer_pattern = self.base_patterns['JEJER'][3:-2]
            wasesa_pattern = self.base_patterns['WASESA'][3:-2]
            lesan_pattern = self.base_patterns['LESAN'][3:-2]

            return[
                # Pola untuk kalimat lengkap: JEJER WASESA LESAN
                re.compile(rf'^\s*{jejer_pattern}\s+{wasesa_pattern}\s+{lesan_pattern}\s*$', re.IGNORECASE)
            ]
        
    def get_pattern_description(self):
            """
            Mengembalikan deskripsi pola yang digunakan.
            """
            description ={
                1: "Kalimat lengkap: JEJER WASESA LESAN"
            }
            return description