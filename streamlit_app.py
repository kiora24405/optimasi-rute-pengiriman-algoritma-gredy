"""
Aplikasi Visualisasi Rute Pengiriman Menggunakan Streamlit dan Folium
"""

import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime
from data_lokasi import LOKASI, get_semua_lokasi, get_semua_paket
from algoritma_greedy import AlgoritmaGreedy

# ============================================================================
# KONFIGURASI STREAMLIT
# ============================================================================

st.set_page_config(
    page_title="Optimasi Rute Pengiriman",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🚚 Sistem Optimasi Rute Pengiriman")
st.markdown("**PT. Logistik Cepat - Medan** | Algoritma Nearest Neighbor (Greedy)")

# ============================================================================
# SIDEBAR - KONFIGURASI
# ============================================================================

with st.sidebar:
    st.header("⚙️ Pengaturan")
    
    depot_id = st.selectbox(
        "Pilih Depot Awal:",
        options=get_semua_lokasi(),
        format_func=lambda x: f"{x}: {LOKASI[x]['nama']}"
    )
    
    kecepatan = st.slider(
        "Kecepatan Pengiriman (km/jam):",
        min_value=20,
        max_value=80,
        value=40,
        step=5
    )
    
    st.divider()
    st.markdown("### 📊 Informasi Umum")
    st.metric("Total Lokasi Pengiriman", len(get_semua_lokasi()) - 1)
    st.metric("Total Paket", len(get_semua_paket()))
    
    total_berat = sum([p["berat"] for p in get_semua_paket()])
    st.metric("Total Berat (kg)", f"{total_berat:.1f}")

# ============================================================================
# INISIALISASI ALGORITMA
# ============================================================================

algoritma = AlgoritmaGreedy(LOKASI)
hasil_greedy = algoritma.nearest_neighbor(depot_id=depot_id)

# ============================================================================
# TAB UTAMA
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Peta Rute",
    "📊 Data & Statistik",
    "📈 Perbandingan",
    "📋 Detail Rute"
])

# ============================================================================
# TAB 1: PETA RUTE
# ============================================================================

with tab1:
    st.header("Visualisasi Peta Rute Pengiriman")
    
    col1, col2 = st.columns([3, 1])
    
    with col2:
        st.subheader("Legenda")
        st.markdown("""
        - 🟩 **Depot** (pusat distribusi)
        - 🔵 **Lokasi Pengiriman**
        - 🔴 **Lokasi di Rute**
        - **Garis Merah** = Rute Optimal
        """)
    
    with col1:
        # Buat peta Folium
        medan_center = [3.1957, 101.6964]  # Koordinat pusat Medan
        
        map_rute = folium.Map(
            location=medan_center,
            zoom_start=14,
            tiles="OpenStreetMap"
        )
        
        # Tambah marker untuk semua lokasi
        rute_set = set(hasil_greedy['rute'])
        
        for lokasi_id in get_semua_lokasi():
            loc = LOKASI[lokasi_id]
            
            if lokasi_id == depot_id:
                # Depot - marker khusus
                folium.Marker(
                    location=[loc['lat'], loc['long']],
                    popup=f"<b>DEPOT</b><br>{loc['nama']}<br>({loc['lat']:.4f}, {loc['long']:.4f})",
                    tooltip=loc['nama'],
                    icon=folium.Icon(color='green', icon='home', prefix='fa')
                ).add_to(map_rute)
            elif lokasi_id in rute_set:
                # Lokasi di rute
                folium.CircleMarker(
                    location=[loc['lat'], loc['long']],
                    radius=8,
                    popup=f"<b>{lokasi_id}: {loc['nama']}</b><br>Tipe: {loc['tipe']}<br>({loc['lat']:.4f}, {loc['long']:.4f})",
                    tooltip=f"{lokasi_id}: {loc['nama']}",
                    color='red',
                    fill=True,
                    fillColor='red',
                    fillOpacity=0.7,
                    weight=2
                ).add_to(map_rute)
            else:
                # Lokasi tidak di rute
                folium.CircleMarker(
                    location=[loc['lat'], loc['long']],
                    radius=6,
                    popup=f"<b>{lokasi_id}: {loc['nama']}</b><br>Tipe: {loc['tipe']}<br>({loc['lat']:.4f}, {loc['long']:.4f})",
                    tooltip=f"{lokasi_id}: {loc['nama']}",
                    color='blue',
                    fill=True,
                    fillColor='blue',
                    fillOpacity=0.5,
                    weight=2
                ).add_to(map_rute)
        
        # Gambar garis rute
        rute_coords = [
            [LOKASI[loc_id]['lat'], LOKASI[loc_id]['long']]
            for loc_id in hasil_greedy['rute']
        ]
        
        folium.PolyLine(
            rute_coords,
            color='red',
            weight=2,
            opacity=0.8,
            popup='Rute Optimal'
        ).add_to(map_rute)
        
        # Tamplikan peta
        st_folium(map_rute, width=1200, height=600)

# ============================================================================
# TAB 2: DATA & STATISTIK
# ============================================================================

with tab2:
    st.header("Data & Statistik Pengiriman")
    
    # Bagian 1: Data Lokasi
    st.subheader("📍 Data Lokasi Pengiriman")
    
    data_lokasi = []
    for lokasi_id in sorted(LOKASI.keys()):
        loc = LOKASI[lokasi_id]
        is_in_route = "✓" if lokasi_id in rute_set else ""
        data_lokasi.append({
            "ID": lokasi_id,
            "Nama Lokasi": loc['nama'],
            "Latitude": f"{loc['lat']:.6f}",
            "Longitude": f"{loc['long']:.6f}",
            "Tipe": loc['tipe'],
            "Di Rute": is_in_route
        })
    
    df_lokasi = pd.DataFrame(data_lokasi)
    st.dataframe(df_lokasi, use_container_width=True)
    
    st.divider()
    
    # Bagian 2: Data Paket
    st.subheader("📦 Data Paket Pengiriman")
    
    data_paket = []
    for paket in get_semua_paket():
        lokasi_id = paket["lokasi"]
        lokasi_nama = LOKASI[lokasi_id]["nama"]
        data_paket.append({
            "ID Paket": paket['id'],
            "Lokasi ID": lokasi_id,
            "Nama Lokasi": lokasi_nama,
            "Berat (kg)": paket['berat'],
            "Penerima": paket['penerima']
        })
    
    df_paket = pd.DataFrame(data_paket)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Paket", len(df_paket))
    with col2:
        st.metric("Total Berat", f"{df_paket['Berat (kg)'].sum():.1f} kg")
    with col3:
        st.metric("Rata-rata Berat", f"{df_paket['Berat (kg)'].mean():.2f} kg")
    
    st.dataframe(df_paket, use_container_width=True)
    
    st.divider()
    
    # Bagian 3: Statistik Rute
    st.subheader("📈 Statistik Rute Optimal")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Total Jarak",
            f"{hasil_greedy['total_jarak']:.2f} km"
        )
    
    with col2:
        waktu_jam = hasil_greedy['total_jarak'] / kecepatan
        waktu_menit = waktu_jam * 60
        st.metric(
            "Waktu Tempuh",
            f"{waktu_menit:.0f} menit",
            f"({waktu_jam:.2f} jam)"
        )
    
    with col3:
        st.metric(
            "Jumlah Lokasi",
            hasil_greedy['jumlah_lokasi']
        )
    
    with col4:
        rata_jarak = hasil_greedy['total_jarak'] / hasil_greedy['jumlah_lokasi']
        st.metric(
            "Rata-rata Jarak/Lokasi",
            f"{rata_jarak:.2f} km"
        )

# ============================================================================
# TAB 3: PERBANDINGAN
# ============================================================================

with tab3:
    st.header("Perbandingan Algoritma")
    
    # Hitung rute random untuk perbandingan
    hasil_random = algoritma.hitung_rute_random(depot_id=depot_id)
    
    # Analisis performa
    analisis = algoritma.analisis_performa(hasil_greedy, hasil_random)
    
    # Tabel perbandingan
    st.subheader("📊 Tabel Perbandingan")
    
    perbandingan_data = {
        "Metrik": [
            "Total Jarak (km)",
            "Waktu Tempuh (menit)",
            "Jumlah Lokasi",
            "Rata-rata Jarak/Lokasi"
        ],
        "Nearest Neighbor (Greedy)": [
            f"{hasil_greedy['total_jarak']:.2f}",
            f"{(hasil_greedy['total_jarak'] / kecepatan) * 60:.0f}",
            f"{hasil_greedy['jumlah_lokasi']}",
            f"{hasil_greedy['total_jarak'] / hasil_greedy['jumlah_lokasi']:.2f}"
        ],
        "Rute Random": [
            f"{hasil_random['total_jarak']:.2f}",
            f"{(hasil_random['total_jarak'] / kecepatan) * 60:.0f}",
            f"{hasil_random['jumlah_lokasi']}",
            f"{hasil_random['total_jarak'] / hasil_random['jumlah_lokasi']:.2f}"
        ]
    }
    
    df_perbandingan = pd.DataFrame(perbandingan_data)
    st.dataframe(df_perbandingan, use_container_width=True)
    
    st.divider()
    
    # Hasil analisis
    st.subheader("📈 Hasil Analisis Performa")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Penghematan Jarak",
            f"{analisis['penghematan_jarak']:.2f} km",
            f"{analisis['persentase_penghematan']:.1f}%"
        )
    
    with col2:
        st.metric(
            "Efisiensi",
            f"{analisis['efisiensi_greedy']:.1f}%",
            "Lebih baik dari random"
        )
    
    with col3:
        performa_ratio = hasil_random['total_jarak'] / hasil_greedy['total_jarak']
        st.metric(
            "Rasio Performa",
            f"{performa_ratio:.2f}x",
            "Greedy lebih optimal"
        )

# ============================================================================
# TAB 4: DETAIL RUTE
# ============================================================================

with tab4:
    st.header("📋 Detail Rute Pengiriman")
    
    st.subheader("Urutan Rute Optimal")
    
    # Tampilkan rute step by step
    rute_text = " → ".join([
        f"{loc_id}\n({LOKASI[loc_id]['nama'][:20]}...)" 
        if len(LOKASI[loc_id]['nama']) > 20 
        else f"{loc_id}\n({LOKASI[loc_id]['nama']})"
        for loc_id in hasil_greedy['rute']
    ])
    
    st.info(f"**Rute Optimal:**\n\n{rute_text}")
    
    st.divider()
    
    # Detail setiap perjalanan
    st.subheader("Detail Setiap Perjalanan")
    
    detail_data = []
    for i, detail in enumerate(hasil_greedy['detail_rute'], 1):
        detail_data.append({
            "No": i,
            "Dari Lokasi": detail['dari'],
            "Ke Lokasi": detail['ke'],
            "Jarak (km)": f"{detail['jarak']:.2f}",
            "Waktu (menit)": f"{detail['jarak'] / kecepatan * 60:.1f}"
        })
    
    df_detail = pd.DataFrame(detail_data)
    st.dataframe(df_detail, use_container_width=True)
    
    st.divider()
    
    # Ringkasan
    st.subheader("📊 Ringkasan Hasil")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Jarak", f"{hasil_greedy['total_jarak']:.2f} km")
    
    with col2:
        waktu_menit = (hasil_greedy['total_jarak'] / kecepatan) * 60
        st.metric("Total Waktu", f"{waktu_menit:.0f} menit")
    
    with col3:
        st.metric("Jumlah Lokasi", hasil_greedy['jumlah_lokasi'])
    
    with col4:
        st.metric("Jumlah Perjalanan", len(hasil_greedy['detail_rute']))

# ============================================================================
# FOOTER
# ============================================================================

st.divider()
st.markdown("""
---
**Keterangan Algoritma Greedy (Nearest Neighbor):**
- Algoritma ini memilih lokasi terdekat yang belum dikunjungi dari posisi saat ini
- Memberikan solusi yang cukup baik dan efisien untuk masalah Traveling Salesman Problem (TSP)
- Waktu komputasi: O(n²)
- Cocok untuk rute pengiriman dengan jumlah lokasi sedang (10-100 lokasi)

**© 2026 PT. Logistik Cepat - Medan**
""")
