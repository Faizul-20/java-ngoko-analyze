
from models.grammar_rules import ProductionRules

class Grammar:
    def __init__(self):
        self.rules = ProductionRules()
        self.start_symbol = "KALIMAT"

    def get_production_for(self, non_terminal):
        """"
        Mengembalikan produksi untuk non-terminal yang diberikan.
        """
        return self.rules.productions.get(non_terminal, [])
    
    def is_terminal(self, symbol):
        """
        Memeriksa apakah simbol adalah terminal.
        """
        all_terminals = self.rules.get_all_terminals()
        return symbol in all_terminals
    
    def is_non_terminal(self, symbol):
        """
        Memeriksa apakah simbol adalah non-terminal.
        """
        return symbol in self.rules.productions

    def get_first_set(self, symbol):
        """
        Mengembalikan himpunan FIRST untuk simbol yang diberikan.
        """
        if self.is_terminal(symbol):
            return {symbol}
        first_set = set()
        productions = self.get_production_for(symbol)

        for production in productions:

            if not production: # epsilon production
                first_set.add('ε')
            else:
                first_symbol = production[0]
                if first_symbol == symbol: # hindari rekursi tak berhingga
                    continue
                first_set.update(self.get_first_set(first_symbol))
        return first_set

    def get_follow_set(self, symbol):
        """
        Mengembalikan himpunan FOLLOW untuk simbol yang diberikan.
        """
        follow_set = {
            "KALIMAT": {'$'},
            "JEJER": {"WASESA"},
            "WASESA": {"LESAN"},
            "LESAN": {'$'}
        }
        return follow_set.get(symbol, set())
    
    def validate_grammar(self):
        issued = []
        for non_terminal in self.rules.productions:
            for production in self.rules.productions[non_terminal]:
                if production and production[0] == non_terminal:
                    issued.append(f"Rekursi kri di : {non_terminal} -> {' '.join(production)}")
        return issued

