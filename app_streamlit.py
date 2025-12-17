import streamlit as st
import pickle
import pandas as pd
import numpy as np

# --- Konfigurasi Halaman Streamlit ---
st.set_page_config(
    page_title="Sistem Penilaian Kelayakan Pembiayaan LKMS",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Judul Aplikasi ---
st.title("💰 Sistem Penilaian Kelayakan Pembiayaan")
st.subheader("Lembaga Keuangan Mikro Syariah (LKMS) berbasis Artificial Intelligence")

# --- Muat Model AI ---
@st.cache_resource
def load_model():
    with open('credit_scoring_model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

model = load_model()

# --- Sidebar: Informasi Aplikasi ---
with st.sidebar:
    st.header("📋 Informasi Aplikasi")
    st.write("""
    Aplikasi ini menggunakan **Machine Learning** untuk memprediksi kelayakan pembiayaan 
    berdasarkan data pemohon.
    
    **Fitur Utama:**
    - Prediksi otomatis kelayakan pembiayaan
    - Probabilitas persetujuan
    - Penjelasan faktor-faktor penentu
    
    **Status Teknologi:** TKT 6 (Prototipe Fungsional)
    """)
    
    st.divider()
    st.write("**Dikembangkan oleh:** Manus AI")
    st.write("**Tahun:** 2025")

# --- Tabs untuk Navigasi ---
tab1, tab2, tab3 = st.tabs(["🔍 Penilaian Kelayakan", "📊 Informasi Model", "❓ Panduan Penggunaan"])

# ============================================================================
# TAB 1: PENILAIAN KELAYAKAN
# ============================================================================
with tab1:
    st.header("Masukkan Data Pemohon Pembiayaan")
    
    # Bagi form menjadi dua kolom untuk tampilan yang lebih rapi
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📌 Data Pribadi")
        
        # Gender
        gender = st.selectbox(
            "Jenis Kelamin",
            options=["Laki-laki", "Perempuan"],
            help="Pilih jenis kelamin pemohon"
        )
        gender_male = 1 if gender == "Laki-laki" else 0
        
        # Marital Status
        married = st.selectbox(
            "Status Pernikahan",
            options=["Belum Menikah", "Sudah Menikah"],
            help="Pilih status pernikahan pemohon"
        )
        married_yes = 1 if married == "Sudah Menikah" else 0
        
        # Dependents
        dependents = st.number_input(
            "Jumlah Tanggungan",
            min_value=0,
            max_value=10,
            value=0,
            step=1,
            help="Jumlah anggota keluarga yang menjadi tanggungan"
        )
        
        # Education
        education = st.selectbox(
            "Pendidikan Terakhir",
            options=["Sarjana/Lebih Tinggi", "Kurang dari Sarjana"],
            help="Pilih tingkat pendidikan tertinggi"
        )
        education_not_grad = 1 if education == "Kurang dari Sarjana" else 0
        
        # Self-Employed
        self_employed = st.selectbox(
            "Status Pekerjaan",
            options=["Karyawan", "Wiraswasta"],
            help="Pilih status pekerjaan pemohon"
        )
        self_employed_yes = 1 if self_employed == "Wiraswasta" else 0
    
    with col2:
        st.subheader("💼 Data Finansial")
        
        # Applicant Income
        applicant_income = st.number_input(
            "Pendapatan Pemohon (dalam Ribuan Rupiah)",
            min_value=0,
            value=3000,
            step=500,
            help="Pendapatan bulanan pemohon. Input 3000 berarti Rp 3.000.000. (Asumsi skala prototipe)"
        )
        
        # Coapplicant Income
        coapplicant_income = st.number_input(
            "Pendapatan Pasangan (dalam Ribuan Rupiah)",
            min_value=0,
            value=0,
            step=500,
            help="Pendapatan bulanan pasangan. Input 500 berarti Rp 500.000. (Asumsi skala prototipe)"
        )
        
        # Total Income
        total_income = applicant_income + coapplicant_income
        
        # Loan Amount
        loan_amount = st.number_input(
            "Jumlah Pembiayaan (dalam Ribuan Rupiah)",
            min_value=0,
            value=120,
            step=10,
            help="Jumlah pembiayaan yang dimohon. Input 120 berarti Rp 120.000. (Asumsi skala prototipe)"
        )
        
        # Loan Amount Term
        loan_term = st.number_input(
            "Jangka Waktu Pembiayaan (bulan)",
            min_value=1,
            max_value=600,
            value=360,
            step=12,
            help="Durasi pembiayaan dalam bulan"
        )
        
        # Credit History
        credit_history = st.selectbox(
            "Riwayat Kredit/Kepatuhan Pembayaran",
            options=["Baik (Tidak ada tunggakan)", "Bermasalah (Ada tunggakan)"],
            help="Status riwayat pembayaran atau kepatuhan sebelumnya"
        )
        credit_history_val = 1 if credit_history == "Baik (Tidak ada tunggakan)" else 0
    
    # --- Data Lokasi ---
    st.subheader("📍 Lokasi Properti")
    col3, col4 = st.columns(2)
    
    with col3:
        property_area = st.selectbox(
            "Lokasi Properti",
            options=["Perkotaan", "Pinggiran Kota", "Pedesaan"],
            help="Pilih lokasi properti/usaha"
        )
    
    with col4:
        # Encode property area
        if property_area == "Pinggiran Kota":
            property_semiurban = 1
            property_urban = 0
        elif property_area == "Perkotaan":
            property_semiurban = 0
            property_urban = 1
        else:  # Pedesaan
            property_semiurban = 0
            property_urban = 0
    
    # --- Tombol Prediksi ---
    st.divider()
    
    if st.button("🔮 Prediksi Kelayakan Pembiayaan", use_container_width=True, type="primary"):
        # Siapkan data untuk prediksi
        input_data = pd.DataFrame({
            'Dependents': [dependents],
            'LoanAmount': [loan_amount],
            'Loan_Amount_Term': [loan_term],
            'Credit_History': [credit_history_val],
            'TotalIncome': [total_income],
            'Gender_Male': [gender_male],
            'Married_Yes': [married_yes],
            'Education_Not Graduate': [education_not_grad],
            'Self_Employed_Yes': [self_employed_yes],
            'Property_Area_Semiurban': [property_semiurban],
            'Property_Area_Urban': [property_urban]
        })
        
        # Lakukan prediksi
        prediction = model.predict(input_data)[0]
        probability = model.predict_proba(input_data)[0]
        
        # Tampilkan hasil
        st.divider()
        st.subheader("📊 Hasil Prediksi")
        
        # Hasil Utama
        col_result1, col_result2 = st.columns(2)
        
        with col_result1:
            if prediction == 1:
                st.success("✅ **PEMBIAYAAN DIREKOMENDASIKAN UNTUK DISETUJUI**", icon="✅")
                status_text = "Pemohon memenuhi kriteria kelayakan pembiayaan."
            else:
                st.error("❌ **PEMBIAYAAN TIDAK DIREKOMENDASIKAN**", icon="❌")
                status_text = "Pemohon belum memenuhi kriteria kelayakan pembiayaan."
            
            st.write(status_text)
        
        with col_result2:
            # Probabilitas
            prob_approved = probability[1] * 100
            prob_rejected = probability[0] * 100
            
            st.metric(
                label="Probabilitas Disetujui",
                value=f"{prob_approved:.1f}%",
                delta=f"Kemungkinan Ditolak: {prob_rejected:.1f}%"
            )
        
        # Visualisasi Probabilitas
        st.divider()
        st.subheader("📈 Visualisasi Probabilitas")
        
        col_chart1, col_chart2 = st.columns(2)
        
        with col_chart1:
            # Bar chart
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots(figsize=(6, 4))
            categories = ['Disetujui', 'Ditolak']
            values = [prob_approved, prob_rejected]
            colors = ['#2ecc71', '#e74c3c']
            ax.bar(categories, values, color=colors, alpha=0.7, edgecolor='black')
            ax.set_ylabel('Probabilitas (%)', fontsize=12)
            ax.set_title('Probabilitas Hasil Prediksi', fontsize=14, fontweight='bold')
            ax.set_ylim([0, 100])
            for i, v in enumerate(values):
                ax.text(i, v + 2, f'{v:.1f}%', ha='center', fontweight='bold')
            plt.tight_layout()
            st.pyplot(fig)
        
        with col_chart2:
            # Gauge chart (simplified)
            st.write("**Skor Kelayakan:**")
            st.progress(prob_approved / 100, text=f"{prob_approved:.1f}%")
            st.write("*Semakin tinggi persentase, semakin layak pembiayaan disetujui.*")
        
        # Rekomendasi Tindak Lanjut
        st.divider()
        st.subheader("💡 Rekomendasi Tindak Lanjut")
        
        if prediction == 1:
            st.info("""
            ✅ **Rekomendasi:** Pembiayaan dapat dipertimbangkan untuk disetujui.
            
            **Langkah Selanjutnya:**
            1. Verifikasi data yang telah diinput
            2. Lakukan pengecekan dokumen pendukung (KTP, NPWP, laporan keuangan, dll.)
            3. Kunjungan lapangan untuk validasi usaha/properti
            4. Penetapan besaran dan jangka waktu pembiayaan
            5. Penandatanganan perjanjian pembiayaan
            """)
        else:
            st.warning("""
            ⚠️ **Rekomendasi:** Pembiayaan perlu ditinjau lebih lanjut atau ditolak.
            
            **Kemungkinan Penyebab:**
            - Riwayat kredit yang bermasalah (faktor utama)
            - Pendapatan yang tidak mencukupi
            - Rasio pembiayaan terhadap pendapatan terlalu tinggi
            
            **Saran untuk Pemohon:**
            1. Perbaiki riwayat pembayaran jika ada tunggakan
            2. Naikkan pendapatan atau kurangi jumlah pembiayaan
            3. Cari co-borrower dengan pendapatan tambahan
            4. Ajukan kembali setelah kondisi finansial membaik
            """)

# ============================================================================
# TAB 2: INFORMASI MODEL
# ============================================================================
with tab2:
    st.header("📊 Informasi Model AI")
    
    st.subheader("🎯 Tujuan Model")
    st.write("""
    Model ini dirancang untuk memprediksi **kelayakan pembiayaan** berdasarkan profil pemohon. 
    Model menggunakan algoritma **Logistic Regression** dari *scikit-learn*, yang memberikan 
    hasil prediksi yang akurat dan mudah diinterpretasi.
    """)
    
    st.subheader("📈 Kinerja Model")
    
    col_perf1, col_perf2, col_perf3 = st.columns(3)
    
    with col_perf1:
        st.metric(label="Akurasi", value="85.37%", delta="Pada data uji")
    
    with col_perf2:
        st.metric(label="Presisi (Ditolak)", value="95%", delta="Tingkat kepercayaan")
    
    with col_perf3:
        st.metric(label="Recall (Disetujui)", value="99%", delta="Tingkat pendeteksian")
    
    st.divider()
    
    st.subheader("🔑 Faktor Penentu Kelayakan (Feature Importance)")
    st.write("""
    Berdasarkan analisis model, faktor-faktor berikut memiliki pengaruh terbesar terhadap 
    keputusan kelayakan pembiayaan:
    """)
    
    importance_data = {
        'Faktor': [
            'Riwayat Kredit/Kepatuhan',
            'Lokasi Properti (Pinggiran)',
            'Status Pernikahan',
            'Pendidikan',
            'Pendapatan Total',
            'Jumlah Tanggungan'
        ],
        'Pengaruh': [
            'Sangat Positif (Dominan)',
            'Positif',
            'Positif',
            'Negatif',
            'Negatif (Minimal)',
            'Positif'
        ],
        'Interpretasi': [
            'Faktor paling penting. Riwayat pembayaran yang baik sangat meningkatkan kelayakan.',
            'Lokasi di pinggiran kota meningkatkan peluang persetujuan.',
            'Status menikah sedikit meningkatkan peluang persetujuan.',
            'Pendidikan lebih rendah sedikit mengurangi peluang persetujuan.',
            'Pendapatan tinggi tidak signifikan mempengaruhi (sudah tercakup dalam Credit History).',
            'Jumlah tanggungan sedikit meningkatkan peluang persetujuan.'
        ]
    }
    
    df_importance = pd.DataFrame(importance_data)
    st.table(df_importance)
    
    st.divider()
    
    st.subheader("⚙️ Spesifikasi Teknis")
    
    tech_info = {
        'Aspek': [
            'Algoritma',
            'Tingkat Kesiapterapan Teknologi (TKT)',
            'Akurasi Model',
            'Jumlah Fitur',
            'Data Latih',
            'Data Uji',
            'Framework',
            'Bahasa Pemrograman'
        ],
        'Detail': [
            'Logistic Regression (scikit-learn)',
            'TKT 6 (Prototipe Fungsional)',
            '85.37%',
            '11 fitur',
            '491 sampel',
            '123 sampel',
            'Streamlit',
            'Python 3.11'
        ]
    }
    
    df_tech = pd.DataFrame(tech_info)
    st.table(df_tech)

# ============================================================================
# TAB 3: PANDUAN PENGGUNAAN
# ============================================================================
with tab3:
    st.header("❓ Panduan Penggunaan Aplikasi")
    
    st.subheader("📖 Cara Menggunakan Aplikasi")
    
    st.write("""
    ### Langkah 1: Masukkan Data Pemohon
    
    Pada tab **"Penilaian Kelayakan"**, masukkan data pemohon pembiayaan dengan rinci:
    
    - **Data Pribadi:** Jenis kelamin, status pernikahan, jumlah tanggungan, pendidikan, status pekerjaan
    - **Data Finansial:** Pendapatan pemohon, pendapatan pasangan, jumlah pembiayaan, jangka waktu
    - **Data Lainnya:** Lokasi properti, riwayat kredit/kepatuhan pembayaran
    
    ### Langkah 2: Klik Tombol Prediksi
    
    Setelah semua data diisi, klik tombol **"🔮 Prediksi Kelayakan Pembiayaan"** untuk memulai analisis.
    
    ### Langkah 3: Interpretasi Hasil
    
    Aplikasi akan menampilkan:
    - **Status Rekomendasi:** Disetujui atau Ditolak
    - **Probabilitas:** Persentase kemungkinan persetujuan
    - **Visualisasi:** Grafik probabilitas untuk pemahaman yang lebih mudah
    - **Rekomendasi Tindak Lanjut:** Saran langkah selanjutnya
    
    ### Langkah 4: Tindak Lanjut
    
    Gunakan hasil prediksi sebagai **alat bantu** dalam pengambilan keputusan. Tetap lakukan 
    verifikasi dokumen dan kunjungan lapangan sesuai prosedur LKMS.
    """)
    
    st.divider()
    
    st.subheader("⚠️ Catatan Penting")
    
    st.warning("""
    1. **Alat Bantu, Bukan Keputusan Final:** Model ini adalah alat bantu analisis. 
       Keputusan akhir tetap harus diambil oleh petugas LKMS dengan mempertimbangkan faktor lain.
    
    2. **Akurasi Model:** Model memiliki akurasi 85.37%, artinya ada kemungkinan kesalahan prediksi 
       sebesar ~14.63%. Selalu verifikasi dengan data dan informasi tambahan.
    
    3. **Data Harus Akurat:** Masukkan data yang akurat dan lengkap untuk hasil prediksi yang optimal.
    
    4. **Privasi Data:** Data yang Anda masukkan hanya digunakan untuk prediksi dan tidak disimpan 
       di server aplikasi.
    
    5. **Keterbatasan Model:** Model dikembangkan dengan data simulasi. Untuk hasil yang lebih akurat, 
       model perlu dilatih ulang dengan data historis LKMS yang spesifik.
    """)
    
    st.divider()
    
    st.subheader("🤔 Pertanyaan Umum (FAQ)")
    
    with st.expander("Apa itu TKT 6?"):
        st.write("""
        **TKT 6** adalah **Tingkat Kesiapterapan Teknologi Level 6**, yang berarti teknologi 
        telah dikembangkan dan diuji dalam lingkungan yang relevan (simulasi). Model ini siap 
        untuk demonstrasi di lingkungan operasional yang sebenarnya (TKT 7).
        """)
    
    with st.expander("Bagaimana model membuat prediksi?"):
        st.write("""
        Model menggunakan algoritma **Logistic Regression** yang telah dilatih dengan data historis 
        pembiayaan. Berdasarkan profil pemohon yang Anda masukkan, model menghitung probabilitas 
        kelayakan dan memberikan rekomendasi.
        """)
    
    with st.expander("Apakah model bisa salah?"):
        st.write("""
        Ya, model memiliki tingkat akurasi 85.37%, yang berarti ada kemungkinan kesalahan. 
        Oleh karena itu, hasil prediksi harus selalu dikonfirmasi dengan verifikasi dokumen 
        dan kunjungan lapangan.
        """)
    
    with st.expander("Bagaimana cara meningkatkan akurasi model?"):
        st.write("""
        Untuk meningkatkan akurasi, model perlu dilatih ulang dengan data historis LKMS yang spesifik. 
        Ini adalah bagian dari fase TKT 7-9 dalam program SINERGI.
        """)

# --- Footer ---
st.divider()
st.markdown("""
---
**Aplikasi Penilaian Kelayakan Pembiayaan LKMS**  
Dikembangkan untuk Program Hilirisasi Riset Prioritas dan Strategis – SINERGI 2026  
Manus AI | 2025
""")
