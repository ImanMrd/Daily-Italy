/**
 * DAILY-ITALY — Writing & Sentence Building View (Scrittura & Costruzione Frasi)
 * English Interface with Interactive Italian Sentence Construction Lab
 */

class WritingView {
  constructor(container) {
    this.container = container;
    this.currentLevel = '';
    this.prompts = [];
    this.activePrompt = null;
    this.userText = '';
    this.evaluation = null;
    this.isEvaluating = false;
  }

  async render() {
    if (!window.api.user) {
      this.container.innerHTML = `
        <div class="auth-gate-card">
          <div class="auth-gate-icon">✍️</div>
          <h2 style="font-family: var(--font-serif); font-size: 1.8rem; margin-bottom: 12px; color: var(--text-primary);">
            Italian Writing & Sentence Building
          </h2>
          <p style="color: var(--text-secondary); max-width: 540px; margin: 0 auto 24px; line-height: 1.6;">
            Train your composition skills with interactive starter tiles, contextual task prompts, and immediate comparison against native model solutions. Log in to continue.
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
        <p>Loading writing exercises...</p>
      </div>
    `;

    try {
      this.prompts = await window.api.getWritingPrompts(this.currentLevel);
      if (!this.activePrompt && this.prompts.length > 0) {
        this.activePrompt = this.prompts[0];
      }
      this.renderLayout();
    } catch (e) {
      this.container.innerHTML = `
        <div style="text-align: center; padding: 40px; color: #ef4444;">
          <p>Error loading writing exercises: ${e.message}</p>
          <button class="btn-secondary" style="margin-top: 12px;" onclick="window.writingView.render()">Try Again</button>
        </div>
      `;
    }
  }

  renderLayout() {
    const prompt = this.activePrompt;

    let starterChipsHtml = '';
    if (prompt && prompt.starter_words_json) {
      try {
        const chips = JSON.parse(prompt.starter_words_json);
        starterChipsHtml = `
          <div style="margin: 16px 0;">
            <div style="font-size: 0.8rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-bottom: 8px;">
              Starter Words (Tap to insert into your response):
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
              ${chips.map(chip => `
                <button 
                  type="button" 
                  class="starter-chip-btn"
                  onclick="window.writingView.appendChip('${chip.replace(/'/g, "\\'")}')"
                  style="
                    background: var(--bg-app-alt); 
                    border: 1px solid var(--border-prominent); 
                    padding: 6px 12px; 
                    border-radius: var(--radius-full); 
                    font-size: 0.85rem; 
                    cursor: pointer; 
                    color: var(--text-primary);
                    transition: all 0.2s ease;
                  "
                >
                  ➕ ${chip}
                </button>
              `).join('')}
            </div>
          </div>
        `;
      } catch (err) {
        console.error('Error parsing chips:', err);
      }
    }

    let evalHtml = '';
    if (this.evaluation) {
      const isHigh = this.evaluation.similarity_score >= 70 || this.evaluation.is_perfect;
      evalHtml = `
        <div style="margin-top: 24px; background: ${isHigh ? 'var(--olive-subtle)' : '#fffbeb'}; border: 2px solid ${isHigh ? 'var(--olive)' : 'var(--tuscan-gold)'}; border-radius: var(--radius-md); padding: 20px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <span style="font-weight: 800; color: ${isHigh ? 'var(--olive)' : 'var(--tuscan-gold)'}; font-size: 1.1rem;">
              ${this.evaluation.is_perfect ? '🌟 Flawless Italian!' : isHigh ? '✓ Great Job!' : '💡 Suggestions for Improvement'}
            </span>
            <span class="gram-badge" style="background: ${isHigh ? 'var(--olive)' : 'var(--tuscan-gold)'}; color: #ffffff;">
              +${this.evaluation.xp_awarded} XP
            </span>
          </div>

          <p style="color: var(--text-primary); font-size: 0.95rem; margin-bottom: 12px;">
            ${this.evaluation.feedback}
          </p>

          <div style="background: var(--bg-surface); padding: 14px 16px; border-radius: var(--radius-sm); border: 1px solid var(--border-subtle);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
              <span style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; color: var(--terracotta); letter-spacing: 0.05em;">
                Native Italian Model Solution:
              </span>
              <button class="audio-btn" style="width: 32px; height: 32px; font-size: 0.9rem;" onclick="window.soundEngine.speakItalian('${this.evaluation.sample_solution.replace(/'/g, "\\'")}')" title="Listen to model solution">
                🔊
              </button>
            </div>
            <div style="font-family: var(--font-serif); font-size: 1.05rem; font-weight: 600; color: var(--text-primary);">
              "${this.evaluation.sample_solution}"
            </div>
          </div>
        </div>
      `;
    }

    let html = `
      <div class="writing-view">
        <div style="margin-bottom: 24px; display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 12px;">
          <div>
            <h1 style="font-family: var(--font-serif); font-size: 2rem; margin-bottom: 4px; color: var(--text-primary);">
              Writing & Sentence Construction
            </h1>
            <p style="color: var(--text-secondary); font-size: 0.9rem;">
              Compose authentic sentences, experiment with Italian syntax, and receive immediate model comparison.
            </p>
          </div>

          <!-- Level Pills -->
          <div style="display: flex; gap: 8px;">
            <button class="nav-btn ${this.currentLevel === '' ? 'active' : ''}" onclick="window.writingView.setLevel('')">All</button>
            <button class="nav-btn ${this.currentLevel === 'A1' ? 'active' : ''}" onclick="window.writingView.setLevel('A1')">A1</button>
            <button class="nav-btn ${this.currentLevel === 'A2' ? 'active' : ''}" onclick="window.writingView.setLevel('A2')">A2</button>
            <button class="nav-btn ${this.currentLevel === 'B1' ? 'active' : ''}" onclick="window.writingView.setLevel('B1')">B1</button>
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 280px 1fr; gap: 24px; align-items: start;">
          
          <!-- Prompts Sidebar -->
          <div style="display: flex; flex-direction: column; gap: 8px; background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 14px; box-shadow: var(--shadow-sm);">
            <div style="font-size: 0.8rem; font-weight: 800; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.05em; margin-bottom: 6px;">
              Writing Prompts (${this.prompts.length})
            </div>
            ${this.prompts.map(p => `
              <div 
                onclick="window.writingView.selectPrompt(${p.id})"
                style="
                  padding: 12px 14px; 
                  border-radius: var(--radius-sm); 
                  cursor: pointer; 
                  background: ${prompt && prompt.id === p.id ? 'var(--terracotta-subtle)' : 'transparent'}; 
                  border: 1px solid ${prompt && prompt.id === p.id ? 'var(--terracotta)' : 'transparent'};
                  transition: all 0.2s ease;
                "
              >
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                  <span class="gram-badge" style="font-size: 0.65rem;">${p.level} &bull; ${p.category}</span>
                </div>
                <div style="font-weight: 700; font-size: 0.95rem; color: var(--text-primary);">
                  ${p.title}
                </div>
              </div>
            `).join('')}
          </div>

          <!-- Main Writing Area -->
          <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 32px; box-shadow: var(--shadow-sm);">
            ${prompt ? `
              <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 8px;">
                <span class="gram-badge" style="background: var(--tuscan-gold-subtle); color: var(--tuscan-gold); font-weight: 700;">Level ${prompt.level}</span>
                <span style="font-size: 0.85rem; color: var(--text-muted);">${prompt.category}</span>
              </div>

              <h2 style="font-family: var(--font-serif); font-size: 1.6rem; color: var(--text-primary); margin-bottom: 12px;">
                ${prompt.title}
              </h2>

              <div style="background: var(--bg-app-alt); border-left: 4px solid var(--terracotta); padding: 14px 18px; border-radius: 4px; color: var(--text-primary); font-size: 1rem; margin-bottom: 20px; line-height: 1.6;">
                <strong>Objective:</strong> ${prompt.task_prompt}
              </div>

              <!-- Starter Chips -->
              ${starterChipsHtml}

              <!-- Textarea for composing -->
              <div style="margin-top: 16px;">
                <label for="writing-textarea" style="display: block; font-weight: 700; font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 6px;">
                  Write your Italian sentence below:
                </label>
                <textarea 
                  id="writing-textarea"
                  class="form-control" 
                  rows="4" 
                  placeholder="Start typing or click the starter tiles above..."
                  style="width: 100%; font-size: 1.05rem; line-height: 1.6; font-family: var(--font-serif); padding: 14px;"
                  oninput="window.writingView.handleInput(event)"
                >${this.userText}</textarea>
              </div>

              <div style="margin-top: 18px; display: flex; justify-content: space-between; align-items: center;">
                <button class="btn-secondary" onclick="window.writingView.clearText()">
                  Clear Text
                </button>
                <button class="btn-tactile" onclick="window.writingView.submitEvaluation()" ${this.isEvaluating || !this.userText.trim() ? 'disabled' : ''}>
                  ${this.isEvaluating ? 'Evaluating...' : 'Submit Sentence & Evaluate (+25 XP)'}
                </button>
              </div>

              <!-- Evaluation Feedback -->
              ${evalHtml}

            ` : `
              <div style="text-align: center; padding: 40px; color: var(--text-muted);">
                Select a writing prompt from the sidebar.
              </div>
            `}
          </div>

        </div>
      </div>
    `;

    this.container.innerHTML = html;
  }

  setLevel(level) {
    this.currentLevel = level;
    this.activePrompt = null;
    this.evaluation = null;
    this.userText = '';
    this.render();
  }

  selectPrompt(promptId) {
    const found = this.prompts.find(p => p.id === promptId);
    if (found) {
      this.activePrompt = found;
      this.userText = '';
      this.evaluation = null;
      this.renderLayout();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  }

  handleInput(e) {
    this.userText = e.target.value;
  }

  appendChip(chipText) {
    if (window.soundEngine) window.soundEngine.playTap();
    if (this.userText && !this.userText.endsWith(' ')) {
      this.userText += ' ';
    }
    this.userText += chipText + ' ';
    const ta = document.getElementById('writing-textarea');
    if (ta) {
      ta.value = this.userText;
      ta.focus();
    }
  }

  clearText() {
    this.userText = '';
    this.evaluation = null;
    const ta = document.getElementById('writing-textarea');
    if (ta) ta.value = '';
    this.renderLayout();
  }

  async submitEvaluation() {
    if (!this.activePrompt || !this.userText.trim()) return;

    this.isEvaluating = true;
    this.renderLayout();

    try {
      const res = await window.api.evaluateWriting(this.activePrompt.id, this.userText);
      this.evaluation = res;
      this.isEvaluating = false;

      if (window.soundEngine) {
        if (res.is_perfect || res.similarity_score >= 70) {
          window.soundEngine.playCelebration();
          window.app.fireConfetti();
        } else {
          window.soundEngine.playSuccess();
        }
      }

      // Update XP bar
      const xpEl = document.getElementById('user-xp-val');
      if (xpEl && res.xp_awarded) {
        xpEl.innerText = parseInt(xpEl.innerText || '0', 10) + res.xp_awarded;
      }

      this.renderLayout();
    } catch (e) {
      this.isEvaluating = false;
      alert('Error evaluating sentence: ' + e.message);
      this.renderLayout();
    }
  }
}

window.WritingView = WritingView;
