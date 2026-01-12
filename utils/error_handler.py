class ErrorHandler:
    def __init__(self):
        self.error_messages = {
            'UNKNOWN_TOKEN': "Kata '{word}' tidak dikenal.",
            'INVALID_SEQUENCE': "Urutan token tidak valid.",
            'EMPTY_INPUT': "Input teks kosong.",
            'MISSING_COMPONENT': "Komponen '{component}' tidak ditemukan.",
            'PARSE_ERROR': "Kesalahan parsing: {details}",
            'FSA_ERROR': "Kesalahan FSA: State '{state}' tidak memiliki transisi untuk '{input}'.",
            'GRAMMAR_VIOLATION': "Pelanggaran grammar: {details}",
            'TOKENIZATION_ERROR': "Kesalahan tokenisasi."
        }

    def handler_error(self, error_type, **kwargs):
        error_type = error_type.upper()
        
        if error_type == 'UNKNOWN_TOKEN':
            return f"Kata '{kwargs.get('word')}' tidak dikenal dalam kosakata Jawa Ngoko."
        
        elif error_type == 'INVALID_SEQUENCE':
            return "Urutan kata tidak sesuai dengan struktur kalimat Bahasa Jawa Ngoko."
        
        elif error_type == 'FSA_ERROR':
            state = kwargs.get('state', 'unknown')
            input_symbol = kwargs.get('input', 'unknown')
            return f"FSA error: State '{state}' tidak dapat memproses input '{input_symbol}'."
        
        elif error_type == 'GRAMMAR_VIOLATION':
            details = kwargs.get('details', 'Struktur kalimat tidak valid')
            return f"Pelanggaran aturan grammar: {details}"
        
        elif error_type == 'TOKENIZATION_ERROR':
            context = kwargs.get('context', '')
            return f"Kesalahan saat memproses kata dalam: '{context}'"
        
        else:
            return f"Error: {error_type}"