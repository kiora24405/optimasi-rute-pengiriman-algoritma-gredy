"""
Implementasi Algoritma Greedy - Nearest Neighbor
untuk Optimasi Rute Pengiriman Barang
"""

import math
from data_lokasi import LOKASI, get_semua_lokasi

class AlgoritmaGreedy:
    """Implementasi Algoritma Nearest Neighbor untuk TSP"""
    
    def __init__(self, lokasi_data):
        """
        Inisialisasi algoritma
        
        Args:
            lokasi_data: Dictionary berisi data lokasi dengan lat/long
        """
        self.lokasi = lokasi_data
        self.jarak_cache = {}
    
    def hitung_jarak(self, lokasi1_id, lokasi2_id):
        """
        Menghitung jarak Euclidean antara dua lokasi
        
        Args:
            lokasi1_id: ID lokasi pertama
            lokasi2_id: ID lokasi kedua
            
        Returns:
            Jarak dalam kilometer
        """
        # Cek cache
        key = (min(lokasi1_id, lokasi2_id), max(lokasi1_id, lokasi2_id))
        if key in self.jarak_cache:
            return self.jarak_cache[key]
        
        loc1 = self.lokasi[lokasi1_id]
        loc2 = self.lokasi[lokasi2_id]
        
        lat1, long1 = loc1["lat"], loc1["long"]
        lat2, long2 = loc2["lat"], loc2["long"]
        
        # Formula Haversine untuk jarak geografis (disederhanakan untuk Medan)
        # 1 derajat ≈ 111 km
        delta_lat = (lat2 - lat1) * 111
        delta_long = (long2 - long1) * 111 * math.cos(math.radians((lat1 + lat2) / 2))
        
        jarak = math.sqrt(delta_lat**2 + delta_long**2)
        
        # Cache hasil
        self.jarak_cache[key] = jarak
        return jarak
    
    def nearest_neighbor(self, depot_id=0):
        """
        Algoritma Nearest Neighbor (Greedy)
        
        Strategi:
        1. Mulai dari depot
        2. Dari lokasi saat ini, pilih lokasi terdekat yang belum dikunjungi
        3. Kunjungi lokasi tersebut
        4. Ulangi hingga semua lokasi dikunjungi
        5. Kembali ke depot
        
        Args:
            depot_id: ID depot (default: 0)
            
        Returns:
            Dictionary dengan rute, total jarak, dan detail
        """
        # Semua lokasi kecuali depot
        semua_lokasi = set(get_semua_lokasi())
        semua_lokasi.discard(depot_id)
        
        rute = [depot_id]
        belum_dikunjungi = semua_lokasi.copy()
        lokasi_saat_ini = depot_id
        total_jarak = 0
        detail_rute = []
        
        # Greedy Loop
        while belum_dikunjungi:
            # Cari lokasi terdekat dari lokasi saat ini
            lokasi_terdekat = None
            jarak_min = float('inf')
            
            for lokasi_id in belum_dikunjungi:
                jarak = self.hitung_jarak(lokasi_saat_ini, lokasi_id)
                
                if jarak < jarak_min:
                    jarak_min = jarak
                    lokasi_terdekat = lokasi_id
            
            # Kunjungi lokasi terdekat
            total_jarak += jarak_min
            rute.append(lokasi_terdekat)
            belum_dikunjungi.remove(lokasi_terdekat)
            
            # Catat detail
            detail_rute.append({
                "dari": self.lokasi[lokasi_saat_ini]["nama"],
                "ke": self.lokasi[lokasi_terdekat]["nama"],
                "jarak": round(jarak_min, 2)
            })
            
            lokasi_saat_ini = lokasi_terdekat
        
        # Kembali ke depot
        jarak_kembali = self.hitung_jarak(lokasi_saat_ini, depot_id)
        total_jarak += jarak_kembali
        rute.append(depot_id)
        
        detail_rute.append({
            "dari": self.lokasi[lokasi_saat_ini]["nama"],
            "ke": self.lokasi[depot_id]["nama"],
            "jarak": round(jarak_kembali, 2)
        })
        
        return {
            "rute": rute,
            "total_jarak": round(total_jarak, 2),
            "jumlah_lokasi": len(get_semua_lokasi()) - 1,
            "detail_rute": detail_rute,
            "waktu_tempuh_menit": round((total_jarak / 40) * 60, 2)  # Asumsi kecepatan 40 km/jam
        }
    
    def hitung_rute_random(self, depot_id=0):
        """
        Menghitung rute random untuk perbandingan
        
        Args:
            depot_id: ID depot
            
        Returns:
            Dictionary dengan rute random, total jarak
        """
        import random
        
        semua_lokasi = list(get_semua_lokasi())
        semua_lokasi.remove(depot_id)
        random.shuffle(semua_lokasi)
        
        rute = [depot_id] + semua_lokasi + [depot_id]
        
        total_jarak = 0
        for i in range(len(rute) - 1):
            total_jarak += self.hitung_jarak(rute[i], rute[i+1])
        
        return {
            "rute": rute,
            "total_jarak": round(total_jarak, 2),
            "jumlah_lokasi": len(get_semua_lokasi()) - 1,
            "waktu_tempuh_menit": round((total_jarak / 40) * 60, 2)
        }
    
    def analisis_performa(self, hasil_greedy, hasil_random):
        """
        Analisis performa algoritma Greedy vs Random
        
        Args:
            hasil_greedy: Hasil dari nearest_neighbor()
            hasil_random: Hasil dari hitung_rute_random()
            
        Returns:
            Dictionary dengan analisis
        """
        jarak_greedy = hasil_greedy["total_jarak"]
        jarak_random = hasil_random["total_jarak"]
        
        efisiensi = ((jarak_random - jarak_greedy) / jarak_random) * 100
        
        return {
            "jarak_greedy": jarak_greedy,
            "jarak_random": jarak_random,
            "penghematan_jarak": round(jarak_random - jarak_greedy, 2),
            "persentase_penghematan": round(efisiensi, 2),
            "efisiensi_greedy": round(efisiensi, 2),
            "efisiensi_persen": round(efisiensi, 2),
            "waktu_hemat_menit": round((hasil_random["waktu_tempuh_menit"] - hasil_greedy["waktu_tempuh_menit"]), 2)
        }
