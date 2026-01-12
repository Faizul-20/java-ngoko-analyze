# [file name]: parser.py (UPDATED)
from colorama import Fore, Style

class Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        print(Fore.CYAN + "[PARSER] Parser CFG dengan FSA integration siap")
        
        # Mapping token ke simbol grammar
        self.token_to_symbol = {
            'JEJER': 'NP',
            'LESAN': 'NP',
            'WASESA_TRANS': 'V_TRANS',
            'WASESA_INTRANS': 'V_INTRANS',
            'KS': 'ADJ',
            'KW': 'NUM',
            'KONJ': 'CONJ',
            'KETRANGAN': 'PREP',
            'GEGANEP': 'GEGANEP',
            'UNKNOWN': 'UNKNOWN'
        }

    def parse(self, input_tokens, fsa_state=None):
        """
        Parsing dengan mempertimbangkan state FSA.
        """
        print(Fore.CYAN + f"\n[PARSER] Memulai parsing")
        if fsa_state:
            print(Fore.WHITE + f"[PARSER] State FSA: {fsa_state}")
        
        # Konversi token ke simbol grammar
        token_symbols = self._map_tokens_to_symbols(input_tokens)
        print(Fore.WHITE + f"[PARSER] Token symbols: {token_symbols}")
        
        # Cari pola yang cocok
        pattern = self._match_pattern(token_symbols, fsa_state)
        
        if pattern:
            print(Fore.GREEN + f"[PARSER] ✓ Pattern ditemukan: {pattern['description']}")
            
            parse_tree = self._build_parse_tree(pattern, input_tokens)
            grammar_rules = [f"S → {' '.join(pattern['production'])}"]
            parse_steps = [f"Pattern: {pattern['description']}"]
            
            return True, parse_tree, parse_steps, grammar_rules, []
        else:
            # Coba parsing dengan pendekatan lebih fleksibel
            return self._flexible_parse(token_symbols, input_tokens)
    
    def _map_tokens_to_symbols(self, tokens):
        """Map token types ke simbol grammar"""
        result = []
        for token in tokens:
            token_type = token.get('type')
            if token_type in self.token_to_symbol:
                result.append(self.token_to_symbol[token_type])
            else:
                result.append(token_type)
        return result
    
    def _match_pattern(self, token_symbols, fsa_state=None):
        """
        Mencocokkan pola berdasarkan simbol token dan state FSA.
        """
        patterns = []
        
        # Pola dasar (tanpa memperhatikan FSA state)
        base_patterns = self._get_base_patterns(token_symbols)
        patterns.extend(base_patterns)
        
        # Pola berdasarkan FSA state (jika diketahui)
        if fsa_state:
            state_patterns = self._get_state_specific_patterns(token_symbols, fsa_state)
            patterns.extend(state_patterns)
        
        # Return pattern pertama yang cocok
        return patterns[0] if patterns else None
    
    def _get_base_patterns(self, token_symbols):
        """Pola dasar untuk semua kalimat"""
        patterns = []
        
        # 1. Wasesa Penggawe Intransitif: NP V_INTRANS
        if len(token_symbols) >= 2 and token_symbols[0] == 'NP' and token_symbols[1] == 'V_INTRANS':
            patterns.append({
                'pattern': ['NP', 'V_INTRANS'],
                'production': ['NP', 'V_INTRANS'],
                'description': 'Wasesa Penggawe Intransitif (J-W)'
            })
        
        # 2. Wasesa Penggawe Transitif: NP V_TRANS NP
        if len(token_symbols) >= 3 and token_symbols[0] == 'NP' and token_symbols[1] == 'V_TRANS' and token_symbols[2] == 'NP':
            patterns.append({
                'pattern': ['NP', 'V_TRANS', 'NP'],
                'production': ['NP', 'V_TRANS', 'NP'],
                'description': 'Wasesa Penggawe Transitif (J-W-L)'
            })
        
        # 3. Wasesa Kahanan: NP ADJ
        if len(token_symbols) >= 2 and token_symbols[0] == 'NP' and token_symbols[1] == 'ADJ':
            patterns.append({
                'pattern': ['NP', 'ADJ'],
                'production': ['NP', 'ADJ'],
                'description': 'Wasesa Kahanan (J-KS)'
            })
        
        # 4. Wasesa Wilangan: NP NUM ✅
        if len(token_symbols) >= 2 and token_symbols[0] == 'NP' and token_symbols[1] == 'NUM':
            patterns.append({
                'pattern': ['NP', 'NUM'],
                'production': ['NP', 'NUM'],
                'description': 'Wasesa Wilangan (J-KW)'
            })
        
        # 5. Wasesa Aran: NP NP ✅
        if len(token_symbols) >= 2 and token_symbols[0] == 'NP' and token_symbols[1] == 'NP':
            patterns.append({
                'pattern': ['NP', 'NP'],
                'production': ['NP', 'NP'],
                'description': 'Wasesa Aran (J-J/L)'
            })
        
        # 6. Dengan Keterangan: ... PREP
        if len(token_symbols) >= 3 and token_symbols[-1] == 'PREP':
            # NP V_INTRANS PREP
            if token_symbols[0] == 'NP' and token_symbols[1] == 'V_INTRANS':
                patterns.append({
                    'pattern': ['NP', 'V_INTRANS', 'PREP'],
                    'production': ['NP', 'V_INTRANS', 'PREP'],
                    'description': 'Intransitif + Keterangan'
                })
            # NP ADJ PREP
            elif token_symbols[0] == 'NP' and token_symbols[1] == 'ADJ':
                patterns.append({
                    'pattern': ['NP', 'ADJ', 'PREP'],
                    'production': ['NP', 'ADJ', 'PREP'],
                    'description': 'Wasesa Kahanan + Keterangan'
                })
            # NP NUM PREP
            elif token_symbols[0] == 'NP' and token_symbols[1] == 'NUM':
                patterns.append({
                    'pattern': ['NP', 'NUM', 'PREP'],
                    'production': ['NP', 'NUM', 'PREP'],
                    'description': 'Wasesa Wilangan + Keterangan'
                })
            # NP V_TRANS NP PREP
            elif len(token_symbols) >= 4 and token_symbols[0] == 'NP' and token_symbols[1] == 'V_TRANS' and token_symbols[2] == 'NP':
                patterns.append({
                    'pattern': ['NP', 'V_TRANS', 'NP', 'PREP'],
                    'production': ['NP', 'V_TRANS', 'NP', 'PREP'],
                    'description': 'Transitif + Keterangan'
                })
        
        # 7. Dengan Penguat: NP ADJ ADJ
        if len(token_symbols) >= 3 and token_symbols[0] == 'NP' and token_symbols[1] == 'ADJ' and token_symbols[2] == 'ADJ':
            patterns.append({
                'pattern': ['NP', 'ADJ', 'ADJ'],
                'production': ['NP', 'ADJ', 'ADJ'],
                'description': 'Wasesa Kahanan dengan penguat'
            })
        
        # 8. Dengan Pelengkap: NP V_TRANS NP GEGANEP
        if len(token_symbols) >= 4 and token_symbols[0] == 'NP' and token_symbols[1] == 'V_TRANS' and token_symbols[2] == 'NP' and token_symbols[3] == 'GEGANEP':
            patterns.append({
                'pattern': ['NP', 'V_TRANS', 'NP', 'GEGANEP'],
                'production': ['NP', 'V_TRANS', 'NP', 'GEGANEP'],
                'description': 'Transitif dengan Pelengkap'
            })
        
        # 9. Kalimat majemuk: ... CONJ ...
        if 'CONJ' in token_symbols:
            conj_index = token_symbols.index('CONJ')
            if conj_index > 0 and conj_index < len(token_symbols) - 1:
                patterns.append({
                    'pattern': ['S', 'CONJ', 'S'],
                    'production': ['S', 'CONJ', 'S'],
                    'description': 'Ukara Camboran (Kalimat Majemuk)'
                })
        
        return patterns
    
    def _get_state_specific_patterns(self, token_symbols, fsa_state):
        """Pola khusus berdasarkan state FSA"""
        patterns = []
        
        # Mapping state ke pola yang diharapkan
        state_pattern_map = {
            "q2": [  # State akhir untuk kalimat sederhana
                (['NP', 'V_INTRANS'], "Wasesa Penggawe Intransitif"),
                (['NP', 'ADJ'], "Wasesa Kahanan"),
                (['NP', 'NUM'], "Wasesa Wilangan"),
                (['NP', 'NP'], "Wasesa Aran"),
            ],
            "q5": [  # State akhir untuk transitif
                (['NP', 'V_TRANS', 'NP'], "Wasesa Penggawe Transitif"),
            ],
            "q6": [  # State akhir dengan pelengkap
                (['NP', 'V_TRANS', 'NP', 'GEGANEP'], "Transitif dengan Pelengkap"),
            ],
            "q11": [  # State dengan keterangan tambahan
                (['NP', 'V_INTRANS', 'PREP'], "Intransitif + Keterangan"),
                (['NP', 'ADJ', 'ADJ'], "Wasesa Kahanan dengan penguat"),
                (['NP', 'ADJ', 'PREP'], "Wasesa Kahanan + Keterangan"),
                (['NP', 'NUM', 'PREP'], "Wasesa Wilangan + Keterangan"),
                (['NP', 'V_TRANS', 'NP', 'PREP'], "Transitif + Keterangan"),
            ],
            "q12": [  # State dengan keterangan berganda
                (['NP', 'V_INTRANS', 'PREP', 'PREP'], "Intransitif + Keterangan Berganda"),
                (['NP', 'ADJ', 'ADJ', 'PREP'], "Wasesa Kahanan dengan penguat + keterangan"),
            ]
        }
        
        # Cek pola untuk state saat ini
        if fsa_state in state_pattern_map:
            for pattern, description in state_pattern_map[fsa_state]:
                if len(token_symbols) == len(pattern):
                    match = True
                    for i in range(len(pattern)):
                        if token_symbols[i] != pattern[i]:
                            match = False
                            break
                    
                    if match:
                        patterns.append({
                            'pattern': pattern,
                            'production': pattern,
                            'description': f"{description} (State: {fsa_state})"
                        })
        
        return patterns
    
    def _build_parse_tree(self, pattern, input_tokens):
        """Membangun parse tree dari pattern"""
        tree = {
            "S": {
                "pattern": pattern['description'],
                "production": pattern['production'],
                "tokens": []
            }
        }
        
        # Tambahkan detail token
        for i, (symbol, token) in enumerate(zip(pattern['production'], input_tokens)):
            tree["S"]["tokens"].append({
                "position": i,
                "symbol": symbol,
                "word": token.get('word'),
                "type": token.get('type'),
                "original_type": token.get('original_type')
            })
        
        return tree
    
    def _flexible_parse(self, token_symbols, input_tokens):
        """Parsing fleksibel untuk kasus yang tidak cocok dengan pola tetap"""
        print(Fore.YELLOW + "[PARSER] Mencoba parsing fleksibel...")
        
        # Coba parsing recursive
        try:
            parse_result = self._recursive_parse("S", token_symbols, 0)
            if parse_result:
                tree, remaining = parse_result
                if remaining == len(token_symbols):
                    return True, tree, ["Parsing recursive berhasil"], [], []
        except:
            pass
        
        error_msg = f"Tidak ada pola CFG yang cocok untuk: {token_symbols}"
        print(Fore.RED + f"[PARSER] Error: {error_msg}")
        return False, None, [], [], [error_msg]
    
    def _recursive_parse(self, symbol, tokens, index):
        """Parsing recursive descent sederhana"""
        if index >= len(tokens):
            return None, index
        
        # Jika simbol terminal
        if symbol in ['NP', 'V_INTRANS', 'V_TRANS', 'ADJ', 'NUM', 'CONJ', 'PREP', 'GEGANEP']:
            if tokens[index] == symbol:
                return {'type': symbol, 'value': tokens[index]}, index + 1
            return None, index
        
        # Coba semua produksi untuk non-terminal
        productions = self.grammar.get_production_for(symbol)
        for production in productions:
            current_index = index
            children = []
            valid = True
            
            for sub_symbol in production:
                result, new_index = self._recursive_parse(sub_symbol, tokens, current_index)
                if result is None:
                    valid = False
                    break
                children.append(result)
                current_index = new_index
            
            if valid:
                return {'type': symbol, 'children': children}, current_index
        
        return None, index
