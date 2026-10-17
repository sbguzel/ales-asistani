import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import { initializeApp } from 'firebase/app';
import { 
  getFirestore, 
  collection, 
  doc, 
  writeBatch, 
  getDocs, 
  serverTimestamp 
} from 'firebase/firestore';

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
  storageBucket: env.VITE_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: env.VITE_FIREBASE_MESSAGING_SENDER_ID,
  appId: env.VITE_FIREBASE_APP_ID,
  measurementId: env.VITE_FIREBASE_MEASUREMENT_ID
};

console.log('🚀 Firebase Firestore Soru Senkronizasyonu Başlatılıyor...');
console.log(`📌 Hedef Proje: ${firebaseConfig.projectId}`);

const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

async function seedQuestions() {
  const seedFile = path.join(rootDir, 'public/data/seed_questions.json');
  if (!fs.existsSync(seedFile)) {
    console.error('❌ Soru veri dosyası bulunamadı:', seedFile);
    process.exit(1);
  }

  const questions = JSON.parse(fs.readFileSync(seedFile, 'utf-8'));
  console.log(`📚 Yüklenecek Soru Sayısı: ${questions.length}`);

  const questionsCol = collection(db, 'questions');
  const batch = writeBatch(db);

  questions.forEach((q, index) => {
    const qDocRef = doc(questionsCol, q.id);
    const dataToSave = {
      ...q,
      orderIndex: index + 1,
      updatedAt: serverTimestamp()
    };
    batch.set(qDocRef, dataToSave, { merge: true });
  });

  console.log('⏳ Firestore Toplu Yazma (Batch) İşlemi Gönderiliyor...');
  await batch.commit();
  console.log('✅ Tüm sorular Firestore "questions" koleksiyonuna başarıyla yüklendi!');

  // Doğrulama: Koleksiyonu oku ve doğrula
  console.log('🔍 Doğrulama yapılıyor...');
  const snapshot = await getDocs(questionsCol);
  console.log(`📊 Firestore'daki Güncel Toplam Soru Sayısı: ${snapshot.size}`);

  const subjects = {};
  snapshot.forEach(docSnap => {
    const data = docSnap.data();
    subjects[data.subject] = (subjects[data.subject] || 0) + 1;
  });
  console.log('📌 Branş Dağılımı:', subjects);

  process.exit(0);
}

seedQuestions().catch(err => {
  console.error('❌ Hata oluştu:', err);
  process.exit(1);
});
