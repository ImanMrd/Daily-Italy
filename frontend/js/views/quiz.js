/**
 * DAILY-ITALY — Interactive Quiz & Exercise Engine
 * English Interface with Instant Pedagogical Feedback
 */

class QuizView {
  constructor(container) {
    this.container = container;
    this.lessonId = null;
    this.exercises = [];
    this.currentIndex = 0;
    this.submissions = [];
    this.matchingState = {
      selectedTile: null,
      matchesFound: 0,
      totalPairs: 0
    };
  }

  async loadLessonExercises(lessonId) {
    if (!window.api.user) {
      this.container.innerHTML = `
        <div class="auth-gate-card">
          <div class="auth-gate-icon">🎯</div>
          <h2 style="font-family: var(--font-serif); font-size: 1.8rem; margin-bottom: 12px; color: var(--text-primary);">
            Consolidation Exercises & Quizzes
          </h2>
          <p style="color: var(--text-secondary); max-width: 540px; margin: 0 auto 24px; line-height: 1.6;">
            Quizzes test your retention, unlock subsequent chapters, and award XP and streaks. Log in or create an account to start.
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
    this.submissions = [];

    this.container.innerHTML = `
      <div style="text-align: center; padding: 40px 0; color: var(--text-secondary);">
        <p>Preparing exercises...</p>
      </div>
    `;

    try {
      this.exercises = await window.api.getExercises(lessonId);
      if (!this.exercises || this.exercises.length === 0) {
        this.container.innerHTML = `<div style="text-align: center; padding: 40px;">No exercises found for this chapter.</div>`;
        return;
      }
      this.renderQuestion();
    } catch (e) {
      this.container.innerHTML = `<div style="text-align: center; padding: 40px; color: #ef4444;">Error: ${e.message}</div>`;
    }
  }

  renderQuestion() {
    if (this.currentIndex >= this.exercises.length) {
      this.submitAndShowResults();
      return;
    }

    const ex = this.exercises[this.currentIndex];
    const progressPct = ((this.currentIndex + 1) / this.exercises.length) * 100;

    let exerciseContent = '';

    if (ex.exercise_type === 'matching') {
      exerciseContent = this.buildMatchingHtml(ex);
    } else {
      // Multiple choice, cloze, odd_one_out
      const options = JSON.parse(ex.options_json || '[]');
      exerciseContent = `
        <div class="options-list">
          ${options.map(opt => `
            <button class="option-btn" onclick="window.quizView.handleOptionClick(this, '${opt.replace(/'/g, "\\'")}')">
              <span>${opt}</span>
              <span class="opt-check"></span>
            </button>
          `).join('')}
        </div>
      `;
    }

    this.container.innerHTML = `
      <div class="quiz-container">
        <div class="quiz-header">
          <span class="quiz-badge">${ex.exercise_type.replace('_', ' ')}</span>
          <div style="flex: 1; margin: 0 16px; height: 8px; background: var(--bg-app); border-radius: var(--radius-full); overflow: hidden;">
            <div style="width: ${progressPct}%; height: 100%; background: var(--terracotta); transition: width 0.3s ease;"></div>
          </div>
          <span style="font-weight: 700; font-size: 0.85rem; color: var(--text-muted);">
            ${this.currentIndex + 1} of ${this.exercises.length}
          </span>
        </div>

        <div class="quiz-prompt">${ex.prompt}</div>

        ${exerciseContent}

        <div class="quiz-feedback" id="quiz-feedback-box"></div>

        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 20px;">
          <button class="btn-secondary" onclick="window.app.switchView('roadmap')">
            Exit
          </button>
          <button class="btn-tactile" id="quiz-next-btn" style="display: none;" onclick="window.quizView.nextQuestion()">
            Continue →
          </button>
        </div>
      </div>
    `;

    if (ex.exercise_type === 'matching') {
      this.initMatchingGame(ex);
    }
  }

  buildMatchingHtml(ex) {
    const pairs = JSON.parse(ex.options_json || '{}');
    const italianKeys = Object.keys(pairs);
    const englishValues = Object.values(pairs);

    // Shuffle both columns
    const shuffledIt = [...italianKeys].sort(() => Math.random() - 0.5);
    const shuffledEn = [...englishValues].sort(() => Math.random() - 0.5);

    this.matchingState.totalPairs = italianKeys.length;
    this.matchingState.matchesFound = 0;
    this.matchingState.pairs = pairs;

    return `
      <div class="matching-board" id="matching-board">
        <div style="display: flex; flex-direction: column; gap: 10px;">
          ${shuffledIt.map(it => `
            <div class="match-tile" data-type="it" data-val="${it}" onclick="window.quizView.handleTileClick(this)">
              ${it}
            </div>
          `).join('')}
        </div>
        <div style="display: flex; flex-direction: column; gap: 10px;">
          ${shuffledEn.map(en => `
            <div class="match-tile" data-type="en" data-val="${en}" onclick="window.quizView.handleTileClick(this)">
              ${en}
            </div>
          `).join('')}
        </div>
      </div>
    `;
  }

  initMatchingGame(ex) {
    this.matchingState.selectedTile = null;
  }

  handleTileClick(tileEl) {
    if (tileEl.classList.contains('matched')) return;

    if (!this.matchingState.selectedTile) {
      // First selection
      this.matchingState.selectedTile = tileEl;
      tileEl.classList.add('selected');
      return;
    }

    const prev = this.matchingState.selectedTile;
    if (prev === tileEl) {
      tileEl.classList.remove('selected');
      this.matchingState.selectedTile = null;
      return;
    }

    // Check if one is IT and one is EN
    if (prev.dataset.type === tileEl.dataset.type) {
      prev.classList.remove('selected');
      this.matchingState.selectedTile = tileEl;
      tileEl.classList.add('selected');
      return;
    }

    const itVal = prev.dataset.type === 'it' ? prev.dataset.val : tileEl.dataset.val;
    const enVal = prev.dataset.type === 'en' ? prev.dataset.val : tileEl.dataset.val;

    if (this.matchingState.pairs[itVal] === enVal) {
      // Correct match!
      window.soundEngine.playSuccess();
      prev.classList.remove('selected');
      tileEl.classList.remove('selected');
      prev.classList.add('matched');
      tileEl.classList.add('matched');
      this.matchingState.selectedTile = null;
      this.matchingState.matchesFound++;

      if (this.matchingState.matchesFound >= this.matchingState.totalPairs) {
        // Complete!
        this.submissions.push({
          exercise_id: this.exercises[this.currentIndex].id,
          user_answer: 'matched'
        });
        const nextBtn = document.getElementById('quiz-next-btn');
        if (nextBtn) nextBtn.style.display = 'inline-flex';
      }
    } else {
      // Wrong match
      window.soundEngine.playWrong();
      prev.classList.add('wrong');
      tileEl.classList.add('wrong');
      setTimeout(() => {
        prev.classList.remove('selected', 'wrong');
        tileEl.classList.remove('selected', 'wrong');
        this.matchingState.selectedTile = null;
      }, 500);
    }
  }

  async handleOptionClick(btnEl, optionValue) {
    const ex = this.exercises[this.currentIndex];
    const feedbackBox = document.getElementById('quiz-feedback-box');
    const nextBtn = document.getElementById('quiz-next-btn');

    // Disable all options
    document.querySelectorAll('.option-btn').forEach(b => b.style.pointerEvents = 'none');

    this.submissions.push({
      exercise_id: ex.id,
      user_answer: optionValue
    });

    try {
      const evaluation = await window.api.checkAnswer(ex.id, optionValue);
      if (evaluation.correct) {
        window.soundEngine.playSuccess();
        btnEl.classList.add('correct');
        feedbackBox.className = 'quiz-feedback correct';
        feedbackBox.innerHTML = `<strong>Correct! (Esatto!)</strong> ${evaluation.explanation || ''}`;
      } else {
        window.soundEngine.playWrong();
        btnEl.classList.add('wrong');
        feedbackBox.className = 'quiz-feedback wrong';
        feedbackBox.innerHTML = `<strong>Not quite.</strong> Correct answer: <em>${evaluation.correct_answer}</em>.<br>${evaluation.explanation || ''}`;
      }
    } catch (e) {
      // Fallback in case of network issue
      feedbackBox.className = 'quiz-feedback correct';
      feedbackBox.innerHTML = `Answer recorded.`;
    }

    nextBtn.style.display = 'inline-flex';
  }

  nextQuestion() {
    this.currentIndex++;
    this.renderQuestion();
  }

  async submitAndShowResults() {
    this.container.innerHTML = `
      <div style="text-align: center; padding: 40px; color: var(--text-secondary);">
        <p>Evaluating answers and calculating XP...</p>
      </div>
    `;

    try {
      const result = await window.api.submitExercises(this.lessonId, this.submissions);
      window.app.updateUserStatsBar();

      if (result.score_percentage >= 70) {
        window.app.triggerConfetti();
      }

      this.container.innerHTML = `
        <div style="max-width: 580px; margin: 30px auto; background: var(--bg-surface); padding: 36px; border-radius: var(--radius-lg); border: 1px solid var(--border-prominent); text-align: center; box-shadow: var(--shadow-lg);">
          <div style="font-size: 3rem; margin-bottom: 12px;">
            ${result.score_percentage >= 70 ? '🏆' : '💪'}
          </div>
          <h2 style="font-family: var(--font-serif); font-size: 2rem; margin-bottom: 8px;">
            ${result.score_percentage >= 70 ? 'Exercises Completed!' : 'Keep Practicing!'}
          </h2>
          <p style="color: var(--text-secondary); margin-bottom: 24px;">
            Score achieved: <strong>${result.correct_count} / ${result.total} (${result.score_percentage}%)</strong>
          </p>

          <div style="display: flex; justify-content: center; gap: 24px; margin-bottom: 28px;">
            <div style="background: var(--bg-surface-elevated); padding: 12px 20px; border-radius: var(--radius-md);">
              <div style="font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase;">XP Earned</div>
              <div style="font-size: 1.4rem; font-weight: 800; color: var(--tuscan-gold);">+${result.xp_awarded} XP</div>
            </div>
            <div style="background: var(--bg-surface-elevated); padding: 12px 20px; border-radius: var(--radius-md);">
              <div style="font-size: 0.8rem; color: var(--text-muted); text-transform: uppercase;">Daily Streak</div>
              <div style="font-size: 1.4rem; font-weight: 800; color: var(--terracotta);">🔥 ${result.current_streak}</div>
            </div>
          </div>

          <div style="display: flex; justify-content: center; gap: 14px;">
            <button class="btn-tactile" onclick="window.app.switchView('roadmap')">
              Return to Chapters
            </button>
            <button class="btn-secondary" onclick="window.quizView.loadLessonExercises(${this.lessonId})">
              Retake Exercises
            </button>
          </div>
        </div>
      `;
    } catch (e) {
      this.container.innerHTML = `<div style="text-align: center; padding: 40px; color: #ef4444;">Error: ${e.message}</div>`;
    }
  }
}

window.QuizView = QuizView;
