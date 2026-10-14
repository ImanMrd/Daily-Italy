/**
 * DAILY-ITALY — Smart Review & Vocabulary Vault View
 * Spaced Repetition System (SuperMemo-2 SM-2)
 * English Interface with Italian Target Immersion
 */

class ReviewView {
  constructor(container) {
    this.container = container;
    this.currentMode = 'cards'; // 'cards' or 'vault'
    this.currentFilter = 'all';
    this.queue = [];
    this.currentIndex = 0;
    this.isFlipped = false;
    this.reviewedCount = 0;
    this.totalXpEarned = 0;
  }

  async render() {
    if (!window.api.user) {
      this.container.innerHTML = `
        <div class="auth-gate-card">
          <div class="auth-gate-icon">🧠</div>
          <h2 style="font-family: var(--font-serif); font-size: 1.8rem; margin-bottom: 12px; color: var(--text-primary);">
            Smart Review: Spaced Repetition SRS
          </h2>
          <p style="color: var(--text-secondary); max-width: 540px; margin: 0 auto 24px; line-height: 1.6;">
            Smart Review adapts intervals to your personal memory strength using the SuperMemo-2 algorithm. To store your learning progress over time, please log in or create an account.
          </p>
          <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
            <button class="btn-tactile" onclick="window.app.openAuthModal(false)">
              🔑 Log In to Account
            </button>
            <button class="btn-secondary" onclick="window.app.openAuthModal(true)">
              ✨ Create Free Account
            </button>
          </div>
        </div>
      `;
      return;
    }

    this.container.innerHTML = `
      <div style="text-align: center; padding: 40px; color: var(--text-secondary);">
        <p>Loading intelligent review session...</p>
      </div>
    `;

    try {
      const stats = await window.api.getStats().catch(() => null);
      const queueData = await window.api.getReviewQueue(this.currentFilter);
      this.queue = queueData.words || [];
      this.currentIndex = 0;
      this.isFlipped = false;
      this.reviewedCount = 0;
      this.totalXpEarned = 0;

      if (this.currentMode === 'cards' && this.queue.length > 0) {
        this.renderCardSession(stats);
      } else {
        this.renderVault(stats, queueData);
      }
    } catch (e) {
      this.container.innerHTML = `
        <div style="text-align: center; padding: 40px; color: #ef4444;">
          <p>Error loading review: ${e.message}</p>
          <button class="btn-secondary" style="margin-top: 14px;" onclick="window.reviewView.render()">Try Again</button>
        </div>
      `;
    }
  }

  renderCardSession(stats) {
    if (this.currentIndex >= this.queue.length) {
      this.renderCompletionScreen();
      return;
    }

    const word = this.queue[this.currentIndex];
    const progressPct = Math.round((this.currentIndex / this.queue.length) * 100);

    let html = `
      <div class="review-view" style="max-width: 680px; margin: 0 auto;">
        
        <!-- Header & Mode Switcher -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
          <div>
            <h1 style="font-family: var(--font-serif); font-size: 1.8rem; color: var(--text-primary); margin-bottom: 4px;">
              Smart Review SRS
            </h1>
            <p style="color: var(--text-secondary); font-size: 0.85rem;">
              Word ${this.currentIndex + 1} of ${this.queue.length} &bull; Spaced Repetition Mode
            </p>
          </div>
          <button class="btn-secondary" style="padding: 8px 14px; font-size: 0.85rem;" onclick="window.reviewView.toggleMode('vault')">
            📋 View Vocabulary Vault
          </button>
        </div>

        <!-- Progress Bar -->
        <div class="progress-bar-container" style="margin-bottom: 24px;">
          <div class="progress-bar-fill" style="width: ${progressPct}%;"></div>
        </div>

        <!-- Interactive SRS 3D Card -->
        <div class="flashcard-scene" onclick="window.reviewView.flipCard()">
          <div class="flashcard ${this.isFlipped ? 'is-flipped' : ''}" id="srs-card">
            
            <!-- Front Face -->
            <div class="flashcard-face flashcard-front">
              <div class="flashcard-top-row">
                <span class="gram-badge">${word.word_type || 'Word'}</span>
                <span style="font-size: 0.8rem; color: var(--text-muted);">Tap to flip ↻</span>
              </div>

              <div class="flashcard-italian" style="font-family: var(--font-serif); font-size: 2.5rem; margin: 20px 0 8px;">
                ${word.italian}
              </div>

              ${word.pronunciation ? `
                <div class="flashcard-pronunciation" style="margin-bottom: 16px;">
                  [ ${word.pronunciation} ]
                </div>
              ` : ''}

              <button class="audio-btn" style="width: 44px; height: 44px; font-size: 1.2rem; margin: 10px auto;" onclick="event.stopPropagation(); window.soundEngine.speakItalian('${word.italian}')" title="Listen to native Italian pronunciation">
                🔊
              </button>

              ${word.example_it ? `
                <div class="flashcard-example-box" style="margin-top: 20px; font-style: italic;">
                  "${word.example_it}"
                </div>
              ` : ''}

              <div style="margin-top: 24px;">
                <button class="btn-secondary" style="padding: 10px 20px; font-size: 0.9rem;" onclick="event.stopPropagation(); window.reviewView.flipCard()">
                  👀 Show Solution
                </button>
              </div>
            </div>

            <!-- Back Face -->
            <div class="flashcard-face flashcard-back">
              <div class="flashcard-top-row">
                <span class="gram-badge">${word.word_type || 'Word'}</span>
                <button class="audio-btn" style="width: 32px; height: 32px; font-size: 0.9rem;" onclick="event.stopPropagation(); window.soundEngine.speakItalian('${word.italian}')">
                  🔊
                </button>
              </div>

              <div style="font-family: var(--font-serif); font-size: 1.6rem; color: var(--terracotta); font-weight: 700; margin-top: 12px;">
                ${word.italian}
              </div>

              <div class="flashcard-english" style="font-size: 1.6rem; font-weight: 700; color: var(--text-primary); margin: 12px 0;">
                ${word.english}
              </div>

              ${word.example_it && word.example_en ? `
                <div class="flashcard-example-box" style="margin-top: 14px; text-align: left;">
                  <div style="color: var(--text-primary); font-style: italic; margin-bottom: 4px;">"${word.example_it}"</div>
                  <div style="color: var(--text-secondary); font-size: 0.85rem;">"${word.example_en}"</div>
                </div>
              ` : ''}

              ${word.related_words ? `
                <div style="margin-top: 14px; font-size: 0.85rem; color: var(--text-muted);">
                  Related words: <strong style="color: var(--text-secondary);">${word.related_words}</strong>
                </div>
              ` : ''}
            </div>

          </div>
        </div>

        <!-- SM-2 Evaluation Buttons (Visible when flipped) -->
        <div style="margin-top: 24px; text-align: center;">
          <div style="font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 12px; font-weight: 600;">
            How well did you remember this word?
          </div>
          <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;">
            <button class="btn-srs btn-srs-again" onclick="window.reviewView.rateWord(${word.word_id}, 1)">
              <div style="font-weight: 800; font-size: 1rem;">1</div>
              <div>Again</div>
              <div style="font-size: 0.7rem; opacity: 0.8;">1 day</div>
            </button>
            <button class="btn-srs btn-srs-hard" onclick="window.reviewView.rateWord(${word.word_id}, 2)">
              <div style="font-weight: 800; font-size: 1rem;">2</div>
              <div>Hard</div>
              <div style="font-size: 0.7rem; opacity: 0.8;">2 days</div>
            </button>
            <button class="btn-srs btn-srs-good" onclick="window.reviewView.rateWord(${word.word_id}, 3)">
              <div style="font-weight: 800; font-size: 1rem;">3</div>
              <div>Good</div>
              <div style="font-size: 0.7rem; opacity: 0.8;">+Interval</div>
            </button>
            <button class="btn-srs btn-srs-easy" onclick="window.reviewView.rateWord(${word.word_id}, 4)">
              <div style="font-weight: 800; font-size: 1rem;">4</div>
              <div>Easy</div>
              <div style="font-size: 0.7rem; opacity: 0.8;">+Interval x1.3</div>
            </button>
          </div>
        </div>

      </div>
    `;

    this.container.innerHTML = html;
  }

  flipCard() {
    this.isFlipped = !this.isFlipped;
    const cardEl = document.getElementById('srs-card');
    if (cardEl) {
      cardEl.classList.toggle('is-flipped', this.isFlipped);
    }
  }

  async rateWord(wordId, rating) {
    try {
      const res = await window.api.submitReviewRating(wordId, rating);
      this.reviewedCount++;
      const xpAward = rating >= 3 ? 5 : 2;
      this.totalXpEarned += xpAward;

      if (window.soundEngine) {
        if (rating >= 3) {
          window.soundEngine.playSuccess();
        } else {
          window.soundEngine.playTap();
        }
      }

      // Update user bar
      const xpEl = document.getElementById('user-xp-val');
      if (xpEl) {
        xpEl.innerText = parseInt(xpEl.innerText || '0', 10) + xpAward;
      }

      this.currentIndex++;
      this.isFlipped = false;
      this.renderCardSession();
    } catch (e) {
      console.error('Error submitting SRS rating:', e);
      this.currentIndex++;
      this.isFlipped = false;
      this.renderCardSession();
    }
  }

  renderCompletionScreen() {
    if (window.soundEngine) {
      window.soundEngine.playCelebration();
    }
    if (window.app && typeof window.app.triggerConfetti === 'function') {
      window.app.triggerConfetti();
    }

    this.container.innerHTML = `
      <div style="max-width: 560px; margin: 40px auto; background: var(--bg-surface); border: 2px solid var(--border-subtle); border-radius: var(--radius-lg); padding: 40px 30px; text-align: center; box-shadow: var(--shadow-md);">
        <div style="font-size: 3.5rem; margin-bottom: 12px;">🎉</div>
        <h2 style="font-family: var(--font-serif); font-size: 2rem; color: var(--text-primary); margin-bottom: 8px;">
          Review Session Complete!
        </h2>
        <p style="color: var(--text-secondary); margin-bottom: 24px;">
          Outstanding work! You reinforced memory retention for <strong>${this.reviewedCount}</strong> Italian words.
        </p>

        <div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 30px;">
          <div style="background: var(--bg-app-alt); padding: 16px 24px; border-radius: var(--radius-md);">
            <div style="font-size: 1.8rem; font-weight: 800; color: var(--tuscan-gold);">+${this.totalXpEarned}</div>
            <div style="font-size: 0.8rem; color: var(--text-secondary); text-transform: uppercase;">XP Earned</div>
          </div>
          <div style="background: var(--bg-app-alt); padding: 16px 24px; border-radius: var(--radius-md);">
            <div style="font-size: 1.8rem; font-weight: 800; color: var(--olive);">${this.reviewedCount}</div>
            <div style="font-size: 0.8rem; color: var(--text-secondary); text-transform: uppercase;">Words Reviewed</div>
          </div>
        </div>

        <div style="display: flex; gap: 12px; justify-content: center;">
          <button class="btn-tactile" onclick="window.reviewView.render()">
            🔄 Review More
          </button>
          <button class="btn-secondary" onclick="window.app.switchView('roadmap')">
            🗺️ Return to Chapters
          </button>
        </div>
      </div>
    `;
  }

  renderVault(stats, queueData) {
    const totalWords = stats ? stats.total_words : queueData.count;
    const mastered = stats ? stats.words_mastered : 0;
    const learning = stats ? stats.words_learning : queueData.count;

    let html = `
      <div class="review-view">
        <div style="margin-bottom: 24px; display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 12px;">
          <div>
            <h1 style="font-family: var(--font-serif); font-size: 2rem; margin-bottom: 4px; color: var(--text-primary);">
              Vocabulary Vault & Smart Review
            </h1>
            <p style="color: var(--text-secondary); font-size: 0.9rem;">
              SuperMemo-2 spaced repetition: words adapt automatically to your personal retention curve.
            </p>
          </div>
          <div style="display: flex; gap: 10px;">
            <button class="btn-tactile" onclick="window.reviewView.toggleMode('cards')">
              ⚡ Start Flashcard Review
            </button>
          </div>
        </div>

        <div class="review-stats-summary">
          <div class="stat-card">
            <div class="stat-card-value">${totalWords}</div>
            <div class="stat-card-label">Available Words</div>
          </div>
          <div class="stat-card">
            <div class="stat-card-value" style="color: var(--amalfi-blue);">${learning}</div>
            <div class="stat-card-label">In Learning</div>
          </div>
          <div class="stat-card">
            <div class="stat-card-value" style="color: var(--olive);">${mastered}</div>
            <div class="stat-card-label">Mastered Words</div>
          </div>
        </div>

        <div style="display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap;">
          <button class="nav-btn ${this.currentFilter === 'all' ? 'active' : ''}" onclick="window.reviewView.setFilter('all')">
            All (${queueData.count})
          </button>
          <button class="nav-btn ${this.currentFilter === 'weak' ? 'active' : ''}" onclick="window.reviewView.setFilter('weak')">
            Words to Consolidate
          </button>
          <button class="nav-btn ${this.currentFilter === 'due' ? 'active' : ''}" onclick="window.reviewView.setFilter('due')">
            Due for Review Today
          </button>
        </div>

        <div style="overflow-x: auto; background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); box-shadow: var(--shadow-sm);">
          <table class="vocab-vault-table" style="width: 100%; border-collapse: collapse;">
            <thead>
              <tr style="border-bottom: 2px solid var(--border-subtle); background: var(--bg-app-alt);">
                <th style="padding: 12px; text-align: left;">Audio</th>
                <th style="padding: 12px; text-align: left;">Italian</th>
                <th style="padding: 12px; text-align: left;">Part of Speech</th>
                <th style="padding: 12px; text-align: left;">English</th>
                <th style="padding: 12px; text-align: left;">Memory Status</th>
              </tr>
            </thead>
            <tbody>
    `;

    if (queueData.words.length === 0) {
      html += `
        <tr>
          <td colspan="5" style="text-align: center; padding: 40px; color: var(--text-muted);">
            No words found matching this filter. Continue studying chapters to expand your vault!
          </td>
        </tr>
      `;
    } else {
      queueData.words.forEach(w => {
        let statusBadge = `<span style="color: var(--amalfi-blue); font-size: 0.8rem; font-weight: 700;">● Learning</span>`;
        if (w.mastery_status === 'mastered') {
          statusBadge = `<span style="color: var(--olive); font-size: 0.8rem; font-weight: 700;">★ Mastered</span>`;
        } else if (w.mastery_status === 'review_needed') {
          statusBadge = `<span style="color: #ef4444; font-size: 0.8rem; font-weight: 700;">▲ Due for Review</span>`;
        }

        html += `
          <tr style="border-bottom: 1px solid var(--border-subtle);">
            <td style="width: 50px; padding: 12px;">
              <button class="audio-btn" style="width: 32px; height: 32px; font-size: 0.9rem;" onclick="window.soundEngine.speakItalian('${w.italian}')">
                🔊
              </button>
            </td>
            <td style="font-weight: 700; font-size: 1.05rem; font-family: var(--font-serif); color: var(--text-primary); padding: 12px;">
              ${w.italian}
            </td>
            <td style="padding: 12px;"><span class="gram-badge" style="font-size: 0.7rem;">${w.word_type || 'Word'}</span></td>
            <td style="color: var(--text-secondary); font-size: 0.95rem; padding: 12px;">${w.english}</td>
            <td style="padding: 12px;">${statusBadge}</td>
          </tr>
        `;
      });
    }

    html += `
            </tbody>
          </table>
        </div>
      </div>
    `;

    this.container.innerHTML = html;
  }

  toggleMode(mode) {
    this.currentMode = mode;
    this.render();
  }

  setFilter(filterMode) {
    this.currentFilter = filterMode;
    this.render();
  }
}

window.ReviewView = ReviewView;
