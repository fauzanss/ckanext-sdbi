#!/bin/bash

# =====================================================
# SCRIPT UNTUK MENJALANKAN SQL SCRIPTS
# =====================================================
# Script ini memudahkan menjalankan SQL scripts untuk keyword management

echo "=========================================="
echo "SQL SCRIPTS RUNNER"
echo "=========================================="
echo ""

# Function untuk menjalankan SQL script
run_sql() {
    local script_name=$1
    local description=$2
    
    echo "Menjalankan: $description"
    echo "Script: $script_name"
    echo "----------------------------------------"
    
    # Copy script ke container
    podman cp "$script_name" db:/tmp/
    
    # Execute script
    podman exec db psql -U ckan -d ckan -f "/tmp/$script_name"
    
    echo "✅ $description selesai!"
    echo ""
}

# Menu pilihan
echo "Pilih script yang akan dijalankan:"
echo "1. Setup awal (create tables)"
echo "2. Insert keywords baru"
echo "3. Insert contoh keywords"
echo "4. Insert kementerian & lembaga lengkap"
echo "5. Insert kota/kabupaten lengkap (504 kota)"
echo "6. Jalankan semua (setup + insert)"
echo "7. Test query statistik"
echo "8. Keluar"
echo ""

read -p "Masukkan pilihan (1-8): " choice

case $choice in
    1)
        run_sql "create_keyword_tables.sql" "Setup awal - Membuat tabel keywords"
        ;;
    2)
        run_sql "insert_keywords.sql" "Insert keywords baru"
        ;;
    3)
        run_sql "add_keyword_examples.sql" "Insert contoh keywords"
        ;;
    4)
        run_sql "insert_kementerian_lembaga.sql" "Insert kementerian & lembaga lengkap"
        ;;
    5)
        run_sql "insert_kota_kabupaten_full.sql" "Insert kota/kabupaten lengkap (504 kota)"
        ;;
    6)
        run_sql "create_keyword_tables.sql" "Setup awal - Membuat tabel keywords"
        run_sql "insert_keywords.sql" "Insert keywords baru"
        ;;
    7)
        echo "Menjalankan test query statistik..."
        echo "----------------------------------------"
        podman exec db psql -U ckan -d ckan -c "
        WITH dataset_text AS (
            SELECT 
                name,
                title,
                notes,
                LOWER(CONCAT(title, ' ', COALESCE(notes, ''))) as full_text
            FROM package 
            WHERE state = 'active' AND private = false
        ),
        provinsi_matches AS (
            SELECT DISTINCT pk.provinsi_name
            FROM dataset_text dt
            JOIN provinsi_keywords pk ON dt.full_text LIKE '%' || pk.keyword || '%'
        ),
        kabupaten_kota_matches AS (
            SELECT DISTINCT kkk.kabupaten_kota_name
            FROM dataset_text dt
            JOIN kabupaten_kota_keywords kkk ON dt.full_text LIKE '%' || kkk.keyword || '%'
        ),
        kementerian_matches AS (
            SELECT DISTINCT kk.kementerian_name
            FROM dataset_text dt
            JOIN kementerian_keywords kk ON dt.full_text LIKE '%' || kk.keyword || '%'
        )
        SELECT 
            'Statistik Terbaru:' as info,
            (SELECT COUNT(*) FROM provinsi_matches) as provinsi_count,
            (SELECT COUNT(*) FROM kabupaten_kota_matches) as kabupaten_kota_count,
            (SELECT COUNT(*) FROM kementerian_matches) as kementerian_count;
        "
        echo "✅ Test query selesai!"
        ;;
    8)
        echo "Keluar dari script runner."
        exit 0
        ;;
    *)
        echo "❌ Pilihan tidak valid!"
        exit 1
        ;;
esac

echo ""
echo "=========================================="
echo "SCRIPT RUNNER SELESAI!"
echo "=========================================="
echo ""
echo "Silakan cek di http://localhost:8080 untuk melihat hasilnya!"
echo ""
echo "Untuk menjalankan script lagi, jalankan:"
echo "./run_sql_scripts.sh"
