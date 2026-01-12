from core.grammar import Grammar
from core.parser import Parser
from core.tokenizer import Tokenizer
from core.automata import FiniteAutomata
from utils.error_handler import ErrorHandler as handle
from colorama import Fore, Style

class JawaNgokoAnalyzer:
    def __init__(self):
        print(Fore.CYAN + "\n" + "="*60)
        print("JAWA NGOKO ANALYZER - CFG & FSA IMPLEMENTATION")
        print("="*60)
        
        self.tokenizer = Tokenizer()
        self.grammar = Grammar()
        self.parser = Parser(self.grammar)
        self.automata = FiniteAutomata()
        self.error_handler = handle()
        
        print(Fore.GREEN + "\n✅ Sistem CFG + FSA siap digunakan\n")

    def analyze(self, text, verbose=True):
        """
        Menganalisis teks input dengan CFG dan FSA.
        """
        print(Fore.CYAN + "\n" + "="*60)
        print(Fore.WHITE + f"ANALISIS: '{text}'")
        print(Fore.CYAN + "="*60)
        
        result = {
            "sentence": text,
            "is_valid": False,
            "tokens": [],
            "fsa_path": [],
            "parse_tree": None,
            "grammar_rules": [],
            "cfg_valid": False,
            "fsa_valid": False,
            "errors": []
        }

        try:
            # 1. TOKENIZATION
            print(Fore.CYAN + "\n[1] TOKENISASI")
            print(Fore.WHITE + "-"*40)
            
            tokens = self.tokenizer.tokenize(text)
            result['tokens'] = tokens
            
            if not tokens:
                result['errors'].append("Tokenisasi gagal: tidak ada token yang dihasilkan")
                return result
            
            # 2. VALIDASI TOKEN
            print(Fore.CYAN + "\n[2] VALIDASI TOKEN")
            print(Fore.WHITE + "-"*40)
            
            valid_tokens, token_errors = self.tokenizer.validate_tokens(tokens)
            
            if token_errors:
                print(Fore.YELLOW + "Ada token yang tidak valid")
                result['errors'].extend(token_errors)
                # Tetap lanjut untuk melihat FSA dan CFG
            
            # 3. FSA VALIDATION (Finite State Automata)
            print(Fore.CYAN + "\n[3] VALIDASI FSA (Finite State Automata)")
            print(Fore.WHITE + "-"*40)
            
            token_sequence = self.tokenizer.get_token_sequence(valid_tokens)
            fsa_valid, fsa_path, fsa_message = self.automata.validate_sequence(token_sequence)
            result['fsa_path'] = fsa_path
            result['fsa_valid'] = fsa_valid
            
            if not fsa_valid:
                print(Fore.RED + f"FSA Error: {fsa_message}")
                result['errors'].append(f"FSA: {fsa_message}")
            
            # 4. CFG PARSING (Context-Free Grammar)
            print(Fore.CYAN + "\n[4] PARSING CFG (Context-Free Grammar)")
            print(Fore.WHITE + "-"*40)
            
            cfg_valid, parse_tree, parse_steps, grammar_rules, parse_errors = self.parser.parse(valid_tokens)
            
            result['parse_tree'] = parse_tree
            result['grammar_rules'] = grammar_rules
            result['cfg_valid'] = cfg_valid
            result['errors'].extend(parse_errors)
            
            if not cfg_valid and parse_errors:
                print(Fore.RED + f"CFG Parsing error: {parse_errors}")
            
            # 5. TENTUKAN VALIDITAS AKHIR
            # Kalimat valid jika lolos FSA DAN CFG
            result["is_valid"] = fsa_valid and cfg_valid and len(result["errors"]) == 0
            
            # 6. TAMPILKAN HASIL
            print(Fore.CYAN + "\n" + "="*60)
            print(Fore.WHITE + "HASIL AKHIR")
            print(Fore.CYAN + "="*60)
            
            status_color = Fore.GREEN if result['is_valid'] else Fore.RED
            status_text = "VALID" if result['is_valid'] else "TIDAK VALID"
            
            print(f"{status_color}{status_text}{Style.RESET_ALL}")
            print(Fore.WHITE + f"  FSA: {'✓' if fsa_valid else '✗'} {'→ '.join(fsa_path)}")
            print(Fore.WHITE + f"  CFG: {'✓' if cfg_valid else '✗'} {len(grammar_rules)} aturan diterapkan")
            
            if result['errors']:
                print(Fore.YELLOW + f"  Errors: {len(result['errors'])}")
            
            print(Fore.CYAN + "="*60)
            
            if verbose:
                self._print_detailed_result(result)
            
            return result
            
        except Exception as e:
            error_msg = f"Error analisis: {str(e)}"
            print(Fore.RED + f"EXCEPTION: {error_msg}")
            result['errors'].append(error_msg)
            result['is_valid'] = False
            return result
    
    def _print_detailed_result(self, result):
        """Cetak hasil detail"""
        print(Fore.CYAN + "\n📋 DETAIL ANALISIS:")
        print(Fore.WHITE + f"Kalimat: '{result['sentence']}'")
        
        print(Fore.CYAN + "\n📊 STATUS VALIDASI:")
        print(Fore.WHITE + f"  FSA: {'✓ LULUS' if result['fsa_valid'] else '✗ GAGAL'}")
        print(Fore.WHITE + f"  CFG: {'✓ LULUS' if result['cfg_valid'] else '✗ GAGAL'}")
        print(Fore.WHITE + f"  FINAL: {'✓ VALID' if result['is_valid'] else '✗ TIDAK VALID'}")
        
        print(Fore.CYAN + "\n🔤 TOKEN:")
        for i, token in enumerate(result['tokens'], 1):
            token_type = token['type']
            word = token['word']
            
            if token_type == 'UNKNOWN':
                print(Fore.RED + f"  {i}. UNKNOWN: '{word}'")
            else:
                color_mapping = {
                    'JEJER': Fore.CYAN,
                    'WASESA_TRANS': Fore.RED,
                    'WASESA_INTRANS': Fore.YELLOW,
                    'LESAN': Fore.GREEN,
                    'KS': Fore.MAGENTA,
                    'KW': Fore.LIGHTYELLOW_EX,
                    'KONJ': Fore.LIGHTBLACK_EX,
                    'KETRANGAN': Fore.LIGHTCYAN_EX
                }
                color = color_mapping.get(token_type, Fore.WHITE)
                print(f"  {i}. {color}{token_type}: '{word}'{Style.RESET_ALL}")
        
        if result['fsa_path']:
            print(Fore.CYAN + "\n🔄 JALUR FSA:")
            path_with_desc = []
            automata = FiniteAutomata()
            for state in result['fsa_path']:
                desc = automata.get_state_description(state)
                short_desc = desc.split(":")[0] if ":" in desc else desc
                path_with_desc.append(f"{state} ({short_desc})")
            
            print(Fore.WHITE + f"  {' → '.join(path_with_desc)}")
        
        if result['grammar_rules']:
            print(Fore.CYAN + "\n📝 ATURAN CFG YANG DIGUNAKAN:")
            for i, rule in enumerate(result['grammar_rules'], 1):
                print(Fore.WHITE + f"  {i}. {rule}")
        
        if result['parse_tree']:
            print(Fore.CYAN + "\n🌳 PARSE TREE:")
            self._print_tree(result['parse_tree'])
        
        if result['errors']:
            print(Fore.RED + "\n❌ KESALAHAN:")
            for i, error in enumerate(result['errors'], 1):
                print(Fore.YELLOW + f"  {i}. {error}")
        else:
            print(Fore.GREEN + "\n✅ Tidak ada kesalahan ditemukan.")
    
    def _print_tree(self, tree, indent=0):
        """Helper untuk mencetak parse tree"""
        for key, value in tree.items():
            print("  " * indent + f"{key}")
            if isinstance(value, dict):
                self._print_tree(value, indent + 1)
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        self._print_tree(item, indent + 1)
                    else:
                        print("  " * (indent + 1) + f"{item}")