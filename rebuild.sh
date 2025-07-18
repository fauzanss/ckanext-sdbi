#!/bin/bash

# Script untuk update SDBI extension di CKAN
# Jalankan dengan: ./update_sdbi.sh

echo "�� Memulai update SDBI extension..."

# Cek apakah container CKAN berjalan
if ! docker ps | grep -q "ckan"; then
    echo "❌ Container CKAN tidak berjalan. Jalankan docker-compose up -d terlebih dahulu."
    exit 1
fi

echo "📦 Building CKAN container (dengan no-cache)..."
if docker-compose build --no-cache ckan; then
    echo "✅ Build CKAN berhasil!"
else
    echo "❌ Build CKAN gagal!"
    exit 1
fi

echo "🔄 Restarting CKAN container..."
if docker-compose up -d ckan; then
    echo "✅ CKAN container berhasil di-restart!"
else
    echo "❌ Restart CKAN gagal!"
    exit 1
fi

echo ""
echo "🎉 Update SDBI selesai!"
echo "�� CKAN dapat diakses di: http://localhost:8080"
echo ""
echo "💡 Tips:"
echo "   - Pastikan sudah push perubahan ke repository SDBI"
echo "   - Clear browser cache jika perubahan tidak muncul"
echo "   - Check logs jika ada error: docker-compose logs ckan"