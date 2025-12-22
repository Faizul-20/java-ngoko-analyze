
import logging
from models.tokens import tokens as Token
from data.vocabulary import Vocabulary

logger = logging.getLogger(__name__)

class Tokenizer:

    def __init__(self):
        # Buat instance Vocabulary (jangan hanya merujuk ke class)
        self.vocab = Vocabulary()

    def tokenize(self, text):
        """
        Melakukan tokenisasi pada teks input berdasarkan kosakata yang ada.
        Mengembalikan daftar token sebagai kamus: {'word', 'type', 'suggestions'}
        """

        token_list = []
        words = text.lower().split()
        logger.debug("Tokenize input: %s", words)

        for word in words:
            word_type = self.vocab.get_word_type(word)
            logger.debug("Hasil tipe untuk '%s': %s", word, word_type)

            if word_type:
                token_list.append(Token(word, word_type).to_dict())
            else:
                # Coba untuk saran koreksi jika kata tidak dikenali
                suggestions = self.vocab.suggest_corrections(word)
                token_list.append(Token(word, 'UNKNOWN', suggestions).to_dict())

        return token_list
    
    def validate_tokens(self, tokens_list):
        """
        Memvalidasi urutan token berdasarkan kosakata yang ada.
        Mengembalikan tuple: (valid_tokens, errors)
        """
        valid_tokens = []
        errors = []

        for token in tokens_list:
            # Token sekarang direpresentasikan sebagai kamus/dict
            if token.get('type') == 'UNKNOWN':
                errors.append(f"Kata tidak dikenal: '{token.get('word')}'")
                if token.get('suggestions'):
                    errors.append(f"  Mungkin maksud: {', '.join(token.get('suggestions')[:3])}")
            else:
                valid_tokens.append(token)
        
        return valid_tokens, errors

    def get_token_sequence(self, tokens_list):
        """Mengembalikan urutan tipe token seperti ['JEJER','WASESA',...]"""
        return [t.get('type') for t in tokens_list]