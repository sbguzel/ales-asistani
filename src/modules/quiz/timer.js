export class ZenTimer {
  constructor(timerElement, targetSeconds = 75, onTick = null) {
    this.element = timerElement;
    this.targetSeconds = targetSeconds;
    this.onTick = onTick;
    this.seconds = 0;
    this.intervalId = null;
    this.startTime = null;
    this.isRunning = false;
    this.reset();
  }

  start(targetSeconds = 75) {
    this.stop();
    this.isRunning = true;
    this.targetSeconds = targetSeconds;
    this.seconds = 0;
    this.startTime = performance.now();
    if (this.element) {
      this.element.classList.remove('idle');
    }
    this.updateDisplay();

    this.intervalId = setInterval(() => {
      this.seconds++;
      this.updateDisplay();
      if (this.onTick) this.onTick(this.seconds);
    }, 1000);
  }

  stop() {
    this.isRunning = false;
    if (this.intervalId) {
      clearInterval(this.intervalId);
      this.intervalId = null;
    }
    const elapsed = this.startTime ? (performance.now() - this.startTime) / 1000 : this.seconds;
    return parseFloat(elapsed.toFixed(1));
  }

  reset() {
    this.stop();
    this.seconds = 0;
    this.startTime = null;
    if (this.element) {
      this.element.classList.add('idle');
      this.element.classList.remove('warning', 'overtime');
    }
    this.updateDisplay();
  }

  updateDisplay() {
    if (!this.element) return;

    const mins = Math.floor(this.seconds / 60);
    const secs = this.seconds % 60;
    const formatted = `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;

    const textEl = this.element.querySelector('.timer-text') || this.element;
    textEl.textContent = formatted;

    // Görsel Zen Renk Durumları (Kesinlikle ses yok)
    this.element.classList.remove('warning', 'overtime');
    if (this.isRunning) {
      if (this.seconds > this.targetSeconds) {
        this.element.classList.add('overtime');
      } else if (this.seconds >= this.targetSeconds * 0.8) {
        this.element.classList.add('warning');
      }
    }
  }
}
