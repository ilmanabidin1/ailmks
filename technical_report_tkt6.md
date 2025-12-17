# Laporan Teknis Prototipe Model Kecerdasan Buatan untuk Penilaian Kelayakan Pembiayaan (TKT 6)

**Judul Proposal SINERGI:** Metode Penilaian Kelayakan Pembiayaan pada Lembaga Keuangan Mikro Syariah berbasis Artificial Intelegent

**Tingkat Kesiapterapan Teknologi (TKT) Saat Ini:** TKT 6 (Prototipe Fungsional)

## I. Pendahuluan

Laporan teknis ini bertujuan untuk menyajikan hasil pengembangan dan pengujian prototipe model *Artificial Intelligence* (AI) untuk penilaian kelayakan pembiayaan (Credit Scoring). Pengembangan model ini merupakan **Bukti Konsep (Proof of Concept/PoC)** yang berfungsi sebagai dasar teknis untuk pengajuan Program Hilirisasi Riset Prioritas dan Strategis – SINERGI, khususnya skema Inovasi Sosial, yang mensyaratkan minimal TKT 6.

Model ini dikembangkan menggunakan algoritma *Machine Learning* yang umum digunakan dalam industri keuangan untuk memprediksi risiko gagal bayar, yang dapat diadaptasi untuk konteks Lembaga Keuangan Mikro Syariah (LKMS).

## II. Metodologi Pengembangan Prototipe

### 1. Sumber Data
Untuk tujuan PoC dan mencapai TKT 6, digunakan data publik historis pinjaman (Loan Approval Prediction Dataset) yang telah dianonimkan. Data ini mensimulasikan variabel-variabel kunci yang relevan dalam proses persetujuan pembiayaan, seperti pendapatan, riwayat kredit, dan karakteristik pemohon.

### 2. Pra-pemrosesan Data
Data melalui proses pembersihan dan rekayasa fitur, meliputi:
*   **Penanganan Nilai Hilang:** Mengisi nilai yang hilang pada variabel kategorikal dengan modus (nilai terbanyak) dan variabel numerik dengan rata-rata.
*   **Rekayasa Fitur:** Menggabungkan pendapatan pemohon dan pasangan (*ApplicantIncome* dan *CoapplicantIncome*) menjadi satu fitur **TotalIncome**.
*   **Encoding:** Mengubah variabel kategorikal menjadi format numerik melalui *Label Encoding* (untuk variabel target `Loan_Status`) dan *One-Hot Encoding* (untuk variabel fitur lainnya).

### 3. Model yang Digunakan
Model yang dipilih adalah **Regresi Logistik (Logistic Regression)**. Model ini dipilih karena memiliki keunggulan dalam hal **interpretasi** (kemampuan menjelaskan faktor-faktor yang mempengaruhi keputusan), yang sangat penting untuk transparansi dalam konteks keuangan syariah.

## III. Hasil dan Evaluasi Model

Model dilatih menggunakan 80% data dan dievaluasi pada 20% data uji.

### 1. Kinerja Model

| Metrik Evaluasi | Nilai | Interpretasi |
| :--- | :--- | :--- |
| **Akurasi (Accuracy)** | 85.37% | Model berhasil memprediksi status pembiayaan dengan benar pada 85.37% kasus dalam data uji. |
| **Presisi (Not Approved)** | 95% | Dari semua prediksi "Tidak Disetujui", 95% benar-benar tidak disetujui. |
| **Recall (Approved)** | 99% | Dari semua kasus yang "Disetujui", model berhasil mengidentifikasi 99% di antaranya. |

### 2. Matriks Kebingungan (Confusion Matrix)

| Prediksi \ Aktual | Tidak Disetujui (N) | Disetujui (Y) |
| :--- | :--- | :--- |
| **Prediksi Tidak Disetujui** | 21 (True Negative) | 1 (False Negative) |
| **Prediksi Disetujui** | 17 (False Positive) | 84 (True Positive) |

**Analisis Kritis:**
Model menunjukkan kinerja yang sangat baik dalam mengidentifikasi pembiayaan yang layak (**Recall Approved = 99%**). Namun, terdapat 17 kasus *False Positive* (diprediksi disetujui, namun aktualnya tidak), yang menunjukkan potensi risiko yang perlu dikelola lebih lanjut saat implementasi. Hanya 1 kasus *False Negative* (diprediksi tidak disetujui, namun aktualnya disetujui), yang berarti model sangat konservatif dalam menolak pembiayaan yang sebenarnya layak.

### 3. Faktor Penentu Kelayakan (Feature Importance)

Berdasarkan koefisien model Regresi Logistik, faktor-faktor berikut memiliki pengaruh terbesar terhadap keputusan kelayakan:

| Peringkat | Fitur | Koefisien | Pengaruh terhadap Kelayakan |
| :--- | :--- | :--- | :--- |
| **1** | **Credit_History** | +2.5189 | **Sangat Positif** (Faktor paling dominan) |
| 2 | Property_Area_Semiurban | +0.6199 | Positif |
| 3 | Married_Yes | +0.3356 | Positif |
| 4 | Education_Not Graduate | -0.4666 | Negatif |
| 5 | TotalIncome | -0.000017 | Negatif (walaupun kecil) |

**Implikasi:** Model prototipe ini menegaskan bahwa **Riwayat Kredit** adalah prediktor utama. Dalam konteks LKMS, fitur ini harus diinterpretasikan sebagai **Riwayat Kepatuhan** atau **Karakter Pemohon** (sesuai prinsip syariah), yang dapat diukur dari kepatuhan pembayaran angsuran sebelumnya atau reputasi di komunitas.

## IV. Justifikasi TKT 6 dan Rekomendasi

### Justifikasi TKT 6
Prototipe model AI ini telah mencapai **TKT 6** karena:
1.  **Model Fungsional:** Model telah dikembangkan, dilatih, dan dievaluasi menggunakan data yang relevan.
2.  **Validasi Lingkungan Relevan:** Pengujian dilakukan pada data uji (simulasi lingkungan operasional) dengan metrik kinerja yang terukur (Akurasi 85.37%).
3.  **Siap untuk TKT 7:** Model ini siap untuk diintegrasikan dan didemonstrasikan dalam lingkungan operasional yang sebenarnya (yaitu, di LKMS mitra) untuk validasi lapangan.

### Rekomendasi Lanjutan untuk Proposal SINERGI
1.  **Gunakan Laporan Ini:** Lampirkan laporan teknis ini sebagai bukti bahwa aspek teknis riset telah mencapai TKT 6, memenuhi persyaratan minimal program.
2.  **Amankan Data LKMS:** Gunakan prototipe dan laporan ini sebagai alat negosiasi untuk meyakinkan LKMS agar bersedia menyediakan data historis mereka untuk pengujian TKT 7.
3.  **Finalisasi Kemitraan Dinas:** Segera amankan surat komitmen dari instansi pemerintah setingkat dinas (misalnya, Dinas Koperasi/UKM) untuk memenuhi persyaratan mitra wajib skema Inovasi Sosial.

***

### Referensi

[1] Panduan Program Hilirisasi Riset Prioritas dan Strategis – SINERGI Tahun 2026. (Bab II, C. Skema dan Luaran Program, 1. Inovasi Sosial).
