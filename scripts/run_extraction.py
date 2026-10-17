#!/usr/bin/env python3
"""
ALES Çıkmış Sorular - Otomatik PDF Çıkarma ve İndeksleme Scripti
11 PDF dosyasını okur; soru metinlerini, gömülü formül/şekil PNG'lerini ve cevap anahtarlarını ayıklar.
"""

import sys
import glob
import json
import time
from pathlib import Path
from pipeline.pdf_extractor import PDFExtractor

def main():
    start_time = time.time()
    pdf_dir = Path("ales_cikmis_sorular")
    pdf_files = sorted(pdf_dir.glob("*.pdf"))

    if not pdf_files:
        print(f"[Hata] '{pdf_dir}' dizininde hiçbir PDF dosyası bulunamadı!")
        sys.exit(1)

    print("=" * 70)
    print("🎯 ALES ASİSTANI - ÇIKMIŞ SORU AYIKLAMA PİPELİNE'I")
    print(f"Toplam PDF Sayısı: {len(pdf_files)}")
    print("=" * 70)

    extractor = PDFExtractor(output_dir="scripts/output")
    summary = {
        "total_exams": len(pdf_files),
        "total_questions_extracted": 0,
        "total_sayisal": 0,
        "total_sozel": 0,
        "total_images_extracted": 0,
        "exams": []
    }

    for idx, pdf_path in enumerate(pdf_files, 1):
        print(f"\n[{idx}/{len(pdf_files)}] {pdf_path.name} ayrıştırılıyor...")
        exam_result = extractor.extract_exam(str(pdf_path))

        sayisal_count = len(exam_result["sections"]["sayisal"])
        sozel_count = len(exam_result["sections"]["sozel"])
        
        # Soru başına görselleri topla
        img_count = sum(len(q.get("images", [])) for q in exam_result["sections"]["sayisal"]) + \
                    sum(len(q.get("images", [])) for q in exam_result["sections"]["sozel"])

        summary["total_sayisal"] += sayisal_count
        summary["total_sozel"] += sozel_count
        summary["total_questions_extracted"] += (sayisal_count + sozel_count)
        summary["total_images_extracted"] += img_count

        summary["exams"].append({
            "filename": pdf_path.name,
            "exam_stem": pdf_path.stem,
            "metadata": exam_result.get("metadata", {}),
            "sayisal_questions": sayisal_count,
            "sozel_questions": sozel_count,
            "images_extracted": img_count
        })

    # Genel özet dosyasını kaydet
    summary_path = Path("scripts/output/summary_index.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    elapsed = round(time.time() - start_time, 2)
    print("\n" + "=" * 70)
    print("✅ AYIKLAMA TAMAMLANDI!")
    print(f"İşlem Süresi: {elapsed} saniye")
    print(f"Toplam Sınav: {summary['total_exams']}")
    print(f"Toplam Çıkarılan Soru: {summary['total_questions_extracted']} (Sayısal: {summary['total_sayisal']}, Sözel: {summary['total_sozel']})")
    print(f"Toplam Çıkarılan Görsel/Şekil: {summary['total_images_extracted']}")
    print(f"Özet Dosyası: {summary_path}")
    print("=" * 70)

if __name__ == "__main__":
    main()
