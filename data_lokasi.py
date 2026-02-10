"""
Data Dummy untuk Lokasi Pengiriman di Medan
Format: (nama_lokasi, latitude, longitude, tipe_lokasi)
"""

LOKASI = {
    0: {"nama": "Depot (Jl. Merdeka)", "lat": 3.1956, "long": 101.6964, "tipe": "Pusat Distribusi"},
    1: {"nama": "Toko A (Jl. Ahmad Yani)", "lat": 3.1996, "long": 101.7046, "tipe": "Toko Elektronik"},
    2: {"nama": "Toko B (Jl. Gatot Subroto)", "lat": 3.2011, "long": 101.7086, "tipe": "Toko Fashion"},
    3: {"nama": "Rumah C (Jl. Diponegoro)", "lat": 3.2025, "long": 101.7020, "tipe": "Rumah Pribadi"},
    4: {"nama": "Kantor D (Jl. Sudirman)", "lat": 3.2008, "long": 101.6950, "tipe": "Kantor Perusahaan"},
    5: {"nama": "Toko E (Jl. Iskandar Muda)", "lat": 3.2055, "long": 101.7100, "tipe": "Minimarket"},
    6: {"nama": "Rumah F (Jl. Cik Ditiro)", "lat": 3.1920, "long": 101.6900, "tipe": "Rumah Pribadi"},
    7: {"nama": "Toko G (Jl. Slamet Riyadi)", "lat": 3.1880, "long": 101.6950, "tipe": "Toko Kelontong"},
    8: {"nama": "Kantor H (Jl. Imam Bonjol)", "lat": 3.1850, "long": 101.7050, "tipe": "Kantor Cabang"},
    9: {"nama": "Rumah I (Jl. Mesjid)", "lat": 3.1910, "long": 101.7120, "tipe": "Rumah Pribadi"},
    10: {"nama": "Toko J (Jl. Zainul Arifin)", "lat": 3.1970, "long": 101.7180, "tipe": "Toko Buku"},
    11: {"nama": "Kantor K (Jl. Pendidikan)", "lat": 3.2040, "long": 101.6920, "tipe": "Kantor Pemerintah"},
    12: {"nama": "Rumah L (Jl. Brigjen Katamso)", "lat": 3.1790, "long": 101.6880, "tipe": "Rumah Pribadi"},
    13: {"nama": "Toko M (Jl. Pemuda)", "lat": 3.1920, "long": 101.7220, "tipe": "Toko Mainan"},
    14: {"nama": "Rumah N (Jl. Putri Hijau)", "lat": 3.2095, "long": 101.7050, "tipe": "Rumah Pribadi"},
}

# Daftar paket pengiriman
PAKET = [
    {"id": 1, "lokasi": 1, "berat": 2.5, "penerima": "Ahmad"},
    {"id": 2, "lokasi": 2, "berat": 1.2, "penerima": "Siti"},
    {"id": 3, "lokasi": 3, "berat": 3.0, "penerima": "Budi"},
    {"id": 4, "lokasi": 4, "berat": 0.8, "penerima": "Rina"},
    {"id": 5, "lokasi": 5, "berat": 2.1, "penerima": "Hendra"},
    {"id": 6, "lokasi": 6, "berat": 1.5, "penerima": "Desi"},
    {"id": 7, "lokasi": 7, "berat": 2.8, "penerima": "Rudi"},
    {"id": 8, "lokasi": 8, "berat": 0.5, "penerima": "Lina"},
    {"id": 9, "lokasi": 9, "berat": 1.9, "penerima": "Toni"},
    {"id": 10, "lokasi": 10, "berat": 3.2, "penerima": "Maya"},
    {"id": 11, "lokasi": 11, "berat": 1.1, "penerima": "Arif"},
    {"id": 12, "lokasi": 12, "berat": 2.6, "penerima": "Eva"},
    {"id": 13, "lokasi": 13, "berat": 0.9, "penerima": "Joni"},
    {"id": 14, "lokasi": 14, "berat": 2.3, "penerima": "Ayu"},
]

def get_lokasi_info(lokasi_id):
    """Mendapatkan informasi lokasi berdasarkan ID"""
    return LOKASI.get(lokasi_id, None)

def get_semua_lokasi():
    """Mendapatkan semua lokasi ID"""
    return list(LOKASI.keys())

def get_semua_paket():
    """Mendapatkan semua paket"""
    return PAKET
