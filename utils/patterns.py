import re


class Patterns:
    def __init__(self):
        from data.vocabulary import Vocabulary
        vocab = Vocabulary()
        
        self.patterns = {
            # Pola 1: Wasesa Penggawe (Verbal)
            1: re.compile(r'^KB\s+(V_INTRANS|V_TRANS\s+KB)(\s+KET)?$'),
            
            # Pola 2: Wasesa Kahanan (Adjektival)
            2: re.compile(r'^KB\s+KS(\s+(banget|tenan))?(\s+KET)?$'),
            
            # Pola 3: Wasesa Wilangan (Numeral)
            3: re.compile(r'^KB\s+KW(\s+KET)?$'),
            
            # Pola 4: Wasesa Aran (Nominal)
            4: re.compile(r'^KB\s+KB(\s+KET)?$'),
            
            # Pola 5: Ukara Camboran (Compound)
            5: re.compile(r'^(.+)\s+KONJ\s+(.+)$')
        }

    def match_pattern(self, token_sequence_str):
        for pattern_num, pattern in self.patterns.items():
            if pattern.match(token_sequence_str):
                return pattern_num
        return None

    def get_pattern_description(self):
        return {
            1: "Wasesa Penggawe (Verbal): KB + (V_INTRANS | V_TRANS + KB) + (KET?)",
            2: "Wasesa Kahanan (Adjektival): KB + KS + (banget|tenan?) + (KET?)",
            3: "Wasesa Wilangan (Numeral): KB + KW + (KET?)",
            4: "Wasesa Aran (Nominal): KB + KB + (KET?)",
            5: "Ukara Camboran: (Kalimat) + KONJ + (Kalimat)"
        }