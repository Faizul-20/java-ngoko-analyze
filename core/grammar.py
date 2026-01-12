from models.grammar_rules import ProductionRules
from colorama import Fore, Style

class Grammar:
    def __init__(self):
        self.rules = ProductionRules()
        self.start_symbol = "S"  # Sesuai laporan: S = Ukara/Kalimat
        
        print(Fore.CYAN + "\n[GRAMMAR] Context-Free Grammar untuk Bahasa Jawa Ngoko")
        print(Fore.WHITE + "-"*50)
        print(Fore.YELLOW + "Start Symbol: S (Ukara/Kalimat)")
        print(Fore.WHITE + f"Non-terminals: {list(self.rules.productions.keys())}")
        
        # Print aturan produksi utama
        print(Fore.CYAN + "\nAturan Produksi Utama:")
        for nt, prods in self.rules.productions.items():
            if nt == "S":  # Hanya tampilkan aturan untuk S
                for prod in prods:
                    print(Fore.WHITE + f"  S → {' '.join(prod)}")
        print(Fore.WHITE + "-"*50)

    def get_production_for(self, non_terminal):
        """
        Mengembalikan produksi untuk non-terminal yang diberikan.
        """
        return self.rules.get_productions_for(non_terminal)
    
    def is_terminal(self, symbol):
        """
        Memeriksa apakah simbol adalah terminal.
        """
        return self.rules.is_terminal(symbol)
    
    def is_non_terminal(self, symbol):
        """
        Memeriksa apakah simbol adalah non-terminal.
        """
        return self.rules.is_non_terminal(symbol)

    def get_first_set(self, symbol):
        """
        Mengembalikan himpunan FIRST untuk simbol yang diberikan.
        """
        if self.is_terminal(symbol):
            return {symbol}
        
        first_set = set()
        visited = set()
        
        def _get_first(sym):
            if sym in visited:
                return set()
            visited.add(sym)
            
            if self.is_terminal(sym):
                return {sym}
            
            productions = self.get_production_for(sym)
            for production in productions:
                if not production:  # epsilon production
                    first_set.add('ε')
                else:
                    first_symbol = production[0]
                    if first_symbol == sym:  # hindari rekursi kiri langsung
                        continue
                    first_set.update(_get_first(first_symbol))
            return first_set
        
        return _get_first(symbol)

    def get_follow_set(self, symbol):
        """
        Mengembalikan himpunan FOLLOW untuk simbol yang diberikan.
        Implementasi sederhana untuk Bahasa Jawa Ngoko.
        """
        follow_set = {
            "S": {'$'},
            "VP": {'$', 'NP', 'CONJ'},
            "NP": {'V_INTRANS', 'V_TRANS', 'ADJ', 'NUM', 'CONJ', '$'},
            "ADJP": {'$', 'CONJ'},
            "NUMP": {'$', 'CONJ'},
            "PP": {'$', 'CONJ'}
        }
        return follow_set.get(symbol, set())
    
    def validate_grammar(self):
        """
        Validasi grammar untuk memeriksa masalah seperti rekursi kiri.
        """
        issues = []
        for non_terminal in self.rules.productions:
            for production in self.rules.productions[non_terminal]:
                if production and production[0] == non_terminal:
                    issues.append(f"Rekursi kiri di: {non_terminal} → {' '.join(production)}")
        return issues
    
    def parse_sentence(self, tokens):
        """
        Parsing sederhana menggunakan pendekatan recursive descent.
        """
        token_types = [t['type'] for t in tokens]
        return self._parse_from_start(self.start_symbol, token_types, 0)
    
    def _parse_from_start(self, symbol, tokens, index):
        """
        Parsing recursive untuk simbol tertentu.
        """
        if index >= len(tokens):
            return None, index
        
        if self.is_terminal(symbol):
            # Cek apakah token saat ini cocok dengan terminal
            if tokens[index] == symbol:
                return {'type': symbol, 'value': tokens[index]}, index + 1
            return None, index
        
        # Coba semua produksi untuk non-terminal
        productions = self.get_production_for(symbol)
        for production in productions:
            current_index = index
            children = []
            valid = True
            
            for sub_symbol in production:
                result, new_index = self._parse_from_start(sub_symbol, tokens, current_index)
                if result is None:
                    valid = False
                    break
                children.append(result)
                current_index = new_index
            
            if valid:
                return {'type': symbol, 'children': children}, current_index
        
        return None, index