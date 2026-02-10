"""
Program Utama - Simulasi Optimasi Rute Pengiriman
Menggunakan Algoritma Greedy (Nearest Neighbor)
"""

from datetime import datetime
from data_lokasi import LOKASI, get_semua_lokasi, get_semua_paket
from algoritma_greedy import AlgoritmaGreedy

def print_separator(char="=", length=80):
    """Print separator line"""
    print(char * length)

def tampilkan_header():
    """Tampilkan header program"""
    print_separator()
    print(" " * 20 + "SISTEM OPTIMASI RUTE PENGIRIMAN BARANG")
    print(" " * 25 + "PT. LOGISTIK CEPAT - MEDAN")
    print(" " * 30 + f"{datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print_separator()

def tampilkan_data_lokasi():
    """Tampilkan semua lokasi pengiriman"""
    print("\n📍 DATA LOKASI PENGIRIMAN")
    print_separator("-", 100)
    print(f"{'No':<4} {'Nama Lokasi':<35} {'Lat':<10} {'Long':<12} {'Tipe':<20}")
    print_separator("-", 100)
    
    for lokasi_id in sorted(LOKASI.keys()):
        loc = LOKASI[lokasi_id]
        print(f"{lokasi_id:<4} {loc['nama']:<35} {loc['lat']:<10.4f} {loc['long']:<12.4f} {loc['tipe']:<20}")
    
    print_separator("-", 100)

def tampilkan_data_paket():
    """Tampilkan semua paket pengiriman"""
    print("\n📦 DATA PAKET PENGIRIMAN")
    print_separator("-", 90)
    print(f"{'ID':<4} {'Lokasi ID':<10} {'Nama Lokasi':<30} {'Berat (kg)':<15} {'Penerima':<20}")
    print_separator("-", 90)
    
    total_berat = 0
    for paket in get_semua_paket():
        lokasi_id = paket["lokasi"]
        lokasi_nama = LOKASI[lokasi_id]["nama"]
        berat = paket["berat"]
        total_berat += berat
        
        print(f"{paket['id']:<4} {lokasi_id:<10} {lokasi_nama:<30} {berat:<15.1f} {paket['penerima']:<20}")
    
    print_separator("-", 90)
    print(f"{'TOTAL PAKET:':<55} {len(get_semua_paket()):<15}")
    print(f"{'TOTAL BERAT:':<55} {total_berat:<15.1f} kg")
    print_separator("-", 90)

def tampilkan_hasil_greedy(algoritma):
    """Tampilkan hasil optimasi dengan algoritma Greedy"""
    print("\n🔍 PROSES OPTIMASI MENGGUNAKAN ALGORITMA NEAREST NEIGHBOR (GREEDY)")
    print_separator("-", 100)
    
    hasil = algoritma.nearest_neighbor(depot_id=0)
    
    print("\n📍 RUTE PENGIRIMAN OPTIMAL:")
    print_separator("-", 100)
    print(f"{'No':<4} {'Dari Lokasi':<35} {'Ke Lokasi':<35} {'Jarak (km)':<12}")
    print_separator("-", 100)
    
    for i, detail in enumerate(hasil["detail_rute"], 1):
        print(f"{i:<4} {detail['dari']:<35} {detail['ke']:<35} {detail['jarak']:<12.2f}")
    
    print_separator("-", 100)
    
    print(f"\n📊 RINGKASAN HASIL OPTIMASI:")
    print(f"   • Jumlah Lokasi Pengiriman: {hasil['jumlah_lokasi']}")
    print(f"   • Total Jarak Tempuh: {hasil['total_jarak']} km")
    print(f"   • Waktu Tempuh (asumsi 40 km/jam): {hasil['waktu_tempuh_menit']} menit ({hasil['waktu_tempuh_menit']/60:.2f} jam)")
    print(f"   • Urutan Rute: {' → '.join([str(i) for i in hasil['rute']])}")
    
    return hasil

def tampilkan_hasil_random(algoritma):
    """Tampilkan hasil dengan rute random untuk perbandingan"""
    print("\n\n🎲 PERBANDINGAN DENGAN RUTE RANDOM")
    print_separator("-", 100)
    
    hasil = algoritma.hitung_rute_random(depot_id=0)
    
    print(f"\n📊 HASIL RUTE RANDOM:")
    print(f"   • Total Jarak Tempuh: {hasil['total_jarak']} km")
    print(f"   • Waktu Tempuh (asumsi 40 km/jam): {hasil['waktu_tempuh_menit']} menit")
    print(f"   • Urutan Rute: {' → '.join([str(i) for i in hasil['rute']])}")
    
    return hasil

def tampilkan_analisis(algoritma, hasil_greedy, hasil_random):
    """Tampilkan analisis performa"""
    print("\n\n📈 ANALISIS PERFORMA")
    print_separator("=", 80)
    
    analisis = algoritma.analisis_performa(hasil_greedy, hasil_random)
    
    print(f"\n   Jarak Greedy (Optimal):     {analisis['jarak_greedy']} km")
    print(f"   Jarak Random (Referensi):   {analisis['jarak_random']} km")
    print(f"   ─" * 40)
    print(f"   Penghematan Jarak:          {analisis['penghematan_jarak']} km")
    print(f"   Efisiensi:                  {analisis['efisiensi_persen']}%")
    print(f"   Waktu Hemat:                {analisis['waktu_hemat_menit']} menit")
    
    print(f"\n✅ Algoritma Greedy lebih efisien {analisis['efisiensi_persen']}% dibanding rute random!")
    print_separator("=", 80)

def tampilkan_penjelasan_algoritma():
    """Tampilkan penjelasan algoritma Greedy"""
    print("\n\n📚 PENJELASAN ALGORITMA NEAREST NEIGHBOR (GREEDY)")
    print_separator("=", 80)
    
    penjelasan = """
STRATEGI GREEDY:
Algoritma Greedy memilih solusi terbaik di setiap langkah dengan harapan mendapat 
solusi global yang optimal atau mendekati optimal.

CARA KERJA NEAREST NEIGHBOR:
1. INISIALISASI
   - Mulai dari depot (lokasi 0 - Jl. Merdeka)
   - Tandai semua lokasi lain sebagai belum dikunjungi

2. LOOP UTAMA (Greedy Selection)
   - Dari lokasi saat ini, cari lokasi terdekat yang BELUM dikunjungi
   - Pilih lokasi terdekat tersebut (inilah langkah greedy)
   - Tandai sebagai sudah dikunjungi
   - Pindah ke lokasi terpilih

3. TERMINASI
   - Ulangi sampai semua lokasi dikunjungi
   - Kembali ke depot

KOMPLEKSITAS WAKTU:
- Time Complexity: O(n²) di mana n = jumlah lokasi
- Space Complexity: O(n)

KEUNTUNGAN:
✓ Cepat dan efisien
✓ Menghasilkan solusi yang cukup baik (70-85% optimal)
✓ Mudah dipahami dan diimplementasikan
✓ Cocok untuk problem size menengah

KEKURANGAN:
✗ Tidak selalu menghasilkan solusi optimal
✗ Bisa terjebak dalam local optimum
✗ Kurang baik untuk problem size sangat besar

APLIKASI REAL-WORLD:
• Rute pengiriman dan logistik
• Perjalanan sales
• Vehicle Routing Problem (VRP)
• Pemeliharaan jaringan
    """
    
    print(penjelasan)
    print_separator("=", 80)

def simpan_hasil_ke_file(hasil_greedy, hasil_random, analisis):
    """Simpan hasil ke file"""
    with open("hasil_simulasi.txt", "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("LAPORAN HASIL SIMULASI OPTIMASI RUTE PENGIRIMAN\n")
        f.write(f"Waktu: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("HASIL ALGORITMA GREEDY (NEAREST NEIGHBOR):\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total Jarak: {hasil_greedy['total_jarak']} km\n")
        f.write(f"Waktu Tempuh: {hasil_greedy['waktu_tempuh_menit']} menit\n")
        f.write(f"Jumlah Lokasi: {hasil_greedy['jumlah_lokasi']}\n")
        f.write(f"Rute: {' → '.join([str(i) for i in hasil_greedy['rute']])}\n\n")
        
        f.write("HASIL RUTE RANDOM (PERBANDINGAN):\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total Jarak: {hasil_random['total_jarak']} km\n")
        f.write(f"Waktu Tempuh: {hasil_random['waktu_tempuh_menit']} menit\n\n")
        
        f.write("ANALISIS PERFORMA:\n")
        f.write("-" * 80 + "\n")
        f.write(f"Penghematan Jarak: {analisis['penghematan_jarak']} km\n")
        f.write(f"Efisiensi: {analisis['efisiensi_persen']}%\n")
        f.write(f"Waktu Hemat: {analisis['waktu_hemat_menit']} menit\n")

def main():
    """Program utama"""
    # Header
    tampilkan_header()
    
    # Data
    tampilkan_data_lokasi()
    tampilkan_data_paket()
    
    # Inisialisasi algoritma
    print("\n⏳ Menginisialisasi algoritma...")
    algoritma = AlgoritmaGreedy(LOKASI)
    
    # Jalankan algoritma
    print("✓ Algoritma diinisialisasi\n")
    
    # Hasil Greedy
    hasil_greedy = tampilkan_hasil_greedy(algoritma)
    
    # Hasil Random
    hasil_random = tampilkan_hasil_random(algoritma)
    
    # Analisis
    analisis = algoritma.analisis_performa(hasil_greedy, hasil_random)
    tampilkan_analisis(algoritma, hasil_greedy, hasil_random)
    
    # Penjelasan
    tampilkan_penjelasan_algoritma()
    
    # Simpan hasil
    simpan_hasil_ke_file(hasil_greedy, hasil_random, analisis)
    print("\n✓ Hasil simulasi disimpan ke 'hasil_simulasi.txt'")
    
    print("\n" + "=" * 80)
    print("Program selesai!")
    print("=" * 80)

if __name__ == "__main__":
    main()
