from core.grammar import Grammar
from core.parser import Parser
from core.tokenizer import Tokenizer
from core.automata import FiniteAutomata
from utils.regex_validator import RegexValidator
from utils.error_handler import ErrorHandler as handle
from colorama import Fore, Style

class JawaNgokoAnalyzer:

    def __init__(self):
        self.tokenizer = Tokenizer()
        self.grammar = Grammar()
        self.parser = Parser(self.grammar)
        self.automata = FiniteAutomata()
        self.error_handler = handle()

        #Validasi grammar saat inisialisasi
        issues = self.grammar.validate_grammar()
        if issues:
            for issue in issues:
                print(f"Grammar Validation Issue: {issue}")

    def analyze(self, text, verbose=True):
        """
        Menganalisis teks input melalui tokenisasi, parsing, dan validasi automata.
        Jika verbose=True maka logging diatur ke DEBUG untuk menampilkan informasi lebih detail.
        """

        result = {
            "sentence": text,
            "is_valid": False,
            "tokens": [],
            "fsa_path": [],
            "parse_tree": None,
            "grammar_rules": [],
            "errors": []
        }   

        try:
            #1 Tokenisasi
            print("tokenizing....")
            tokens = self.tokenizer.tokenize(text)
            result['tokens'] = tokens

            #2 Validasi Token
            print("validating tokens....")
            valid_tokens,token_errors = self.tokenizer.validate_tokens(tokens)
            if token_errors:
                print("error token....")
                eror_msg = self.error_handler.handler_error("TOKENIZATION_ERROR", context=text)
                result["errors"].append(eror_msg)
                result["errors"].extend(token_errors)
                return result
            
            
            #3 validasi FSA
            print("validating fsa....")
            token_sequence = self.tokenizer.get_token_sequence(valid_tokens)
            fsa_valid,fsa_path,fsa_message = self.automata.validate_sequence(token_sequence)
            result['fsa_path'] = fsa_path

            if not fsa_valid:
                print("error fsa....")
                eror_msg = self.error_handler.handler_error("FSA_ERROR", context=text)
                result["errors"].append(eror_msg)
                return result
            

            # 4 CFG Parsing
            cfg_valid,parse_tree,parse_steps,grammar_rules,parse_errors = self.parser.parse(valid_tokens)

            result['grammar_rules'] = grammar_rules
            result["errors"].extend(parse_errors)

            # 5 Tentukan validitas akhir
            Validator = RegexValidator()
            if not Validator.validate_sentence_structure(text):
                print("error structure....")
                eror_msg = self.error_handler.handler_error("GRAMMAR_VIOLATION", context=text)
                result["errors"].append(eror_msg)
                cfg_valid = False
                return result
            
            result["is_valid"] = fsa_valid and cfg_valid and len(result["errors"]) == 0

            if verbose:
                self.print_analysis_result(result)
            return result
        except Exception as e:
            result['errors'].append(f"Analysis error: {str(e)}")
            result['is_valid'] = False
            return result
    
    def print_analysis_result(self, analysis_result):
        """
        Mencetak hasil analisis dengan format yang baik.
        """

        print("\n" + "=" * 60)
        print(f"Analysis Results for: '{analysis_result['sentence']}'")
        print("=" * 60)

        print(f"\nStatus Validitas: {'Valid' if analysis_result['is_valid'] else 'Tidak Valid'}\n")

        print(Fore.CYAN + Style.BRIGHT + "=== Hasil Analisis Jawa Ngoko ===")
        print(Fore.YELLOW + f"Kalimat: {analysis_result['sentence']}")
        print(Fore.YELLOW + f"Validitas: {'Valid' if analysis_result['is_valid'] else 'Tidak Valid'}")
        
        print(Fore.GREEN + "\n-- Tokenisasi --")
        for token in analysis_result['tokens']:
            print(f"  Kata: '{token['word']}', Tipe: {token['type']}")
        
        print(Fore.GREEN + "\n-- Jalur FSA --")
        print("  " + " -> ".join(analysis_result['fsa_path']))
        
        print(Fore.GREEN + "\n-- Aturan Grammar yang Digunakan --")
        for rule in analysis_result['grammar_rules']:
            print(f"  {rule}")
        
        if analysis_result['errors']:
            print(Fore.RED + "\n-- Kesalahan Ditemukan --")
            for error in analysis_result['errors']:
                print(f"  {error}")
        else:
            print(Fore.GREEN + "\nTidak ada kesalahan ditemukan. Kalimat valid menurut grammar dan FSA.")
        
        print("\n" + "=" * 60 + "\n")
