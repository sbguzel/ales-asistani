import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { initializeApp } from 'firebase/app';
import { getStorage, ref, uploadBytes, getDownloadURL } from 'firebase/storage';
import { getFirestore, doc, updateDoc } from 'firebase/firestore';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const rootDir = path.resolve(__dirname, '../../');

// .env dosyasını oku
const envPath = path.join(rootDir, '.env');
if (!fs.existsSync(envPath)) {
  console.error('❌ .env dosyası bulunamadı:', envPath);
  process.exit(1);
}

const envContent = fs.readFileSync(envPath, 'utf-8');
const env = {};
envContent.split('\n').forEach(line => {
  const trimmed = line.trim();
  if (trimmed && !trimmed.startsWith('#')) {
    const idx = trimmed.indexOf('=');
    if (idx !== -1) {
      const k = trimmed.substring(0, idx).trim();
      const v = trimmed.substring(idx + 1).trim();
      env[k] = v;
    }
  }
});

const firebaseConfig = {
  apiKey: env.VITE_FIREBASE_API_KEY,
  authDomain: env.VITE_FIREBASE_AUTH_DOMAIN,
  projectId: env.VITE_FIREBASE_PROJECT_ID,
  storageBucket: env.VITE_FIREBASE_STORAGE_BUCKET || 'ales-asistani.firebasestorage.app',
  messagingSenderId: env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: env.VITE_FIREBASE_APP_ID,
  measurementId: env.VITE_FIREBASE_MEASUREMENT_ID
};

console.log('🚀 Firebase Storage Görsel Senkronizasyonu Başlatılıyor...');
console.log(`📌 Hedef Bucket: ${firebaseConfig.storageBucket}`);

const app = initializeApp(firebaseConfig);
const storage = getStorage(app);
const db = getFirestore(app);

// Dosya eşleştirmesi: Soru ID -> Dosya Adı
const fileQuestionMap = {
  'geo_ucgen_aci_q44.svg': '2021_ales1_mat_44',
  'geo_ucgen_alan_q45.svg': '2021_ales1_mat_45',
  'geo_kare_alan_q46.svg': '2021_ales1_mat_46',
  'geo_dikdortgen_oran_q47.svg': '2021_ales1_mat_47',
  'geo_cember_yarim_q48.svg': '2021_ales1_mat_48',
};

async function uploadAssets() {
  const svgDir = path.join(rootDir, 'public/assets/questions/svg');
  if (!fs.existsSync(svgDir)) {
    console.error('❌ SVG dizini bulunamadı:', svgDir);
    process.exit(1);
  }

  const files = fs.readdirSync(svgDir).filter(f => f.endsWith('.svg'));
  console.log(`📂 Bulunan SVG Dosyası: ${files.length}`);

  const seedPath = path.join(rootDir, 'public/data/seed_questions.json');
  let questions = [];
  if (fs.existsSync(seedPath)) {
    questions = JSON.parse(fs.readFileSync(seedPath, 'utf-8'));
  }

  const uploadedUrls = {};
  let totalBytesUploaded = 0;

  for (const file of files) {
    const filePath = path.join(svgDir, file);
    const fileBuffer = fs.readFileSync(filePath);
    const fileSizeKB = (fileBuffer.length / 1024).toFixed(2);
    totalBytesUploaded += fileBuffer.length;

    console.log(`\n⏳ Yükleniyor: ${file} (${fileSizeKB} KB)...`);

    // Storage hedef referansı (örneğin questions/svg/geo_kare_alan_q46.svg)
    const storageRef = ref(storage, `questions/svg/${file}`);

    // Uzun süreli önbellekleme (Cache-Control) ile ücretsiz bant genişliği korunur
    const metadata = {
      contentType: 'image/svg+xml',
      cacheControl: 'public, max-age=31536000, immutable'
    };

    await uploadBytes(storageRef, fileBuffer, metadata);
    const downloadUrl = await getDownloadURL(storageRef);

    console.log(`✅ Yüklendi!`);
    console.log(`🔗 URL: ${downloadUrl}`);

    uploadedUrls[file] = downloadUrl;

    // İlgili Soru ID'sini bul ve güncelle
    const questionId = fileQuestionMap[file];
    if (questionId) {
      // 1. seed_questions.json içindeki veriyi güncelle
      const qIndex = questions.findIndex(q => q.id === questionId);
      if (qIndex !== -1) {
        questions[qIndex].imageUrl = downloadUrl;
      }

      // 2. Firestore'daki ilgili dokümanı güncelle
      try {
        const qDocRef = doc(db, 'questions', questionId);
        await updateDoc(qDocRef, {
          imageUrl: downloadUrl
        });
        console.log(`📝 Firestore dokümanı güncellendi: ${questionId}`);
      } catch (err) {
        console.warn(`⚠️ Firestore dokümanı güncellenirken hata: ${err.message}`);
      }
    }
  }

  // seed_questions.json dosyasını kaydet
  fs.writeFileSync(seedPath, JSON.stringify(questions, null, 2), 'utf-8');
  console.log('\n💾 public/data/seed_questions.json güncellendi.');

  const totalKB = (totalBytesUploaded / 1024).toFixed(2);
  console.log(`\n🎉 Tüm dosyalar başarıyla yüklendi!`);
  console.log(`📊 Toplam Yüklenen Boyut: ${totalKB} KB (Firebase Spark 5 GB kotasının %${((totalBytesUploaded / (5 * 1024 * 1024 * 1024)) * 100).toFixed(6)}'sı)`);
  console.log(`🚀 Tarayıcı önbellekleme aktif (1 yıl) — kota kullanımı minimum seviyededir.`);

  process.exit(0);
}

uploadAssets().catch(err => {
  console.error('❌ Yükleme hatası:', err);
  process.exit(1);
});
