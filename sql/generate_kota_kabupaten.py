#!/usr/bin/env python3
"""
Script untuk generate SQL insert untuk semua kota/kabupaten di Indonesia
"""

# List semua kota/kabupaten di Indonesia
kota_kabupaten = [
    # ACEH
    "ACEH BARAT", "ACEH BARAT DAYA", "ACEH BESAR", "ACEH JAYA", "ACEH SELATAN", 
    "ACEH SINGKIL", "ACEH TAMIANG", "ACEH TENGAH", "ACEH TENGGARA", "ACEH TIMUR", 
    "ACEH UTARA", "BANDA ACEH", "LANGSa", "LHOKSEUMAWE", "SABANG", "SUBULUSSALAM",
    
    # SUMATERA UTARA
    "AGAM", "ASAHAN", "BATUBARA", "DAIRI", "DELI SERDANG", "HUMBANG HASUNDUTAN",
    "KARO", "LABUHANBATU", "LABUHANBATU SELATAN", "LABUHANBATU UTARA", "LANGKAT",
    "MANDAILING NATAL", "NIAS", "NIAS BARAT", "NIAS SELATAN", "NIAS UTARA",
    "PADANG LAWAS", "PADANG LAWAS UTARA", "PAKPAK BHARAT", "SAMOSIR",
    "SERDANG BEDAGAI", "SIMALUNGUN", "TAPANULI SELATAN", "TAPANULI TENGAH",
    "TAPANULI UTARA", "TOBA", "TOBA SAMOSIR", "BINJAI", "GUNUNGSITOLI", "MEDAN",
    "PADANG SIDEMPUAN", "PEMATANG SIANTAR", "SIBOLGA", "TANJUNG BALAI", "TEBING TINGGI",
    
    # SUMATERA BARAT
    "DHARMASRAYA", "KEPULAUAN MENTAWAI", "LIMA PULUH KOTA", "PADANG PARIAMAN",
    "PASAMAN", "PASAMAN BARAT", "PESISIR SELATAN", "SIJUNJUNG", "SOLOK",
    "SOLOK SELATAN", "TANAH DATAR", "BUKITTINGGI", "PADANG", "PADANG PANJANG",
    "PARIAMAN", "PAYAKUMBUH", "SAWAH LUNTO", "SOLOK",
    
    # RIAU
    "BENGKALIS", "INDRAGIRI HILIR", "INDRAGIRI HULU", "KAMPAR", "KEPULAUAN ANAMBAS",
    "KEPULAUAN MERANTI", "KUANTAN SINGINGI", "PELALAWAN", "ROKAN HILIR", "ROKAN HULU",
    "SIAK", "DUMAI", "PEKANBARU",
    
    # KEPULAUAN RIAU
    "BINTAN", "KARIMUN", "KEPULAUAN ANAMBAS", "LINGGA", "NATUNA", "BATAM", "TANJUNG PINANG",
    
    # JAMBI
    "BUNGO", "KERINCI", "MERANGIN", "MUARO JAMBI", "SAROLANGUN", "TANJUNG JABUNG BARAT",
    "TANJUNG JABUNG TIMUR", "TEBO", "JAMBI", "SUNGAIPENUH",
    
    # SUMATERA SELATAN
    "BANYUASIN", "EMPAT LAWANG", "LAHAT", "MUARA ENIM", "MUSI BANYUASIN", "MUSI RAWAS",
    "MUSI RAWAS UTARA", "OGAN ILIR", "OGAN KOMERING ILIR", "OGAN KOMERING ULU",
    "OGAN KOMERING ULU SELATAN", "OGAN KOMERING ULU TIMUR", "PENUKAL ABAB LEMATANG ILIR",
    "PALEMBANG", "PRABUMULIH",
    
    # BENGKULU
    "BENGKULU", "BENGKULU SELATAN", "BENGKULU TENGAH", "BENGKULU UTARA", "KAUR",
    "KEPAHIANG", "LEBONG", "MUKO MUKO", "REJANG LEBONG", "SELUMA",
    
    # LAMPUNG
    "LAMPUNG BARAT", "LAMPUNG SELATAN", "LAMPUNG TENGAH", "LAMPUNG TIMUR", "LAMPUNG UTARA",
    "MESUJI", "PESAWARAN", "PESISIR BARAT", "PRINGSEWU", "TULANG BAWANG",
    "TULANG BAWANG BARAT", "WAY KANAN", "BANDAR LAMPUNG", "METRO",
    
    # BANGKA BELITUNG
    "BANGKA", "BANGKA BARAT", "BANGKA SELATAN", "BANGKA TENGAH", "BELITUNG",
    "BELITUNG TIMUR", "PANGKAL PINANG",
    
    # DKI JAKARTA
    "JAKARTA BARAT", "JAKARTA PUSAT", "JAKARTA SELATAN", "JAKARTA TIMUR", "JAKARTA UTARA",
    "KEPULAUAN SERIBU",
    
    # JAWA BARAT
    "BANDUNG", "BANDUNG BARAT", "BEKASI", "BOGOR", "CIAMIS", "CIANJUR", "CILACAP",
    "CIREBON", "GARUT", "INDRAMAYU", "KARAWANG", "KUNINGAN", "MAJALENGKA", "PANGANDARAN",
    "PURWAKARTA", "SUBANG", "SUKABUMI", "SUMEDANG", "TASIKMALAYA", "BANJAR", "BANDUNG",
    "BEKASI", "BOGOR", "CIMAHI", "CIREBON", "DEPOK", "SUKABUMI", "TASIKMALAYA",
    
    # JAWA TENGAH
    "BANJARNEGARA", "BANYUMAS", "BATANG", "BLORA", "BOYOLALI", "BREBES", "CILACAP",
    "DEMAK", "GROBOGAN", "JEPARA", "KARANGANYAR", "KEBUMEN", "KENDAL", "KLATEN",
    "KUDUS", "MAGELANG", "PATI", "PEKALONGAN", "PEMALANG", "PURBALINGGA", "PURWOREJO",
    "REMBANG", "SEMARANG", "SRAGEN", "SUKOHARJO", "TEMANGGUNG", "WONOGIRI", "WONOSOBO",
    "MAGELANG", "PEKALONGAN", "SALATIGA", "SEMARANG", "SURAKARTA", "TEGAL",
    
    # DI YOGYAKARTA
    "BANTUL", "GUNUNG KIDUL", "KULON PROGO", "SLEMAN", "YOGYAKARTA",
    
    # JAWA TIMUR
    "BANGKALAN", "BANYUWANGI", "BLITAR", "BOJONEGORO", "BONDOWOSO", "GRESIK", "JEMBER",
    "JOMBANG", "KEDIRI", "LAMONGAN", "LUMAJANG", "MADIUN", "MAGETAN", "MALANG",
    "MOJOKERTO", "NGAWI", "PACITAN", "PAMEKASAN", "PASURUAN", "PONOROGO", "PROBOLINGGO",
    "SAMPANG", "SIDOARJO", "SITUBONDO", "SUMENEP", "TRENGGALEK", "TUBAN", "TULUNGAGUNG",
    "BATU", "BLITAR", "KEDIRI", "MADIUN", "MALANG", "MOJOKERTO", "PASURUAN", "PROBOLINGGO",
    "SURABAYA",
    
    # BANTEN
    "LEBAK", "PANDEGLANG", "SERANG", "TANGERANG", "CILEGON", "SERANG", "TANGERANG",
    "TANGERANG SELATAN",
    
    # BALI
    "BADUNG", "BANGLI", "BULELENG", "GIANYAR", "JEMBRANA", "KARANGASEM", "KLUNGKUNG",
    "TABANAN", "DENPASAR",
    
    # NUSA TENGGARA BARAT
    "BIMA", "DOMPU", "LOMBOK BARAT", "LOMBOK TENGAH", "LOMBOK TIMUR", "LOMBOK UTARA",
    "SUMBAWA", "SUMBAWA BARAT", "BIMA", "MATARAM",
    
    # NUSA TENGGARA TIMUR
    "ALOR", "BELU", "ENDE", "FLORES TIMUR", "KUPANG", "LEMBATA", "MALAKA", "MANGGARAI",
    "MANGGARAI BARAT", "MANGGARAI TIMUR", "NAGEKEO", "NGADA", "ROTE NDAO", "SABU RAIJUA",
    "SIKKA", "SUMBA BARAT", "SUMBA BARAT DAYA", "SUMBA TENGAH", "SUMBA TIMUR", "TIMOR TENGAH SELATAN",
    "TIMOR TENGAH UTARA", "KUPANG",
    
    # KALIMANTAN BARAT
    "BENGKAYANG", "KAPUAS HULU", "KAYONG UTARA", "KETAPANG", "KUBU RAYA", "LANDAK",
    "MELAWI", "MEMPAWAH", "SAMBAS", "SANGGAU", "SINTANG", "PONTIANAK", "SINGKAWANG",
    
    # KALIMANTAN TENGAH
    "BARITO SELATAN", "BARITO TIMUR", "BARITO UTARA", "GUNUNG MAS", "KAPUAS", "KATINGAN",
    "KOTAWARINGIN BARAT", "KOTAWARINGIN TIMUR", "LAMANDAU", "MURUNG RAYA", "PULANG PISAU",
    "SUKAMARA", "SERUYAN", "PALANGKARAYA",
    
    # KALIMANTAN SELATAN
    "BALANGAN", "BANJAR", "BARITO KUALA", "HULU SUNGAI SELATAN", "HULU SUNGAI TENGAH",
    "HULU SUNGAI UTARA", "KOTABARU", "TABALONG", "TANAH BUMBU", "TANAH LAUT", "TAPIN",
    "BANJARBARU", "BANJARMASIN",
    
    # KALIMANTAN TIMUR
    "BERAU", "KUTAI BARAT", "KUTAI KARTANEGARA", "KUTAI TIMUR", "MAHAKAM ULU", "PASER",
    "PENAJAM PASER UTARA", "BALIKPAPAN", "BONTANG", "SAMARINDA", "TARAKAN",
    
    # KALIMANTAN UTARA
    "BULUNGAN", "MALINAU", "NUNUKAN", "TANA TIDUNG",
    
    # SULAWESI UTARA
    "BOLAANG MONGONDOW", "BOLAANG MONGONDOW SELATAN", "BOLAANG MONGONDOW TIMUR",
    "BOLAANG MONGONDOW UTARA", "KEPULAUAN SANGIHE", "KEPULAUAN SIAU TAGULANDANG BIARO (SITARO)",
    "KEPULAUAN TALAUD", "MINAHASA", "MINAHASA SELATAN", "MINAHASA TENGGARA", "MINAHASA UTARA",
    "BITUNG", "KOTAMOBAGU", "MANADO", "TOMOHON",
    
    # SULAWESI TENGAH
    "BANGGAI", "BANGGAI KEPULAUAN", "BANGGAI LAUT", "BUOL", "DONGGALA", "MOROWALI",
    "MOROWALI UTARA", "PALI", "PARIGI MOUTONG", "POSO", "SIGI", "TOJO UNA-UNA", "TOLI TOLI",
    "PALU",
    
    # SULAWESI SELATAN
    "BANTAENG", "BARRU", "BONE", "BULUKUMBA", "ENREKANG", "GOWA", "JENEPONTO", "KEPULAUAN SELAYAR",
    "LUWU", "LUWU TIMUR", "LUWU UTARA", "MAROS", "PANGKAJENE KEPULAUAN", "PINRANG", "SIDENRENG RAPPANG",
    "SINJAI", "SOPPENG", "TAKALAR", "TANA TORAJA", "TORAJA UTARA", "WAJO", "MAKASSAR", "PALOPO",
    "PAREPARE",
    
    # SULAWESI TENGGARA
    "BOMBANA", "BUTON", "BUTON SELATAN", "BUTON TENGAH", "BUTON UTARA", "KOLAKA", "KOLAKA TIMUR",
    "KOLAKA UTARA", "KONAWE", "KONAWE KEPULAUAN", "KONAWE SELATAN", "KONAWE UTARA", "MUNA",
    "MUNA BARAT", "WAKATOBI", "KENDARI", "BAU BAU",
    
    # SULAWESI BARAT
    "MAMASA", "MAMUJU", "MAMUJU TENGAH", "MAMUJU UTARA", "PASANGKAYU", "POLEWALI MANDAR",
    
    # GORONTALO
    "BOALEMO", "BONE BOLANGO", "GORONTALO", "GORONTALO UTARA", "POHUWATO", "GORONTALO",
    
    # MALUKU
    "BURU", "BURU SELATAN", "KEPULAUAN ARU", "KEPULAUAN TANIMBAR", "KEPULAUAN YAPEN",
    "MALUKU BARAT DAYA", "MALUKU TENGAH", "MALUKU TENGGARA", "MALUKU TENGGARA BARAT",
    "SERAM BAGIAN BARAT", "SERAM BAGIAN TIMUR", "AMBON", "TERNATE", "TIDORE KEPULAUAN",
    
    # MALUKU UTARA
    "HALMAHERA BARAT", "HALMAHERA SELATAN", "HALMAHERA TENGAH", "HALMAHERA TIMUR",
    "HALMAHERA UTARA", "KEPULAUAN SULA", "PULAU MOROTAI", "PULAU TALIABU", "TERNATE",
    "TIDORE KEPULAUAN",
    
    # PAPUA BARAT
    "FAK FAK", "KAIMANA", "MANOKWARI", "MANOKWARI SELATAN", "PEGUNUNGAN ARFAK", "SORONG",
    "SORONG SELATAN", "TAMBRAUW", "TELUK BINTUNI", "TELUK WONDAMA", "SORONG",
    
    # PAPUA
    "ASMAT", "BIAK NUMFOR", "BOVEN DIGOEL", "DEIYAI", "DOGIYAI", "INTAN JAYA", "JAYAPURA",
    "JAYAWIJAYA", "KEEROM", "KEPULAUAN YAPEN", "LANNY JAYA", "MAMBERAMO RAYA", "MAMBERAMO TENGAH",
    "MAPPI", "MERAUKE", "MIMIKA", "NABIRE", "NDUGA", "PEGUNUNGAN BINTANG", "PUNCAK",
    "PUNCAK JAYA", "SARMI", "SUPIORI", "TOLIKARA", "WAROPEN", "YAHUKIMO", "YALIMO",
    "JAYAPURA"
]

def generate_sql():
    """Generate SQL insert statements"""
    sql_statements = []
    seen_combinations = set()
    
    for kota in kota_kabupaten:
        kota_lower = kota.lower()
        
        # Insert 4 aliases for each kota/kabupaten, avoiding duplicates
        combinations = [
            (kota_lower, kota_lower, 'FALSE'),
            (kota_lower, f'kabupaten {kota_lower}', 'TRUE'),
            (kota_lower, f'kab {kota_lower}', 'TRUE'),
            (kota_lower, f'kota {kota_lower}', 'TRUE')
        ]
        
        for name, keyword, is_alias in combinations:
            key = (name, keyword)
            if key not in seen_combinations:
                seen_combinations.add(key)
                sql_statements.append(f"('{name}', '{keyword}', {is_alias}),")
    
    return sql_statements

if __name__ == "__main__":
    sql_statements = generate_sql()
    
    # Write to file
    with open('insert_kota_kabupaten_full.sql', 'w') as f:
        f.write("-- =====================================================\n")
        f.write("-- INSERT KOTA/KABUPATEN LENGKAP INDONESIA\n")
        f.write("-- =====================================================\n")
        f.write("-- Script ini berisi semua kota dan kabupaten di Indonesia\n")
        f.write("-- dengan berbagai alias untuk keyword matching\n\n")
        
        f.write("-- Clear existing data\n")
        f.write("DELETE FROM kabupaten_kota_keywords;\n\n")
        
        f.write("-- Insert semua kota/kabupaten dengan 4 alias masing-masing\n")
        f.write("INSERT INTO kabupaten_kota_keywords (kabupaten_kota_name, keyword, is_alias) VALUES\n")
        
        for i, statement in enumerate(sql_statements):
            if i == len(sql_statements) - 1:
                f.write(f"    {statement[:-1]};\n")  # Remove comma for last statement
            else:
                f.write(f"    {statement}\n")
        
        f.write("\n-- Verifikasi hasil insert\n")
        f.write("SELECT 'Kota/Kabupaten yang ditambahkan:' as info;\n")
        f.write("SELECT kabupaten_kota_name, COUNT(*) as keyword_count \n")
        f.write("FROM kabupaten_kota_keywords \n")
        f.write("GROUP BY kabupaten_kota_name \n")
        f.write("ORDER BY kabupaten_kota_name;\n")
    
    print(f"Generated SQL file with {len(kota_kabupaten)} kota/kabupaten")
    print(f"Total keywords: {len(kota_kabupaten) * 4}")
