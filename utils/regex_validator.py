import re
from data.vocabulary import Vocabulary

class RegexValidator:
    def __init__(self):
        self.vocab = Vocabulary()
        self.patterns = self._compile_patterns()

    def _compile_patterns(self):
        # Escape semua kata untuk regex
        def escape_words(words):
            return [re.escape(word) for word in words]
        
        return {
            'KB': '|'.join(escape_words(self.vocab.jejer + self.vocab.lesan)),
            'V_INTRANS': '|'.join(escape_words([w for w in self.vocab.wasesa if 'turu' in w or 'mlaku' in w])),
            'V_TRANS': '|'.join(escape_words([w for w in self.vocab.wasesa if 'mangan' in w or 'tuku' in w])),
            'KS': '|'.join(escape_words(self.vocab.ks)),
            'KW': '|'.join(escape_words(self.vocab.kw)),
            'KONJ': '|'.join(escape_words(self.vocab.konj)),
            'KET': '|'.join(escape_words(self.vocab.ket))
        }

    def validate_sentence_structure(self, sentence):
        # Validasi pola sederhana
        words = sentence.lower().split()
        
        if len(words) < 2:
            return False
            
        # Cek apakah kata pertama adalah Jejer
        if words[0] not in self.vocab.jejer:
            return False
            
        return True