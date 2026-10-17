import { eventBus } from './eventBus.js';

class State {
  constructor() {
    this._state = {
      user: null, // { uid, username }
      theme: localStorage.getItem('ales_theme') || 'dark',
      currentQuestion: null,
      questionIndex: 0,
      totalQuestions: 0,
      selectedOption: null,
      isAnswerEvaluated: false,
      timer: {
        seconds: 0,
        isRunning: false,
        targetTime: 75
      },
      canvas: {
        penColor: '#38bdf8',
        penWidth: 2.5,
        isEraser: false,
        showGrid: false
      },
      activeTab: 'quiz', // 'quiz' | 'stats' | 'mistakes'
      studyMode: 'all',  // 'all' | 'matematik' | 'turkce' | 'mantik' | 'mistakes'
      stats: {
        attempts: []
      }
    };

    this._listeners = new Set();
  }

  get() {
    return this._state;
  }

  set(partialState) {
    this._state = { ...this._state, ...partialState };
    eventBus.emit('state:changed', this._state);
    this._notifyListeners();
  }

  subscribe(listener) {
    this._listeners.add(listener);
    listener(this._state);
    return () => this._listeners.delete(listener);
  }

  _notifyListeners() {
    this._listeners.forEach(fn => fn(this._state));
  }
}

export const state = new State();
