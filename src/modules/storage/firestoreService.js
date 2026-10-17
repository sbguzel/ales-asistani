import { collection, addDoc, serverTimestamp, query, where, getDocs, orderBy, limit } from 'firebase/firestore';
import { db } from '../../core/config.js';
import { state } from '../../core/state.js';

export class FirestoreService {
  /**
   * Soru çözüm denemesini (attempt) Firestore'a veya yerel depoya kaydeder
   */
  static async saveAttempt({ questionId, category, selectedOption, isCorrect, timeSpentSeconds, targetTimeSec, usedCanvas }) {
    const user = state.get().user;
    const attemptData = {
      userId: user ? user.uid : 'anonymous',
      questionId,
      category,
      selectedOption,
      isCorrect,
      timeSpentSeconds,
      targetTimeSec,
      usedCanvas: !!usedCanvas,
      timestamp: new Date().toISOString()
    };

    // 1. Önce daima yerel hafızaya (Cache-First) yazarak çevrimdışı çalışmayı garantiye al
    try {
      const localAttempts = JSON.parse(localStorage.getItem('ales_attempts') || '[]');
      localAttempts.push(attemptData);
      localStorage.setItem('ales_attempts', JSON.stringify(localAttempts));
    } catch (e) {
      console.warn('LocalStorage save error:', e);
    }

    // 2. Kullanıcı oturum açmışsa Firestore'a asenkron gönder
    if (user && user.uid) {
      try {
        const attemptsCol = collection(db, 'user_attempts');
        await addDoc(attemptsCol, {
          ...attemptData,
          createdAt: serverTimestamp()
        });
      } catch (err) {
        console.warn('[FirestoreService] Firestore senkronizasyon gecikmesi:', err);
      }
    }

    return attemptData;
  }

  /**
   * Kullanıcının geçmiş yanlış yaptığı soruları (Hata Defteri) getirir
   */
  static getMistakeQuestionIds() {
    try {
      const localAttempts = JSON.parse(localStorage.getItem('ales_attempts') || '[]');
      const mistakes = new Set();
      localAttempts.forEach(att => {
        if (!att.isCorrect) mistakes.add(att.questionId);
        else mistakes.delete(att.questionId); // Sonradan doğru çözdüyse hata defterinden düşür
      });
      return Array.from(mistakes);
    } catch (e) {
      return [];
    }
  }

  /**
   * İstatistikleri hesaplar (Toplam çözülen, Doğru, Yanlış, Başarı % ve Ort. Süre)
   */
  static getLocalStats() {
    try {
      const attempts = JSON.parse(localStorage.getItem('ales_attempts') || '[]');
      const total = attempts.length;
      if (total === 0) {
        return { total: 0, correct: 0, wrong: 0, accuracy: 0, avgTime: 0 };
      }
      const correct = attempts.filter(a => a.isCorrect).length;
      const wrong = total - correct;
      const accuracy = Math.round((correct / total) * 100);
      const totalTime = attempts.reduce((acc, curr) => acc + (curr.timeSpentSeconds || 0), 0);
      const avgTime = Math.round(totalTime / total);

      return { total, correct, wrong, accuracy, avgTime };
    } catch (e) {
      return { total: 0, correct: 0, wrong: 0, accuracy: 0, avgTime: 0 };
    }
  }
}
