
class ErrorHandler:

    def __init__(self):
        self.error_messages = {
            'UkNOWN_TOKEN':"Kata {word} tidak dikenal ditemukan.",
            'INVALID_SEQUENCE':"Urutan token tidak valid.",
            'EMPTY_INPUT':"Input teks kosong.",
            'MISSING_COMPONENT':"Komponen yang dibutuhkan hilang dalam input komponen yang di butuhkan {component}.",
            'PARSE_ERROR':"Terjadi kesalahan saat parsing.",
            'FSA_ERROR':"Terjadi kesalahan pada Finite State Automata.{details}",
            'GRAMMAR_VIOLATION':"Pelanggaran aturan tata bahasa terdeteksi.{details}",
            'TOKENIZATION_ERROR':"Terjadi kesalahan selama tokenisasi. Error: {error} Karena: {context}"
        }

    def handler_error(self,error, context=None):
        """
        Mengembalikan pesan error berdasarkan kode error yang diberikan.
        """
        if isinstance(error, Exception):
            error_type = str(error)
        else:
            error_type = error
            
        error_type = error_type.upper()

        if "UKNOWN_TOKEN" in error_type:
            return self._suggestions_for_unknown_token()
        elif "INVALID_SEQUENCE" in error_type:
            return self._suggestions_for_invalid_sequence()
        elif "EMPTY_INPUT" in error_type:
            return self._suggestions_for_empty_input()
        elif "MISSING_COMPONENT" in error_type:
            return self._suggestions_for_missing_component(context)
        elif "PARSE_ERROR" in error_type:
            return self.error_messages['PARSE_ERROR']
        elif "FSA_ERROR" in error_type:
            details = f" Detail: {str(error)}" if context is None else f" Detail: {context}"
            return self.error_messages['FSA_ERROR'].format(details=details)
        elif "GRAMMAR_VIOLATION" in error_type:
            details = f" Detail: {str(error)}" if context is None else f" Detail: {context}"
            return self.error_messages['GRAMMAR_VIOLATION'].format(details=details)
        elif "TOKENIZATION_ERROR" in str(error):
            return self.error_messages['TOKENIZATION_ERROR'].format(error=str(error), context=context)
        else:
            return f"Terjadi kesalahan tak terduga: {str(error)}"
        

    def _suggestions_for_unknown_token(self):
        print("1. Pastikan kata menggunakan ejaan Bahasa Jawa Ngoko yang benar")
        print("2. Gunakan kamus dasar: aku, mangan, sego, buku, dll.")
        print("3. Hindari kata serapan dari bahasa Indonesia/asing")

    def _suggestions_for_invalid_sequence(self):
        print("1. Periksa urutan kata sesuai struktur kalimat Bahasa Jawa Ngoko")
        print("2. Gunakan pola kalimat sederhana: Subjek - Predikat - Objek")
        print("3. Hindari penggunaan kata yang tidak sesuai konteks")
    
    def _suggestions_for_missing_component(self, component):
        print(f"1. Pastikan komponen '{component}' ada dalam kalimat")
        print("2. Gunakan pola kalimat lengkap: Subjek - Predikat - Objek")
        print("3. Periksa kembali kosakata yang digunakan")
        