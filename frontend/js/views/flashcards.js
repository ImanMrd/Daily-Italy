/**
 * DAILY-ITALY — 3D Flashcard Studio View
 * English Interface with Native Italian Pronunciation
 */

class FlashcardView {
  constructor(container) {
    this.container = container;
    this.words = [];
    this.currentIndex = 0;
    this.lessonId = null;
    this.isFlipped = false;
  }

  async loadLesson(lessonId) {
    if (!window.api.user) {
      this.container.innerHTML = `
        <div class="auth-gate-card">
          <div class="auth-gate-icon">🃏</div>
          <h2 style="font-family: var(--font-serif); font-size: 1.8rem; margin-bottom: 12px; color: var(--text-primary);">
            3D Flashcards & Pronunciation
          </h2>
          <p style="color: var(--text-secondary); max-width: 540px; margin: 0 auto 24px; line-height: 1.6;">
            Study high-frequency vocabulary with interactive 3D flashcards, listen to native Italian pronunciation, and track your spaced repetition progress.
          </p>
          <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
            <button class="btn-tactile" onclick="window.app.openAuthModal(false)">🔑 Log In to Account</button>
            <button class="btn-secondary" onclick="window.app.openAuthModal(true)">✨ Create Free Account</button>
          </div>
        </div>
      `;
      return;
    }

    this.lessonId = lessonId;
    this.currentIndex = 0;
    this.isFlipped = false;

    this.container.innerHTML = `
      <div style="text-align: center; padding: 40px 0; color: var(--text-secondary);">
        <p>Loading flashcards...</p>
      </div>
    `;

    try {
      this.words = await window.api.getWords(lessonId);
      if (!this.words || this.words.length === 0) {
        this.container.innerHTML = `<div style="text-align: center; padding: 40px;">No words found for this chapter.</div>`;
        return;
      }
      this.renderCurrentCard();
    } catch (e) {
      this.container.innerHTML = `<div style="text-align: center; padding: 40px; color: #ef4444;">Error: ${e.message}</div>`;
    }
  }

  renderCurrentCard() {
    if (this.currentIndex >= this.words.length) {
      this.renderCompletionScreen();
      return;
    }

    const word = this.words[this.currentIndex];
    const progressPct = ((this.currentIndex + 1) / this.words.length) * 100;

    this.container.innerHTML = `
      <div class="flashcard-session">
        <div class="session-header">
          <button class="btn-secondary" onclick="window.app.switchView('roadmap')">
            ← Back to Chapters
          </button>
          <div class="session-progress-bar">
            <div class="progress-fill" style="width: ${progressPct}%;"></div>
          </div>
          <span style="font-weight: 700; font-size: 0.9rem; color: var(--tuscan-gold);">
            ${this.currentIndex + 1} / ${this.words.length}
          </span>
        </div>

        <div class="card-perspective-stage" onclick="window.flashcardView.flipCard()">
          <div class="flashcard-3d ${this.isFlipped ? 'flipped' : ''}" id="active-flashcard">
            
            <!-- FRONT -->
            <div class="card-face card-front">
              <div class="card-front-top">
                <span class="gram-badge">${word.word_type || 'Word'}</span>
                <button class="audio-btn" title="Listen to pronunciation" onclick="event.stopPropagation(); window.flashcardView.speakCurrent();">
                  🔊
                </button>
              </div>

              <div class="card-front-center">
                <div class="italian-word">${word.italian}</div>
                ${word.pronunciation ? `<div class="phonetic-guide">/${word.pronunciation}/</div>` : ''}
              </div>

              <div class="card-hint">
                <span>Tap or click card to see English translation ↺</span>
              </div>
            </div>

            <!-- BACK -->
            <div class="card-face card-back">
              <div>
                <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--amalfi-blue); margin-bottom: 6px;">
                  English Translation
                </div>
                <div class="english-translation">${word.english}</div>
              </div>

              ${word.example_it ? `
                <div class="example-sentence-box">
                  <div class="example-it">"${word.example_it}"</div>
                  <div class="example-en">${word.example_en || ''}</div>
                </div>
              ` : ''}

              ${word.related_words ? `
                <div class="family-box">
                  <strong>Related words:</strong> ${word.related_words}
                </div>
              ` : '<div></div>'}

              <div class="card-hint">
                <span>Rate your memory strength below to schedule review ↓</span>
              </div>
            </div>

          </div>
        </div>

        <!-- SRS Rating Controls -->
        <div class="srs-controls">
          <button class="srs-btn btn-again" onclick="window.flashcardView.rateCard(1)">
            <span>Again</span>
            <span class="sub-label">&lt; 1 day</span>
          </button>
          <button class="srs-btn btn-hard" onclick="window.flashcardView.rateCard(2)">
            <span>Hard</span>
            <span class="sub-label">2 days</span>
          </button>
          <button class="srs-btn btn-good" onclick="window.flashcardView.rateCard(3)">
            <span>Good</span>
            <span class="sub-label">4 days</span>
          </button>
          <button class="srs-btn btn-easy" onclick="window.flashcardView.rateCard(4)">
            <span>Easy</span>
            <span class="sub-label">7 days</span>
          </button>
        </div>
      </div>
    `;

    // Automatically speak the Italian word on appearance
    window.soundEngine.speakItalian(word.italian);
  }

  flipCard() {
    this.isFlipped = !this.isFlipped;
    window.soundEngine.playFlip();
    const cardEl = document.getElementById('active-flashcard');
    if (cardEl) {
      cardEl.classList.toggle('flipped', this.isFlipped);
    }
  }

  speakCurrent() {
    const word = this.words[this.currentIndex];
    if (word) {
      window.soundEngine.speakItalian(word.italian);
    }
  }

  async rateCard(rating) {
    const word = this.words[this.currentIndex];
    window.soundEngine.playSuccess();

    // Fire & forget review submission to update SM-2 SRS schedule
    window.api.submitReviewRating(word.id, rating).catch(() => {});

    this.currentIndex++;
    this.isFlipped = false;
    this.renderCurrentCard();
  }

  renderCompletionScreen() {
    window.app.triggerConfetti();
    this.container.innerHTML = `
      <div style="max-width: 520px; margin: 40px auto; text-align: center; background: var(--bg-surface); padding: 40px; border-radius: var(--radius-lg); border: 1px solid var(--border-prominent); box-shadow: var(--shadow-lg);">
        <div style="font-size: 3rem; margin-bottom: 12px;">🎉</div>
        <h2 style="font-family: var(--font-serif); font-size: 1.8rem; margin-bottom: 8px;">Great Job!</h2>
        <p style="color: var(--text-secondary); margin-bottom: 24px;">
          You reviewed all words in this session. Now test your retention and earn XP with the related exercises!
        </p>
        <div style="display: flex; gap: 12px; justify-content: center;">
          <button class="btn-tactile" onclick="window.app.startQuiz(${this.lessonId})">
            ✍️ Start Exercises (+50 XP)
          </button>
          <button class="btn-secondary" onclick="window.app.switchView('roadmap')">
            Return to Chapters
          </button>
        </div>
      </div>
    `;
  }
}

window.FlashcardView = FlashcardView;
