#!/usr/bin/env python3
"""
Main Application: Syntax Analyzer Bahasa Jawa Ngoko
"""

from colorama import init, Fore
from core.analyzer import JawaNgokoAnalyzer

init(autoreset=True)

class MainApp:
    def __init__(self):
        self.analyzer = JawaNgokoAnalyzer()
        

    def run_test_case(self):
        """Pengujian dengan contoh kalimat"""
        print(Fore.CYAN + "\nPENGUJIAN OTOMATIS")
        
        test_cases = [
            ("aku mangan sego", True),
            ("adik turu", True),
            ("omahku gedhe", True),
            ("bapakku guru", True),
            ("aku mangan lan dheweke ngombe", True),
            ("mangan aku sego", False),
            ("aku", False),
            ("aku mangan", False),
        ]

        for sentence, expected in test_cases:
            result = self.analyzer.analyze(sentence, verbose=False)
            status = "✓" if result['is_valid'] == expected else "✗"
            color = Fore.GREEN if result['is_valid'] == expected else Fore.RED
            print(f"{color}{status} '{sentence}': {'VALID' if result['is_valid'] else 'TIDAK VALID'}")
            
            if not result['is_valid'] and result['errors']:
                print(Fore.YELLOW + f"  Error: {result['errors'][0]}")

        input("\nTekan Enter untuk lanjut...")

    def interactive_mode(self):
        """Analisis kalimat dari pengguna"""
        print(Fore.CYAN + "\nMODE INTERAKTIF")
        
        while True:
            print(Fore.WHITE + "-"*40)
            user_input = input(Fore.YELLOW + "Masukkan kalimat: ").strip()
            
            if user_input.lower() == 'exit':
                break
            
            if not user_input:
                continue
            
            result = self.analyzer.analyze(user_input, verbose=False)
            
            if result['is_valid']:
                print(Fore.GREEN + "✅ VALID")
                print(Fore.CYAN + f"Token: {[t['type'] for t in result['tokens']]}")
                print(Fore.CYAN + f"FSA: {' → '.join(result['fsa_path'])}")
            else:
                print(Fore.RED + "❌ TIDAK VALID")
                if result['errors']:
                    print(Fore.YELLOW + f"Error: {result['errors'][0]}")

    def run(self):
        """Metode utama"""
        try:
            while True:
                
                print(Fore.WHITE + "\nMENU:")
                print("1. Analisis Kalimat")
                print("2. Pengujian Otomatis")
                print("3. Keluar")
                
                choice = input(Fore.YELLOW + "Pilih: ").strip()
                
                if choice == '1':
                    self.interactive_mode()
                elif choice == '2':
                    self.run_test_case()
                elif choice == '3':
                    print(Fore.GREEN + "Terima kasih!")
                    break
                    
        except KeyboardInterrupt:
            print(Fore.YELLOW + "\nProgram dihentikan")

if __name__ == "__main__":
    app = MainApp()
    app.run()