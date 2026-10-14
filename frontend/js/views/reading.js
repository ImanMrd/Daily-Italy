/**
 * DAILY-ITALY — Readings & Comprehension View (Letture & Dialoghi)
 * English Interface with Authentic Italian Target Narratives & Audio
 */

class ReadingView {
  constructor(container) {
    this.container = container;
    this.currentLevel = '';
    this.activePassage = null;
    this.passages = [];
    this.showEnglish = false;
    this.selectedAnswers = {}; // { question_index: selected_option }
    this.submissionResult = null;
  }

  async render() {
    if (!window.api.user) {
      this.container.innerHTML = `
        <div class="auth-gate-card">
          <div class="auth-gate-icon">📚</div>
          <h2 style="font-family: var(--font-serif); font-size: 1.8rem; margin-bottom: 12px; color: var(--text-primary);">
            Italian Readings & Dialogue Comprehension
          </h2>
          <p style="color: var(--text-secondary); max-width: 540px; margin: 0 auto 24px; line-height: 1.6;">
            Immerse yourself in authentic stories and daily dialogues with native voice narration, vocabulary notes, and comprehension questions. Log in or create an account to continue.
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
        <p>Loading reading passages...</p>
      </div>
    `;

    try {
      this.passages = await window.api.getReadingPassages(this.currentLevel);
      if (!this.activePassage && this.passages.length > 0) {
        this.activePassage = await window.api.getReadingPassageDetail(this.passages[0].id);
      }
      this.renderLayout();
    } catch (e) {
      this.container.innerHTML = `
        <div style="text-align: center; padding: 40px; color: #ef4444;">
          <p>Error loading readings: ${e.message}</p>
          <button class="btn-secondary" style="margin-top: 12px;" onclick="window.readingView.render()">Try Again</button>
        </div>
      `;
    }
  }

  renderLayout() {
    const passage = this.activePassage;

    let vocabHintsHtml = '';
    if (passage && passage.vocabulary_hints_json) {
      try {
        const hints = JSON.parse(passage.vocabulary_hints_json);
        vocabHintsHtml = `
          <div style="margin: 24px 0; background: var(--bg-app-alt); border-radius: var(--radius-md); padding: 18px 20px;">
            <div style="font-size: 0.8rem; font-weight: 800; text-transform: uppercase; color: var(--terracotta); letter-spacing: 0.05em; margin-bottom: 10px;">
              💡 Key Vocabulary & Lexical Notes
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
              ${hints.map(h => `
                <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); padding: 6px 12px; border-radius: var(--radius-sm); font-size: 0.85rem;">
                  <strong style="color: var(--text-primary); font-family: var(--font-serif);">${h.term}</strong>: 
                  <span style="color: var(--text-secondary);">${h.en}</span>
                </div>
              `).join('')}
            </div>
          </div>
        `;
      } catch (err) {
        console.error('Error parsing vocab hints:', err);
      }
    }

    let questionsHtml = '';
    if (passage && passage.questions_json) {
      try {
        const questions = JSON.parse(passage.questions_json);
        questionsHtml = `
          <div style="margin-top: 36px; padding-top: 24px; border-top: 2px solid var(--border-subtle);">
            <h3 style="font-family: var(--font-serif); font-size: 1.4rem; color: var(--text-primary); margin-bottom: 16px;">
              ❓ Comprehension Check
            </h3>
            <div style="display: flex; flex-direction: column; gap: 20px;">
              ${questions.map((q, idx) => {
                const selected = this.selectedAnswers[idx];
                const res = this.submissionResult ? this.submissionResult.details[idx] : null;

                return `
                  <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 18px; box-shadow: var(--shadow-sm);">
                    <div style="font-weight: 700; font-size: 1rem; color: var(--text-primary); margin-bottom: 12px;">
                      ${idx + 1}. ${q.question}
                    </div>

                    <div style="display: grid; grid-template-columns: 1fr; gap: 8px;">
                      ${q.options.map(opt => {
                        const isChosen = selected === opt;
                        let btnStyle = 'background: var(--bg-surface); border: 1px solid var(--border-prominent);';
                        if (isChosen) {
                          btnStyle = 'background: var(--terracotta-subtle); border: 2px solid var(--terracotta); font-weight: 700;';
                        }
                        if (res) {
                          if (opt === res.correct_answer) {
                            btnStyle = 'background: var(--olive-subtle); border: 2px solid var(--olive); color: var(--olive); font-weight: 700;';
                          } else if (isChosen && !res.correct) {
                            btnStyle = 'background: #fee2e2; border: 2px solid #ef4444; color: #991b1b;';
                          }
                        }

                        return `
                          <button 
                            type="button"
                            onclick="window.readingView.selectOption(${idx}, '${opt.replace(/'/g, "\\'")}')"
                            style="text-align: left; padding: 12px 16px; border-radius: var(--radius-sm); cursor: pointer; transition: all 0.2s ease; ${btnStyle}"
                            ${this.submissionResult ? 'disabled' : ''}
                          >
                            ${opt}
                          </button>
                        `;
                      }).join('')}
                    </div>

                    ${res ? `
                      <div style="margin-top: 12px; font-size: 0.85rem; padding: 10px; border-radius: 6px; background: ${res.correct ? 'var(--olive-subtle)' : '#fee2e2'}; color: ${res.correct ? 'var(--olive)' : '#991b1b'};">
                        <strong>${res.correct ? '✓ Correct!' : '✗ Incorrect answer.'}</strong> ${res.explanation || ''}
                      </div>
                    ` : ''}
                  </div>
                `;
              }).join('')}
            </div>

            <div style="margin-top: 24px; text-align: right;">
              ${!this.submissionResult ? `
                <button class="btn-tactile" onclick="window.readingView.submitAnswers()">
                  Verify Answers & Earn XP
                </button>
              ` : `
                <div style="display: flex; justify-content: space-between; align-items: center; background: var(--olive-subtle); padding: 16px 20px; border-radius: var(--radius-md);">
                  <div style="color: var(--olive); font-weight: 700; font-size: 1.1rem;">
                    Score: ${this.submissionResult.correct_count} / ${this.submissionResult.total} (+${this.submissionResult.xp_awarded} XP)
                  </div>
                  <button class="btn-secondary" onclick="window.readingView.resetQuiz()">
                    Retake Quiz
                  </button>
                </div>
              `}
            </div>
          </div>
        `;
      } catch (err) {
        console.error('Error parsing questions:', err);
      }
    }

    let html = `
      <div class="reading-view">
        <div style="margin-bottom: 24px; display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 12px;">
          <div>
            <h1 style="font-family: var(--font-serif); font-size: 2rem; margin-bottom: 4px; color: var(--text-primary);">
              Readings & Dialogues
            </h1>
            <p style="color: var(--text-secondary); font-size: 0.9rem;">
              Develop reading fluency and cultural insight through authentic Italian dialogues and narratives.
            </p>
          </div>

          <!-- Level Pills -->
          <div style="display: flex; gap: 8px;">
            <button class="nav-btn ${this.currentLevel === '' ? 'active' : ''}" onclick="window.readingView.setLevel('')">All</button>
            <button class="nav-btn ${this.currentLevel === 'A1' ? 'active' : ''}" onclick="window.readingView.setLevel('A1')">A1</button>
            <button class="nav-btn ${this.currentLevel === 'A2' ? 'active' : ''}" onclick="window.readingView.setLevel('A2')">A2</button>
            <button class="nav-btn ${this.currentLevel === 'B1' ? 'active' : ''}" onclick="window.readingView.setLevel('B1')">B1</button>
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 280px 1fr; gap: 24px; align-items: start;">
          
          <!-- Passages Sidebar -->
          <div style="display: flex; flex-direction: column; gap: 8px; background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 14px; box-shadow: var(--shadow-sm);">
            <div style="font-size: 0.8rem; font-weight: 800; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.05em; margin-bottom: 6px;">
              Available Passages (${this.passages.length})
            </div>
            ${this.passages.map(p => `
              <div 
                onclick="window.readingView.selectPassage(${p.id})"
                style="
                  padding: 12px 14px; 
                  border-radius: var(--radius-sm); 
                  cursor: pointer; 
                  background: ${passage && passage.id === p.id ? 'var(--terracotta-subtle)' : 'transparent'}; 
                  border: 1px solid ${passage && passage.id === p.id ? 'var(--terracotta)' : 'transparent'};
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

          <!-- Main Passage Reader -->
          <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 32px; box-shadow: var(--shadow-sm);">
            ${passage ? `
              <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 14px; flex-wrap: wrap; gap: 10px;">
                <div>
                  <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 8px;">
                    <span class="gram-badge" style="background: var(--amalfi-subtle); color: var(--amalfi-deep); font-weight: 700;">Level ${passage.level}</span>
                    <span style="font-size: 0.85rem; color: var(--text-muted);">${passage.category}</span>
                  </div>
                  <h2 style="font-family: var(--font-serif); font-size: 1.8rem; color: var(--text-primary);">
                    ${passage.title}
                  </h2>
                </div>

                <!-- Controls: Audio & Translation Toggle -->
                <div style="display: flex; gap: 10px; align-items: center;">
                  <button class="audio-btn" style="width: 44px; height: 44px; font-size: 1.2rem;" onclick="window.readingView.readAloud()" title="Listen to audio narration">
                    🔊
                  </button>
                  <button class="btn-secondary" style="padding: 8px 14px; font-size: 0.85rem;" onclick="window.readingView.toggleEnglish()">
                    ${this.showEnglish ? 'Hide English Translation' : 'Show English Translation'}
                  </button>
                </div>
              </div>

              <!-- Italian Content -->
              <div style="font-size: 1.05rem; line-height: 1.85; color: var(--text-primary); font-family: var(--font-serif); white-space: pre-line; background: var(--bg-surface-hover); padding: 24px; border-radius: var(--radius-md); border: 1px solid var(--border-subtle);">
                ${passage.content_it}
              </div>

              <!-- Optional English Translation -->
              ${this.showEnglish && passage.content_en ? `
                <div style="margin-top: 16px; font-size: 0.95rem; line-height: 1.7; color: var(--text-secondary); background: var(--bg-app-alt); padding: 20px; border-radius: var(--radius-md); white-space: pre-line; border-left: 4px solid var(--terracotta);">
                  <div style="font-weight: 700; margin-bottom: 6px; color: var(--terracotta-dark); font-size: 0.8rem; text-transform: uppercase;">English Translation:</div>
                  ${passage.content_en}
                </div>
              ` : ''}

              <!-- Vocab hints -->
              ${vocabHintsHtml}

              <!-- Comprehension Quiz -->
              ${questionsHtml}

            ` : `
              <div style="text-align: center; padding: 40px; color: var(--text-muted);">
                Select a reading passage from the sidebar.
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
    this.activePassage = null;
    this.selectedAnswers = {};
    this.submissionResult = null;
    this.render();
  }

  async selectPassage(passageId) {
    try {
      this.activePassage = await window.api.getReadingPassageDetail(passageId);
      this.selectedAnswers = {};
      this.submissionResult = null;
      this.showEnglish = false;
      this.renderLayout();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (e) {
      console.error('Error fetching reading passage detail:', e);
    }
  }

  toggleEnglish() {
    this.showEnglish = !this.showEnglish;
    this.renderLayout();
  }

  readAloud() {
    if (!this.activePassage) return;
    if (window.soundEngine) {
      window.soundEngine.speakItalian(this.activePassage.content_it);
    }
  }

  selectOption(questionIdx, option) {
    if (this.submissionResult) return;
    this.selectedAnswers[questionIdx] = option;
    if (window.soundEngine) window.soundEngine.playTap();
    this.renderLayout();
  }

  async submitAnswers() {
    if (!this.activePassage) return;

    try {
      const result = await window.api.submitReadingAnswers(this.activePassage.id, this.selectedAnswers);
      this.submissionResult = result;

      if (window.soundEngine) {
        if (result.correct_count === result.total) {
          window.soundEngine.playCelebration();
          window.app.triggerConfetti();
        } else {
          window.soundEngine.playSuccess();
        }
      }

      // Update XP bar
      const xpEl = document.getElementById('user-xp-val');
      if (xpEl && result.xp_awarded) {
        xpEl.innerText = parseInt(xpEl.innerText || '0', 10) + result.xp_awarded;
      }

      this.renderLayout();
    } catch (e) {
      alert('Error submitting answers: ' + e.message);
    }
  }

  resetQuiz() {
    this.selectedAnswers = {};
    this.submissionResult = null;
    this.renderLayout();
  }
}

window.ReadingView = ReadingView;
