import { HistoryManager } from './historyManager.js';
import { state } from '../../core/state.js';

export class CanvasManager {
  constructor(canvasElement, containerElement) {
    this.canvas = canvasElement;
    this.container = containerElement;
    this.ctx = canvasElement.getContext('2d');
    this.history = new HistoryManager(15);

    this.isDrawing = false;
    this.lastX = 0;
    this.lastY = 0;
    this.showGrid = false;
    this.dpr = window.devicePixelRatio || 1;

    this.init();
  }

  init() {
    this.resize();
    window.addEventListener('resize', () => this.resize());
    this.attachPointerEvents();
  }

  resize() {
    const rect = this.container.getBoundingClientRect();
    const width = rect.width;
    const height = rect.height;

    // Önceki çizimi yedekle
    let prevImage = null;
    if (this.canvas.width > 0 && this.canvas.height > 0) {
      prevImage = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);
    }

    this.dpr = window.devicePixelRatio || 1;
    this.canvas.width = width * this.dpr;
    this.canvas.height = height * this.dpr;

    this.ctx.scale(this.dpr, this.dpr);
    this.canvas.style.width = `${width}px`;
    this.canvas.style.height = `${height}px`;

    this.ctx.lineCap = 'round';
    this.ctx.lineJoin = 'round';

    if (prevImage) {
      this.ctx.putImageData(prevImage, 0, 0);
    }
  }

  attachPointerEvents() {
    this.canvas.addEventListener('pointerdown', (e) => this.onPointerDown(e));
    this.canvas.addEventListener('pointermove', (e) => this.onPointerMove(e));
    this.canvas.addEventListener('pointerup', () => this.onPointerUp());
    this.canvas.addEventListener('pointercancel', () => this.onPointerUp());
  }

  getPointerPos(e) {
    const rect = this.canvas.getBoundingClientRect();
    return {
      x: e.clientX - rect.left,
      y: e.clientY - rect.top
    };
  }

  onPointerDown(e) {
    this.canvas.setPointerCapture(e.pointerId);
    this.isDrawing = true;

    // Mevcut çizimi undo yığınına kaydet
    const currentState = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);
    this.history.saveState(currentState);

    const pos = this.getPointerPos(e);
    this.lastX = pos.x;
    this.lastY = pos.y;

    const canvasSettings = state.get().canvas;
    this.ctx.beginPath();
    this.ctx.moveTo(this.lastX, this.lastY);

    if (canvasSettings.isEraser) {
      this.ctx.globalCompositeOperation = 'destination-out';
      this.ctx.lineWidth = canvasSettings.penWidth * 6;
    } else {
      this.ctx.globalCompositeOperation = 'source-over';
      this.ctx.strokeStyle = canvasSettings.penColor;
      this.ctx.lineWidth = canvasSettings.penWidth;
    }

    // Tek dokunuşta nokta bırakabilmesi için
    this.ctx.lineTo(this.lastX + 0.1, this.lastY + 0.1);
    this.ctx.stroke();
  }

  onPointerMove(e) {
    if (!this.isDrawing) return;

    const pos = this.getPointerPos(e);
    
    this.ctx.beginPath();
    this.ctx.moveTo(this.lastX, this.lastY);
    this.ctx.lineTo(pos.x, pos.y);
    this.ctx.stroke();

    this.lastX = pos.x;
    this.lastY = pos.y;
  }

  onPointerUp() {
    this.isDrawing = false;
  }

  undo() {
    const currentState = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);
    const prevState = this.history.undo(currentState);
    if (prevState) {
      this.ctx.putImageData(prevState, 0, 0);
    }
  }

  redo() {
    const currentState = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);
    const nextState = this.history.redo(currentState);
    if (nextState) {
      this.ctx.putImageData(nextState, 0, 0);
    }
  }

  clear() {
    const currentState = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);
    this.history.saveState(currentState);
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
  }

  toggleGrid() {
    this.showGrid = !this.showGrid;
    if (this.showGrid) {
      this.container.style.backgroundImage = 'radial-gradient(var(--canvas-grid) 1.5px, transparent 1.5px)';
      this.container.style.backgroundSize = '24px 24px';
    } else {
      this.container.style.backgroundImage = 'none';
    }
    return this.showGrid;
  }
}
