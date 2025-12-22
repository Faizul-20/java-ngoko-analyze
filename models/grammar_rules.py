
from data.jejer_list import JEJER_VOCAB
from data.wasesa_list import WASESA_VOCAB
from data.lesan_list import LESAN_VOCAB

class ProductionRules:
    def __init__(self):
        
        self.terminals = {
            "JEJER": JEJER_VOCAB,
            "WASESA": WASESA_VOCAB,
            "LESAN": LESAN_VOCAB
        }

        self.productions = {
           "KALIMAT": [
                ['JEJER', 'WASESA', 'LESAN'],# S-P-O
                ['JEJER', 'WASESA'] # S-P
              ]
       }

    def get_all_terminals(self):
        """
        mengambil semua terminal yang ada dalam aturan produksi
        """
        all_terminals = set()

        for category in self.terminals.values():
           all_terminals.update(category)
        return all_terminals
    
    def get_word_type(self, word):
        """
        Mengembalikan tipe token berdasarkan kata yang diberikan.
        """
        for token_type, words in self.terminals.items():
            if word in words:
                return token_type
            
        return None
                