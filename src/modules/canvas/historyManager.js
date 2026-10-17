export class HistoryManager {
  constructor(maxSteps = 15) {
    this.maxSteps = maxSteps;
    this.undoStack = [];
    this.redoStack = [];
  }

  saveState(imageData) {
    this.undoStack.push(imageData);
    if (this.undoStack.length > this.maxSteps) {
      this.undoStack.shift();
    }
    // Yeni bir çizim yapıldığında redo yığını temizlenir
    this.redoStack = [];
  }

  undo(currentState) {
    if (this.undoStack.length === 0) return null;
    if (currentState) {
      this.redoStack.push(currentState);
    }
    return this.undoStack.pop();
  }

  redo(currentState) {
    if (this.redoStack.length === 0) return null;
    if (currentState) {
      this.undoStack.push(currentState);
    }
    return this.redoStack.pop();
  }

  canUndo() {
    return this.undoStack.length > 0;
  }

  canRedo() {
    return this.redoStack.length > 0;
  }

  clear() {
    this.undoStack = [];
    this.redoStack = [];
  }
}
