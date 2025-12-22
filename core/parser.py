

class Parser:
    def __init__(self,grammar):
        self.grammar = grammar

    def _build_parse_table(self):
        
        table = {}

        for non_terminal in self.grammar.rules:
            table[non_terminal] = {}
            productions = self.grammar.get_production_for(non_terminal)
            for production in productions:
                first_set = self.grammar.get_first_set(production[0])
                for terminal in first_set:
                    table[non_terminal][terminal] = production
                if 'ε' in first_set:
                    follow_set = self.grammar.get_follow_set(non_terminal)
                    for terminal in follow_set:
                        table[non_terminal][terminal] = production
        return table
    
    def _get_production_first(self, production):
        
        if not production :
            return {'ε'}
        
        first_set = set()

        for symbol in production:
            symbol_first = self.grammar.get_first_set(symbol)
            first_set.update(symbol_first - {'ε'})

            if 'ε' not in symbol_first:
                break
        else:
            first_set.add('ε')

        return first_set
    
    def parse(self, input_tokens):
        """
        Parser sederhana yang mencocokkan urutan token terhadap produksi di grammar.
        Mengembalikan tuple: (is_valid, parse_tree, parse_steps, grammar_rules_used, errors)
        """
        # Ekstrak sequence tipe token
        token_types = [t['type'] for t in input_tokens]

        start = self.grammar.start_symbol
        productions = self.grammar.get_production_for(start)

        # Cek apakah token_types cocok salah satu produksi
        for production in productions:
            if token_types == production:
                # Valid: bangun representasi parse sederhana
                parse_tree = {start: production}
                parse_steps = [f"Matched production: {start} -> {' '.join(production)}"]
                grammar_rules = [f"{start} -> {' '.join(production)}"]
                return True, parse_tree, parse_steps, grammar_rules, []

        # Jika tidak cocok, coba apakah produksi pemangkasan (mis. tanpa LESAN)
        for production in productions:
            if len(token_types) == len(production) and token_types == production[:len(token_types)]:
                parse_tree = {start: token_types}
                parse_steps = [f"Partial match to production: {start} -> {' '.join(production)}"]
                grammar_rules = [f"{start} -> {' '.join(production)}"]
                return True, parse_tree, parse_steps, grammar_rules, []

        # Jika tidak cocok sama sekali, kembalikan error
        errors = [f"Parsing error: sequence {' '.join(token_types)} tidak cocok dengan grammar."]
        return False, None, [], [], errors