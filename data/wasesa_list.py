# wasesa_list.py

# Kata kerja transitif (Wasesa Penggawe Transitif) - MEMBUTUHKAN OBJEK
WASESA_TRANSITIVE = [
    # =============================================
    # MAKAN & MINUM (EATING & DRINKING) - Transitif
    # =============================================
    'mangan', 'nedha', 'dhahar', 'ngombe', 'nginung',
    'nyruput', 'nyicip', 'nyacah', 'nggigit', 'nyomot',
    'ngunyah', 'ngecap', 'ngeloni', 'ngisep', 'ngulu',
    'ngedhot', 'nguntal', 'ngobong', 'mateng', 'masak',
    
    # =============================================
    # BELANJA & TRANSAKSI - Transitif
    # =============================================
    'tuku', 'mundhut', 'tumbas', 'jupuk', 'bayar', 'mbayar',
    'tukar', 'ijol', 'ngijol', 'nego', 'tawar', 'patok',
    'dagang', 'jual', 'dodol', 'perang',
    
    # =============================================
    # MEMBACA & MENULIS - Transitif
    # =============================================
    'maca', 'maos', 'moco', 'nulis', 'nyerat', 'nggarap',
    'ngetik', 'nyalin', 'nyonto', 'nggambar', 'nyoret',
    'nggaris', 'ngarsip',
    
    # =============================================
    # MEMBAWA & MENGANGKAT - Transitif
    # =============================================
    'nggawa', 'nggendong', 'nggandhul', 'nggotong', 'ngangkat',
    'nganjat', 'ngencengi', 'nyekel', 'ngempit', 'nyangkut',
    'nggantung', 'nggandheng',
    
    # =============================================
    # MEMBERSIHKAN - Transitif
    # =============================================
    'nyapu', 'ngresik', 'ngumbah', 'ngepel', 'ngelap',
    'nyampahi', 'nggawe resik', 'ngresiki', 'mbucal',
    'ngguwang', 'mbuwang', 'ngosok', 'nggosok', 'ngamplas',
    'ngkilap',
    
    # =============================================
    # MELIHAT & MENGAMATI - Transitif
    # =============================================
    'ndelok', 'ningali', 'mirsani', 'ngerteni', 'ngawasi',
    'ngintip', 'ngiler', 'mandeng', 'menggok', 'mawas',
    'mirsa', 'ngaweruhi',
    
    # =============================================
    # BERBICARA - Transitif (butuh objek/topik)
    # =============================================
    'ngomong', 'ngendika', 'kandha', 'celathu', 'ngobrol',
    'guneman', 'rembug', 'rembag', 'ngudar', 'ngaturake',
    'nyritakake', 'nyebut', 'nyandra', 'nyaritakake',
    'ngandhani', 'ngandharake',
    
    # =============================================
    # BEKERJA & MENGOLAH - Transitif
    # =============================================
    'gawe', 'nggawe', 'nyambutgawe', 'makarya', 'ngopeni',
    'ngurusi', 'ngolah', 'ngrampungake', 'nggarap', 'ngrancang',
    'ngrancangi', 'ngrampungi',
    
    # =============================================
    # MEMASAK - Transitif
    # =============================================
    'nggoreng', 'nggodhog', 'nggangsir', 'ngpanggang', 'ngbakar',
    'nguleg', 'ngulek', 'nyampur', 'ngaduk',
    
    #
    # Tambahan Sendiri
    # 
    'dadi'
]

# Kata kerja intransitif (Wasesa Penggawe Intransitif) - TIDAK BUTUH OBJEK
WASESA_INTRANSITIVE = [
    # =============================================
    # TIDUR & ISTIRAHAT - Intransitif
    # =============================================
    'turu', 'sare', 'nglelep', 'mekutha', 'ngorok', 'ngimpi',
    'ndremi', 'ngantuk', 'tilem','tangi',
    
    # =============================================
    # BERGERAK - Intransitif
    # =============================================
    'mlaku', 'lumaku', 'laku', 'mlampah', 'mletik', 'mlayu',
    'mblayu', 'mlumpat', 'mblanjur', 'munggah', 'mudhun',
    'turun', 'naik', 'minggat', 'minggir', 'mlebu', 'metu',
    'lunga', 'tekane', 'teka', 'budhal', 'mangkat', 'miber',
    'mabur', 'nglayang',
    
    # =============================================
    # EMOSI & PERASAAN - Intransitif
    # =============================================
    'seneng', 'bungah', 'susah', 'sedih', 'nesu', 'bungah',
    'sregep', 'semangat', 'kepengin', 'kepingin', 'pengin',
    'karep', 'karsa', 'kangen', 'rindu', 'bingung',
    'guyu', 'nangis', 'mesem',
    
    # =============================================
    # BERMAIN & REKREASI - Intransitif
    # =============================================
    'dolan', 'main', 'maen', 'pliyuran', 'plesiran', 'nglumpuk',
    'ngumpul', 'rame-rame', 'srawung', 'ngaso', 'istirahat',
    'santai', 'leres', 'liburan', 'plesir',
    
    # =============================================
    # BELAJAR & MENGAJAR - Intransitif
    # =============================================
    'sinau', 'maos', 'wulang', 'mulang', 'ngajar', 'marahi',
    'ngandhani', 'nulungi', 'mbantu', 'ngewangi', 'ngewales',
    'ngopeni', 'ngajari'
    
    #SENDIRI
    ,'adus'
]

# Untuk backward compatibility 
WASESA_VOCAB = WASESA_TRANSITIVE + WASESA_INTRANSITIVE