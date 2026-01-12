import logging
from models.tokens import Token
from data.vocabulary import Vocabulary
from colorama import Fore, Style

logger = logging.getLogger(__name__)

class Tokenizer:
    def __init__(self):
        self.vocab = Vocabulary()
        print(Fore.GREEN + "[TOKENIZER] Tokenizer dengan normalisasi kepemilikan siap")
        
        # Mapping untuk FSA
        self.token_map = {
            'JEJER': 'JEJER',
            'WASESA_TRANS': 'WASESA_TRANS',
            'WASESA_INTRANS': 'WASESA_INTRANS', 
            'KS': 'KS',
            'KW': 'KW',
            'LESAN': 'LESAN',
            'KETRANGAN': 'KETRANGAN',
            'KONJ': 'KONJ'
        }
        
        # Warna untuk setiap tipe token
        self.token_colors = {
            'JEJER': Fore.CYAN,
            'WASESA_TRANS': Fore.RED,
            'WASESA_INTRANS': Fore.YELLOW,
            'LESAN': Fore.GREEN,
            'KS': Fore.MAGENTA,
            'KW': Fore.LIGHTYELLOW_EX,
            'KONJ': Fore.LIGHTBLACK_EX,
            'KETRANGAN': Fore.LIGHTCYAN_EX,
            'UNKNOWN': Fore.LIGHTRED_EX
        }

    def tokenize(self, text):
        """
        Melakukan tokenisasi pada teks input dengan normalisasi.
        """
        print(Fore.WHITE + f"\n[TOKENIZER] Tokenisasi: '{text}'")
        
        tokens = []
        words = text.lower().split()
        
        for i, word in enumerate(words):
            # Dapatkan informasi kepemilikan
            poss_info = self.vocab.get_possessive_info(word)
            word_type = self.vocab.get_word_type(word)
            
            if word_type:
                # Map ke tipe yang sesuai dengan FSA
                mapped_type = self.token_map.get(word_type, word_type)
                
                # Buat token dengan informasi tambahan
                token_data = {
                    'word': word,
                    'type': mapped_type,
                    'original_type': word_type,
                    'position': i,
                    'possessive': poss_info['is_possessive'],
                    'normalized': poss_info['normalized']
                }
                
                if poss_info['is_possessive']:
                    token_data['possessive_marker'] = poss_info['marker']
                
                tokens.append(token_data)
                
                # Tampilkan dengan warna yang sesuai
                color = self.token_colors.get(word_type, Fore.WHITE)
                display_text = f"{word_type}: '{word}'"
                if poss_info['is_possessive']:
                    display_text += f" (kepemilikan: {poss_info['marker']})"
                print(f"  {color}{display_text}{Style.RESET_ALL}")
            else:
                # Kata tidak dikenal
                suggestions = self.vocab.suggest_corrections(word)
                token_data = {
                    'word': word,
                    'type': 'UNKNOWN',
                    'original_type': 'UNKNOWN',
                    'position': i,
                    'possessive': False,
                    'suggestions': suggestions
                }
                tokens.append(token_data)
                print(f"  {Fore.LIGHTRED_EX}UNKNOWN: '{word}'{Style.RESET_ALL}")
                if suggestions:
                    print(f"    {Fore.LIGHTYELLOW_EX}Saran: {', '.join(suggestions)}{Style.RESET_ALL}")
        
        print(Fore.WHITE + f"[TOKENIZER] Total token: {len(tokens)}")
        return tokens
    
    def validate_tokens(self, tokens_list):
        """
        Memvalidasi urutan token.
        """
        valid_tokens = []
        errors = []
        
        for token in tokens_list:
            if token.get('type') == 'UNKNOWN':
                error_msg = f"Kata tidak dikenal: '{token.get('word')}'"
                suggestions = token.get('suggestions', [])
                if suggestions:
                    error_msg += f" (saran: {', '.join(suggestions[:3])})"
                errors.append(error_msg)
            else:
                valid_tokens.append(token)
        
        if errors:
            print(Fore.YELLOW + f"[TOKENIZER] {len(errors)} error ditemukan")
        else:
            print(Fore.GREEN + f"[TOKENIZER] Semua token valid")
        
        return valid_tokens, errors

    def get_token_sequence(self, tokens_list):
        """Mengembalikan urutan tipe token"""
        sequence = [t.get('type') for t in tokens_list]
        print(Fore.WHITE + f"[TOKENIZER] Sequence: {sequence}")
        return sequence
    
    def print_token_summary(self, tokens_list):
        """Mencetak ringkasan token dengan informasi kepemilikan"""
        print(Fore.WHITE + "\n[TOKENIZER] Ringkasan Token:")
        
        type_counts = {}
        possessive_count = 0
        
        for token in tokens_list:
            token_type = token.get('type')
            type_counts[token_type] = type_counts.get(token_type, 0) + 1
            
            if token.get('possessive'):
                possessive_count += 1
        
        for token_type, count in type_counts.items():
            color = self.token_colors.get(token_type, Fore.WHITE)
            print(f"  {color}{token_type}: {count} token{Style.RESET_ALL}")
        
        if possessive_count > 0:
            print(f"  {Fore.LIGHTCYAN_EX}Kata kepemilikan: {possessive_count} token{Style.RESET_ALL}")