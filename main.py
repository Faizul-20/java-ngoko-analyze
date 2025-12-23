#!/usr/bin/env python3
"""
Main Application: Syntax Analyzer Bahasa Jawa Ngoko
"""

import sys
from colorama import init, Fore, Style
from core.analyzer import JawaNgokoAnalyzer
from utils.error_handler import ErrorHandler

init(autoreset=True)  # Initialize colorama
    
class MainApp:
    def __init__(self):
        self.analyzer = JawaNgokoAnalyzer()
        self.error_handler = ErrorHandler()

    def print_welcome(self):
        print(Fore.GREEN + Style.BRIGHT + "Selamat datang di Jawa Ngoko Analyzer!")
        print("Masukkan kalimat dalam bahasa Jawa Ngoko untuk dianalisis.")
        print("Ketik 'exit' untuk keluar dari aplikasi.\n")

    def run_test_case(self):
        # Contoh kalimat untuk pengujian
        test_sentences = [
            "Aku mangan sego",
            "Kowe ngombe banyu",
            "Dheweke tuku buku",
            "Ibu maca layang",
            "Bapak nulis tas",
            "Mas nggawa klambi",
            "Mbakyu nyapu omah"
        ]

        for sentence in test_sentences:
            print(Fore.MAGENTA + f"\nMenganalisis kalimat: '{sentence}'")
            analysis_result = self.analyzer.analyze(sentence, verbose=True)
            print(Fore.YELLOW + f"Hasil Analisis: {'VALID' if analysis_result['is_valid'] else 'TIDAK VALID'}")

            if not analysis_result['is_valid']:
                print(Fore.RED + "Kalimat tidak valid. Menangani kesalahan...")
                if 'errors' in analysis_result:
                    for error in analysis_result['errors']:
                        self.error_handler.handler_error(error, context=sentence)
                        print(Fore.YELLOW + f"- Error: {error}")
            else:
                print(Fore.GREEN + "Kalimat valid menurut grammar dan FSA.")
    

    def interactive_mode(self):
        while True:
            user_input = input(Fore.WHITE + "\nMasukkan kalimat Jawa Ngoko (atau ketik 'exit' untuk keluar): ").strip()
            if user_input.lower() == 'exit':
                print(Fore.GREEN + "Terima kasih telah menggunakan Jawa Ngoko Analyzer. Sampai jumpa!")
                break

            analysis_result = self.analyzer.analyze(user_input, verbose=True)

            if not analysis_result['is_valid']:
                if 'errors' in analysis_result:
                    for error in analysis_result['errors']:
                        ErrorHandler().handler_error(Exception(error), context=user_input)
                        print(Fore.YELLOW + f"- Error: {error}")
            else:
                print(Fore.GREEN + "Kalimat valid menurut grammar dan FSA.")


    def run(self):
        try:
            self.print_welcome()

            print(f"\n{Fore.WHITE} Pilih Mode Analisis:")
            print(f"1. {Fore.CYAN}Mode Interaktif")
            print(f"2. {Fore.CYAN}Mode Pengujian dengan Kasus Contoh")
            print(f"3. {Fore.CYAN}Keluar")

            choice = input(f"\n{Fore.WHITE}Masukkan pilihan Anda (1/2/3): ").strip()

            if choice == '1':
                self.interactive_mode()
            elif choice == '2':
                self.run_test_case()
            elif choice == '3':
                print(Fore.GREEN + "Terima kasih telah menggunakan Jawa Ngoko Analyzer. Sampai jumpa!")
                sys.exit(0)
            else:
                print(Fore.RED + "Pilihan tidak valid. Silakan coba lagi.")
        except KeyboardInterrupt:
            print(Fore.GREEN + "\nTerima kasih telah menggunakan Jawa Ngoko Analyzer. Sampai jumpa!")
            sys.exit(0)
            
if __name__ == "__main__":
    main_app = MainApp()
    main_app.run()