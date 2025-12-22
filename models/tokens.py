
class tokens:
    def __init__(self, word, token_type, suggestions=None):
        self.word = word
        self.token_type = token_type
        self.suggestions = suggestions or []
    
    def to_dict(self):
        """
        Mengembalikan representasi kamus dari token.
        """
        return {
            'word': self.word,
            'type': self.token_type,
            'suggestions': self.suggestions
        }
    
    def __str__(self):
        return f"Token(word={self.word}, type={self.token_type}"
        
    def __repr__(self):
        return self.__str__()