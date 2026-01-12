# [file name]: grammar_rules.py (UPDATED - tambah aturan untuk FSA lengkap)
from data.jejer_list import JEJER_VOCAB
from data.wasesa_list import WASESA_TRANSITIVE, WASESA_INTRANSITIVE
from data.lesan_list import LESAN_VOCAB
from data.ks_list import KS_VOCAB
from data.kw_list import KW_VOCAB
from data.konj_list import KONJ_VOCAB
from data.ket_list import KET_VOCAB

class ProductionRules:
    def __init__(self):
        # Terminals (kata-kata aktual dalam Bahasa Jawa)
        self.terminals = {
            # Noun Phrase (Jejer dan Lesan) - digabung karena dalam FSA sama-sama NP
            "NP": list(set(JEJER_VOCAB + LESAN_VOCAB + [
                'guru', 'murid', 'siswa', 'dokter', 'perawat',
                'pedagang', 'petani', 'nelayan', 'sopir', 'polisi',
                'bapak', 'ibu', 'adik', 'kakak', 'anak'
            ])),
            
            # Verbs - Kata Kerja
            "V_INTRANS": WASESA_INTRANSITIVE,  # Kata kerja intransitif
            "V_TRANS": WASESA_TRANSITIVE,      # Kata kerja transitif
            
            # Adjectives - Kata Sifat
            "ADJ": list(set(KS_VOCAB + [
                'banget', 'tenan', 'pisan', 'temenan', 'sanget',
                'luwih', 'kurang', 'sithik', 'akeh', 'apik',
                'enak', 'cepat', 'lambat', 'gedhe', 'cilik'
            ])),
            
            # Numerals - Kata Bilangan  
            "NUM": KW_VOCAB,
            
            # Conjunctions - Kata Sambung
            "CONJ": KONJ_VOCAB,
            
            # Prepositions - Kata Keterangan
            "PREP": KET_VOCAB,
            
            # Geganep (Pelengkap) - tambahan untuk transitif
            "GEGANEP": list(set(LESAN_VOCAB + [
                'karo', 'kali', 'marang', 'kanggo', 'untuk'
            ]))
        }

        # Context-Free Grammar untuk Bahasa Jawa Ngoko
        # Diperbarui untuk mendukung FSA lengkap
        self.productions = {
            # =============================================
            # A. LEVEL KALIMAT (UKARA) - SESUAI FSA
            # =============================================
            "S": [  # Sentence (Ukara)
                # 1. POLA DASAR (q0 → q1 → q2)
                ["NP", "V_INTRANS"],                      # Adhik turu (q2)
                ["NP", "ADJ"],                            # Omahku gedhe (q2)
                ["NP", "NUM"],                            # Sapine lima (q2)
                ["NP", "NP"],                             # Bapakku guru (q2)
                
                # 2. POLA DENGAN KETERANGAN AWAL (q0 → q4 → ...)
                ["PREP", "NP", "V_INTRANS"],              # Ing kamar adhik turu
                ["PREP", "NP", "ADJ"],                    # Ing omah gedhe
                ["PREP", "NP", "NUM"],                    # Ing kandang sapine lima
                ["PREP", "NP", "NP"],                     # Ing sekolah bapakku guru
                
                # 3. POLA TRANSITIF (q0 → q1 → q3 → q5)
                ["NP", "V_TRANS", "NP"],                  # Aku mangan sego (q5)
                
                # 4. POLA TRANSITIF DENGAN KETERANGAN AWAL
                ["PREP", "NP", "V_TRANS", "NP"],          # Wingi aku mangan sego
                
                # 5. POLA DENGAN PELENGKAP (q0 → q1 → q3 → q5 → q6)
                ["NP", "V_TRANS", "NP", "GEGANEP"],       # Aku mènèhi buku marang adhik
                
                # 6. POLA DENGAN KETERANGAN TAMBAHAN (→ q11 → q12)
                ["NP", "V_INTRANS", "PREP"],              # Adhik turu ing kamar
                ["NP", "ADJ", "ADJ"],                     # Omahku gedhe banget
                ["NP", "ADJ", "PREP"],                    # Omahku gedhe ing desa
                ["NP", "NUM", "PREP"],                    # Sapine lima ing kandang
                ["NP", "NP", "PREP"],                     # Bapakku guru ing sekolah
                ["NP", "V_TRANS", "NP", "PREP"],          # Aku mangan sego wingi
                ["NP", "V_TRANS", "NP", "ADJ"],           # Aku mangan sego enak
                ["NP", "V_TRANS", "NP", "GEGANEP", "PREP"], # Aku mènèhi buku marang adhik wingi
                
                # 7. POLA KETERANGAN BERANTAI (→ q11 → q12)
                ["NP", "V_INTRANS", "PREP", "PREP"],      # Adhik turu ing kamar wingi
                ["NP", "ADJ", "ADJ", "PREP"],             # Omahku gedhe banget ing desa
                
                # 8. KALIMAT MAJEMUK (dengan KONJ kembali ke q0)
                ["S", "CONJ", "S"],                       # Aku nulis lan adik maca
                
                # 9. VARIASI LAIN (untuk error handling)
                ["NP", "V_TRANS"],                        # Transitif tanpa objek
                ["V_TRANS", "NP"],                        # Tanpa subjek
                ["PREP", "NP"],                           # Hanya keterangan + NP
                ["ADJ"],                                  # Hanya kata sifat
                ["NUM"],                                  # Hanya bilangan
            ],
            
            # =============================================
            # B. LEVEL FRASA (untuk parsing detail)
            # =============================================
            "VP": [  # Verb Phrase
                ["V_INTRANS"],
                ["V_TRANS", "NP"],
                ["V_TRANS", "NP", "GEGANEP"],
                ["V_INTRANS", "PP"],
                ["V_TRANS", "NP", "PP"],
                ["V_TRANS", "NP", "ADJP"],
            ],
            
            "NP": [  # Noun Phrase
                ["NP"],
                ["NP", "ADJ"],      # NP dengan keterangan sifat
                ["NP", "PP"],       # NP dengan keterangan tempat/waktu
                ["PREP", "NP"],     # Keterangan + NP
            ],
            
            "ADJP": [  # Adjective Phrase
                ["ADJ"],
                ["ADJ", "ADJ"],     # Penguat
                ["ADJ", "PP"],      # ADJ + keterangan
            ],
            
            "NUMP": [  # Numeral Phrase
                ["NUM"],
                ["NUM", "NUM"],     # Bilangan kompleks
                ["NUM", "PP"],      # NUM + keterangan
            ],
            
            "PP": [  # Prepositional Phrase
                ["PREP", "NP"],
                ["PREP", "ADJP"],
                ["PREP", "NUMP"],
                ["PREP", "VP"],
            ],
            
            "GP": [  # Geganep Phrase (Pelengkap)
                ["GEGANEP", "NP"],
                ["GEGANEP", "PP"],
            ]
        }
        
        # Simbol awal grammar
        self.start_symbol = "S"
        
        # Non-terminals
        self.non_terminals = list(self.productions.keys())
        
        # Semua simbol
        self.all_symbols = set(self.non_terminals)
        for terminals in self.terminals.values():
            self.all_symbols.update(terminals)
    
    # [METHODS YANG SAMA SEPERTI SEBELUMNYA...]
    # get_all_terminals, get_word_type, is_terminal, is_non_terminal,
    # get_productions_for, get_first_set, get_follow_set, 
    # get_rule_description, validate_grammar, print_grammar_summary,
    # find_production_by_pattern
    
    def get_fsa_compatible_productions(self, state):
        """
        Mendapatkan produksi yang kompatibel dengan state FSA tertentu.
        """
        state_to_productions = {
            "q0": [["NP"], ["PREP", "NP"]],
            "q1": [["V_INTRANS"], ["V_TRANS"], ["ADJ"], ["NUM"], ["NP"]],
            "q2": [[], ["PREP"], ["ADJ"], ["NUM"], ["CONJ", "S"]],
            "q3": [["NP"], ["PREP", "NP"]],
            "q4": [["V_INTRANS"], ["V_TRANS"], ["ADJ"], ["NUM"], ["NP"]],
            "q5": [[], ["GEGANEP", "NP"], ["PREP"], ["ADJ"], ["CONJ", "S"]],
            "q6": [[], ["PREP"], ["ADJ"], ["CONJ", "S"]],
            "q11": [[], ["PREP"], ["ADJ"], ["NUM"], ["CONJ", "S"]],
            "q12": [[], ["CONJ", "S"]]
        }
        
        return state_to_productions.get(state, [])
    
    def get_pattern_for_state(self, state):
        """
        Mendapatkan pola kalimat berdasarkan state FSA akhir.
        """
        patterns = {
            "q2": [
                ("NP V_INTRANS", "Wasesa Penggawe Intransitif"),
                ("NP ADJ", "Wasesa Kahanan"),
                ("NP NUM", "Wasesa Wilangan"),
                ("NP NP", "Wasesa Aran"),
            ],
            "q5": [
                ("NP V_TRANS NP", "Wasesa Penggawe Transitif"),
            ],
            "q6": [
                ("NP V_TRANS NP GEGANEP", "Transitif dengan Pelengkap"),
            ],
            "q11": [
                ("NP V_INTRANS PREP", "Intransitif + Keterangan"),
                ("NP ADJ ADJ", "Adjektival dengan Penguat"),
                ("NP ADJ PREP", "Adjektival + Keterangan"),
            ],
            "q12": [
                ("NP V_INTRANS PREP PREP", "Intransitif + Keterangan Berganda"),
                ("NP ADJ ADJ PREP", "Adjektival dengan Penguat + Keterangan"),
            ]
        }
        
        return patterns.get(state, [])
