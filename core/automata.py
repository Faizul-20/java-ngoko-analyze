# [file name]: automata.py (UPDATED)
class FiniteAutomata:
    def __init__(self):
        # State diagram yang lebih lengkap sesuai gambar
        # q0: Start → Jejer → q1
        # q1: Wasesa → q2 (intransitif) atau q3 (transitif)
        # q3: Lesan → q5 → (Geganep) → q6 atau (Ketrangan) → q12
        # Dari q2/q5/q6 bisa ke q11 (Ketrangan) → q12 (Ketrangan akhir)
        # Bisa kembali ke q0 via KONJ untuk kalimat majemuk
        
        self.states = {
            # Q0: Start state - menunggu Jejer, Keterangan,V_INTRANS
            "q0": {
                "JEJER": "q1",
                "KETRANGAN": "q4",  # Bisa mulai dengan keterangan
                "WASESA_INTRANS" : "q1"  
            },
            
            # Q1: Setelah Jejer - bisa ke berbagai jenis Wasesa
            "q1": {
                "WASESA_INTRANS": "q2",   # Intransitif
                "WASESA_TRANS": "q3",     # Transitif
                "KS": "q2",               # Kata sifat
                "KW": "q2",               # Kata bilangan
                "NP": "q2",               # Wasesa Aran (NP langsung)
                "KETRANGAN": "q4",         # Ke keterangan
                "JEJER":"q2",
                "KONJ": "q0"              # Kalimat majemuk
                
            },
            
            # Q2: Final untuk kalimat sederhana (intransitif, adjektival, numeral, nominal)
            "q2": {
            
                "$": "ACCEPT",
                "KETRANGAN": "q11",       # Tambah keterangan
                "KONJ": "q0",             # Kalimat majemuk
                "KS": "q11",              # Penguat kata sifat
                "KW": "q11",              # Tambahan bilangan
                "PREP": "q11",          # Preposisi sebagai keterangan
                "WASESA_TRANS" : "q11",
                "WASESA_INTRANS" : "q11"
                
            },
            
            # Q3: State untuk transitif - menunggu Lesan (objek)
            "q3": {
                "LESAN": "q5",
                "NP": "q5",               # Lesan juga NP
                "KETRANGAN": "q4",        # Bisa ke keterangan dulu
                "JEJER": "q5"             # Error: double subject
            },
            
            # Q4: Setelah Ketrangan - kembali ke pola normal
            "q4": {
                "WASESA_INTRANS": "q2",
                "WASESA_TRANS": "q3",
                "KS": "q2",
                "KW": "q2",
                "NP": "q2",
                "JEJER": "q1"             # Bisa kembali ke Jejer
            },
            
            # Q5: Setelah Lesan (objek) - transitif valid
            "q5": {
                "$": "ACCEPT",
                "GEGANEP": "q6",          # Pelengkap
                "KETRANGAN": "q11",       # Keterangan
                "KS": "q11",              # Kata sifat sebagai keterangan
                "KW": "q11",              # Kata bilangan
                "KONJ": "q0"              # Kalimat majemuk
            },
            
            # Q6: Setelah Geganep (pelengkap)
            "q6": {
                "$": "ACCEPT",
                "KETRANGAN": "q11",
                "KS": "q11",
                "KW": "q11",
                "KONJ": "q0"
            },
            
            # Q9: Error state - double Jejer
            "q9": {
                "$": "REJECT",
                "KETRANGAN": "REJECT",
                "KONJ": "REJECT"
            },
            
            # Q11: State untuk keterangan tambahan
            "q11": {
                "$": "ACCEPT",
                "KETRANGAN": "q12",       # Keterangan berantai
                "KS": "q11",              # KS berulang
                "KW": "q11",              # KW berulang
                "KONJ": "q0"              # Kalimat majemuk
            },
            
            # Q12: State akhir setelah keterangan berantai
            "q12": {
                "$": "ACCEPT",
                "KONJ": "q0"              # Bisa ke kalimat majemuk
            },
            
            # ACCEPT: State diterima
            "ACCEPT": {
                "$": "ACCEPT"
            },
            
            # REJECT: State ditolak
            "REJECT": {
                "$": "REJECT"
            }
        }
        
        # Mapping simbol untuk fleksibilitas
        self.symbol_mapping = {
            "KB": "JEJER",          # Kata benda
            "WASESA": "WASESA_TRANS",  # Default wasesa ke transitif
            "ADJ": "KS",            # Adjective ke KS
            "NUM": "KW",            # Numeral ke KW
            "PREP": "KETRANGAN"     # Preposition ke keterangan
        }
        
        self.start_state = "q0"
        self.accept_states = {"q2", "q5", "q6", "q11", "q12", "ACCEPT"}
        self.reject_states = {"q9", "REJECT"}
        self.current_state = self.start_state
        self.path = [self.start_state]
        self.history = []
        
        print(f"[FSA] Inisialisasi: {len(self.states)} states, {len(self.accept_states)} accept states")
    
    def _map_symbol(self, symbol):
        """Map simbol input ke simbol yang dikenali FSA"""
        if symbol in self.symbol_mapping:
            return self.symbol_mapping[symbol]
        return symbol
    
    def transition(self, input_symbol):
        """
        Transisi berdasarkan simbol input.
        """
        mapped_symbol = self._map_symbol(input_symbol)
        
        # Simpan history
        self.history.append({
            'state': self.current_state,
            'input': input_symbol,
            'mapped': mapped_symbol,
            'time': len(self.history)
        })
        
        print(f"  [FSA] {self.current_state} --{input_symbol} ({mapped_symbol})--> ", end="")
        
        if self.current_state not in self.states:
            print(f"ERROR: State {self.current_state} tidak ada")
            return False, f"State {self.current_state} tidak valid"
        
        transitions = self.states[self.current_state]
        
        if mapped_symbol in transitions:
            next_state = transitions[mapped_symbol]
            print(f"{next_state}")
            
            self.current_state = next_state
            self.path.append(next_state)
            
            # Beri deskripsi transisi
            desc = self._get_transition_description(self.current_state)
            return True, f"{mapped_symbol} → {next_state} ({desc})"
        
        # Cek untuk end of input
        if input_symbol == "$":
            if self.current_state in self.accept_states:
                self.path.append("ACCEPT")
                print(f"ACCEPTED")
                return True, "Kalimat valid"
            elif self.current_state in self.reject_states:
                self.path.append("REJECT")
                print(f"REJECTED")
                return False, "Kalimat tidak valid"
        
        print(f"ERROR: Tidak ada transisi")
        return False, f"Tidak ada transisi dari {self.current_state} dengan '{mapped_symbol}'"
    
    def _get_state_description(self, state):
        """Deskripsi untuk setiap state"""
        descriptions = {
            "q0": "START: Menunggu Jejer (Subjek) atau Keterangan awal",
            "q1": "JEJER DITERIMA: Siap menerima Wasesa (predikat)",
            "q2": "KALIMAT SEDERHANA VALID: Intransitif/KS/KW/NP",
            "q3": "MENUNGGU OBJEK: Setelah Wasesa transitif, butuh Lesan",
            "q4": "KETERANGAN AWAL: Telah menerima keterangan, butuh predikat",
            "q5": "TRANSITIF VALID: Sudah ada subjek, predikat, dan objek",
            "q6": "DENGAN PELENGKAP: Transitif + objek + pelengkap",
            "q9": "ERROR: Dua Jejer berturut-turut",
            "q11": "KETERANGAN TAMBAHAN: Bisa diakhiri atau tambah lagi",
            "q12": "KETERANGAN AKHIR: Siap diakhiri",
            "ACCEPT": "KALIMAT DITERIMA",
            "REJECT": "KALIMAT DITOLAK"
        }
        return descriptions.get(state, f"State {state}")
    
    def _get_transition_description(self, state):
        """Deskripsi khusus untuk transisi ke state tertentu"""
        if state == "q2":
            return "Kalimat intransitif/adjektival/numeral/nominal valid"
        elif state == "q5":
            return "Kalimat transitif valid (S-P-O)"
        elif state == "q6":
            return "Kalimat dengan pelengkap valid"
        elif state == "ACCEPT":
            return "Kalimat diterima secara lengkap"
        elif state == "REJECT":
            return "Struktur kalimat tidak valid"
        else:
            return self._get_state_description(state)
    
    def reset(self):
        """Reset automata ke state awal"""
        self.current_state = self.start_state
        self.path = [self.start_state]
        self.history = []
    
    def validate_sequence(self, input_sequence):
        """
        Validasi urutan token.
        Mengembalikan (is_valid, path, message)
        """
        print(f"\n{'='*60}")
        print(f"[FSA] VALIDASI: {input_sequence}")
        print(f"{'='*60}")
        
        self.reset()
        
        # Tambahkan end marker
        sequence_with_end = input_sequence + ["$"]
        
        for i, symbol in enumerate(sequence_with_end):
            print(f"\nStep {i+1}/{len(sequence_with_end)}: ", end="")
            valid, message = self.transition(symbol)
            
            if not valid:
                print(f"\n✗ GAGAL: {message}")
                print(f"Path: {' → '.join(self.path)}")
                return False, self.path, message
            
            # Jika sampai di REJECT state, hentikan
            if self.current_state == "REJECT":
                print(f"\n✗ DITOLAK: Struktur tidak valid")
                return False, self.path, "Struktur kalimat tidak valid"
        
        # Cek apakah berakhir di accept state
        final_state = self.path[-1] if self.path else "UNKNOWN"
        
        if final_state in self.accept_states or final_state == "ACCEPT":
            print(f"\n{'='*60}")
            print(f"✓ BERHASIL: Diterima di state {final_state}")
            print(f"Path: {' → '.join(self.path)}")
            print(f"{'='*60}")
            
            # Berikan analisis pola
            pattern_analysis = self._analyze_pattern(self.path)
            print(f"Pola: {pattern_analysis}")
            
            return True, self.path, f"Diterima ({pattern_analysis})"
        else:
            print(f"\n✗ GAGAL: State akhir {final_state} tidak diterima")
            print(f"Path: {' → '.join(self.path)}")
            return False, self.path, f"State akhir tidak diterima"
    
    def _analyze_pattern(self, path):
        """Analisis pola kalimat berdasarkan path"""
        if "q2" in path and "q11" in path:
            return "Kalimat dengan keterangan tambahan"
        elif "q5" in path and "q6" in path:
            return "Kalimat transitif dengan pelengkap"
        elif "q5" in path:
            return "Kalimat transitif sederhana (S-P-O)"
        elif "q2" in path:
            return "Kalimat intransitif/adjektival/numeral/nominal"
        elif "q0" in path and "KONJ" in [h.get('input') for h in self.history]:
            return "Kalimat majemuk"
        else:
            return "Kalimat sederhana"
    
    def get_detailed_analysis(self):
        """Dapatkan analisis detail FSA"""
        return {
            "current_state": self.current_state,
            "state_description": self._get_state_description(self.current_state),
            "is_accepting": self.current_state in self.accept_states,
            "is_rejecting": self.current_state in self.reject_states,
            "path": self.path.copy(),
            "history": self.history.copy(),
            "possible_transitions": list(self.states.get(self.current_state, {}).keys())
        }
