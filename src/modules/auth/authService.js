import {
  signInWithEmailAndPassword,
  createUserWithEmailAndPassword,
  signOut,
  onAuthStateChanged,
  updateProfile,
  setPersistence,
  browserLocalPersistence,
  browserSessionPersistence
} from 'firebase/auth';
import { doc, setDoc, getDoc, serverTimestamp } from 'firebase/firestore';
import { auth, db, APP_CONFIG } from '../../core/config.js';
import { state } from '../../core/state.js';
import { eventBus } from '../../core/eventBus.js';

export class AuthService {
  /**
   * Kullanıcı adını Firebase Auth için geçerli sanal bir e-postaya dönüştürür.
   * Örn: "ahmet_99" -> "user_ahmet_99@ales.internal"
   */
  static formatInternalEmail(username) {
    const clean = username.trim().toLowerCase().replace(/[^a-z0-9_]/g, '');
    if (!clean) throw new Error('Geçersiz kullanıcı adı. Yalnızca harf, rakam ve alt çizgi kullanın.');
    return `user_${clean}${APP_CONFIG.DOMAINS.INTERNAL_EMAIL_SUFFIX}`;
  }

  /**
   * Sanal e-postadan temiz kullanıcı adını ayıklar.
   */
  static extractUsername(email, displayName) {
    if (displayName) return displayName;
    if (!email) return 'Misafir';
    const match = email.match(/^user_([a-z0-9_]+)@/i);
    return match ? match[1] : email.split('@')[0];
  }

  /**
   * Yeni kullanıcı kaydı (Sadece Kullanıcı Adı + Şifre)
   */
  static async register(username, password, rememberMe = true) {
    try {
      const email = this.formatInternalEmail(username);
      if (password.length < 6) {
        throw new Error('Şifre en az 6 karakter olmalıdır.');
      }

      await setPersistence(auth, rememberMe ? browserLocalPersistence : browserSessionPersistence);
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;

      // Kullanıcı adını Firebase profiline ekle
      await updateProfile(user, { displayName: username.trim() });

      // Firestore üzerinde kullanıcı profil dokümanı oluştur
      const userRef = doc(db, 'users', user.uid);
      await setDoc(userRef, {
        userId: user.uid,
        username: username.trim(),
        createdAt: serverTimestamp(),
        settings: {
          theme: 'dark',
          penColor: '#38bdf8',
          penWidth: 2.5,
          showGridLines: false
        }
      });

      const userData = { uid: user.uid, username: username.trim() };
      state.set({ user: userData });
      eventBus.emit('auth:success', userData);
      return userData;
    } catch (error) {
      throw new Error(this.getLocalizedErrorMessage(error));
    }
  }

  /**
   * Giriş yapma (Sadece Kullanıcı Adı + Şifre)
   */
  static async login(username, password, rememberMe = true) {
    try {
      const email = this.formatInternalEmail(username);
      await setPersistence(auth, rememberMe ? browserLocalPersistence : browserSessionPersistence);
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
      const user = userCredential.user;

      const cleanName = this.extractUsername(user.email, user.displayName);
      const userData = { uid: user.uid, username: cleanName };

      state.set({ user: userData });
      eventBus.emit('auth:success', userData);
      return userData;
    } catch (error) {
      throw new Error(this.getLocalizedErrorMessage(error));
    }
  }

  /**
   * Çıkış yapma
   */
  static async logout() {
    try {
      await signOut(auth);
      state.set({ user: null });
      eventBus.emit('auth:logout');
    } catch (error) {
      console.error('[AuthService] Çıkış hatası:', error);
    }
  }

  /**
   * Oturum durumunu dinleme
   */
  static initAuthListener() {
    onAuthStateChanged(auth, async (user) => {
      if (user) {
        const cleanName = this.extractUsername(user.email, user.displayName);
        const userData = { uid: user.uid, username: cleanName };
        state.set({ user: userData });
        eventBus.emit('auth:stateChanged', userData);
      } else {
        state.set({ user: null });
        eventBus.emit('auth:stateChanged', null);
      }
    });
  }

  /**
   * Hata kodlarını sakin Türkçe mesajlara dönüştürür
   */
  static getLocalizedErrorMessage(error) {
    if (error.code) {
      switch (error.code) {
        case 'auth/email-already-in-use':
          return 'Bu kullanıcı adı zaten alınmış. Farklı bir kullanıcı adı deneyin veya giriş yapın.';
        case 'auth/user-not-found':
        case 'auth/wrong-password':
        case 'auth/invalid-credential':
          return 'Kullanıcı adı veya şifre hatalı.';
        case 'auth/weak-password':
          return 'Şifreniz en az 6 karakterden oluşmalıdır.';
        case 'auth/network-request-failed':
          return 'İnternet bağlantınızı kontrol edin.';
        default:
          return error.message || 'Giriş yapılırken bir hata oluştu.';
      }
    }
    return error.message || 'Beklenmeyen bir hata oluştu.';
  }
}
