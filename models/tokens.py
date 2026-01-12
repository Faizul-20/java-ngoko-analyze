class Token:
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
        suggestions_str = f", suggestions={self.suggestions}" if self.suggestions else ""
        return f"Token(word='{self.word}', type='{self.token_type}'{suggestions_str})"
        
    def __repr__(self):
        return self.__str__()
    
    def is_valid(self):
        """Cek apakah token valid (bukan UNKNOWN)"""
        return self.token_type != 'UNKNOWN'
    
    def get_detailed_info(self):
        """Dapatkan informasi detail token"""
        token_types_info = {
            'JEJER': {'role': 'Subjek', 'description': 'Pelaku atau subjek kalimat'},
            'WASESA_TRANS': {'role': 'Predikat', 'description': 'Kata kerja transitif (butuh objek)'},
            'WASESA_INTRANS': {'role': 'Predikat', 'description': 'Kata kerja intransitif'},
            'KS': {'role': 'Predikat', 'description': 'Kata sifat (Wasesa Kahanan)'},
            'KW': {'role': 'Predikat', 'description': 'Kata bilangan (Wasesa Wilangan)'},
            'LESAN': {'role': 'Objek', 'description': 'Penerima aksi'},
            'KONJ': {'role': 'Penghubung', 'description': 'Menghubungkan klausa'},
            'KETRANGAN': {'role': 'Keterangan', 'description': 'Menjelaskan waktu/tempat/cara'},
            'UNKNOWN': {'role': 'Tidak Dikenal', 'description': 'Kata tidak dikenal dalam kosakata'}
        }
        
        info = token_types_info.get(self.token_type, {'role': 'Unknown', 'description': 'Tidak diketahui'})
        return {
            'word': self.word,
            'type': self.token_type,
            'role': info['role'],
            'description': info['description'],
            'is_valid': self.is_valid(),
            'has_suggestions': len(self.suggestions) > 0
        }