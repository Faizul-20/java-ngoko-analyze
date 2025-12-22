import re
from data.vocabulary import Vocabulary

class RegexValidator:

    def __init__(self):
        
        self.patterns = self._compile_patterns()

        self.sentence_pattern = re.compile(
            r'^\s*({jejer})\s+({wasesa})\s+({lesan})\s*$'.format(
                    jejer='|'.join(self.patterns['JEJER']),
                    wasesa='|'.join(self.patterns['WASESA']),
                    lesan='|'.join(self.patterns['LESAN'])
                )
        )
        
    def _compile_patterns(self):
        vocab = Vocabulary()
        patterns = {
            'JEJER': vocab.jejer,
            'WASESA': vocab.wasesa,
            'LESAN': vocab.lesan
        }
        return patterns    

