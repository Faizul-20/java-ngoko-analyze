

class FiniteAutomata:
    def __init__(self):
        self.states = {
            "q0" : {"JEJER" : "q1"}, #Harus di mulai Dari Jejer
            "q1" : {"WASESA" : "q2"}, # Setelah Jejer Harus Wasesa
            "q2" : {"LESAN" : "q3"}, # Setelah Wasesa Harus Lesan
            "q3" : {"$" : "ACCEPT" } # Setelah Lesan Harus Akhir Input

        }

        self.accept_states = {"q3","ACCEPT"}
        self.current_state = "q0"
        self.path = ["q0"]

    def transition(self, input_symbol):
        """
        Transisi berdasarkan simbol input dan state saat ini.
        """

        if self.current_state not in self.states:
            return False,f"State salah : {self.current_state}"

        if input_symbol in self.states[self.current_state]:
            next_state = self.states[self.current_state][input_symbol]
            self.current_state = next_state
            self.path.append(self.current_state)
            return True,f"Transisi : {input_symbol} -> {next_state}"
        
        #Cek Akhir Input
        if input_symbol == '$' and self.current_state in self.accept_states:
            self.path.append('ACCEPT')
            return True, "ACCEPTED"
        
        return False,f"Transisi tidak valid dari state {self.current_state} dengan simbol {input_symbol}"
    
    def is_accepted(self):
        """
        periksa apkah state saat ini diterima
        """
        return self.current_state in self.accept_states
    
    def validate_sequence(self, input_sequence):
        """
        Validasi urutan input.
        Reset state dan path sebelum validasi agar dapat dijalankan berulang.
        Mengembalikan tuple: (is_valid, path, message)
        """
        # Reset state dan path untuk validasi yang deterministik
        self.current_state = 'q0'
        self.path = ['q0']

        for symbol in input_sequence:
            valid, message = self.transition(symbol)
            if not valid:
                # Kembalikan path saat ini juga agar caller bisa menampilkan jalur hingga kegagalan
                return False, self.path, message
        
        # Cek Akhir Input
        valid, message = self.transition('$')
        if not valid:
            return False, self.path, message
        
        if self.is_accepted():
            return True, self.path, "Input diterima oleh Finite Automata."
        else:
            return False, self.path, "Input tidak diterima oleh Finite Automata."
        
    def get_possible_transitions(self, state):
        """
        Dapatkan transisi yang mungkin dari state tertentu.
        """
        if state in self.states:
            return list(self.states[state].keys())
        return []