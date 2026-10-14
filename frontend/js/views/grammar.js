/**
 * DAILY-ITALY — Grammar Mastery View (Grammar in Context)
 * English Interface with Italian Target Rules and Conjugation Tables
 */

class GrammarView {
  constructor(container) {
    this.container = container;
    this.currentLevel = '';
    this.activeLesson = null;
    this.lessons = [];
  }

  async render() {
    if (!window.api.user) {
      this.container.innerHTML = `
        <div class="auth-gate-card">
          <div class="auth-gate-icon">📖</div>
          <h2 style="font-family: var(--font-serif); font-size: 1.8rem; margin-bottom: 12px; color: var(--text-primary);">
            Italian Grammar in Context
          </h2>
          <p style="color: var(--text-secondary); max-width: 540px; margin: 0 auto 24px; line-height: 1.6;">
            Access comprehensive grammar rules, interactive conjugation tables, pronunciation of example sentences, and structured guides. Register or log in to get started.
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
        <p>Loading grammar topics...</p>
      </div>
    `;

    try {
      this.lessons = await window.api.getGrammarLessons(this.currentLevel);
      if (!this.activeLesson && this.lessons.length > 0) {
        this.activeLesson = await window.api.getGrammarLessonDetail(this.lessons[0].id);
      }
      this.renderLayout();
    } catch (e) {
      this.container.innerHTML = `
        <div style="text-align: center; padding: 40px; color: #ef4444;">
          <p>Error loading grammar: ${e.message}</p>
          <button class="btn-secondary" style="margin-top: 12px;" onclick="window.grammarView.render()">Try Again</button>
        </div>
      `;
    }
  }

  renderLayout() {
    const lesson = this.activeLesson;

    let tablesHtml = '';
    if (lesson && lesson.tables_json) {
      try {
        const tables = JSON.parse(lesson.tables_json);
        tablesHtml = tables.map(t => `
          <div style="margin: 20px 0; background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); overflow: hidden; box-shadow: var(--shadow-sm);">
            <div style="background: var(--bg-app-alt); padding: 12px 16px; font-weight: 700; font-family: var(--font-serif); font-size: 1rem; color: var(--terracotta);">
              ${t.title}
            </div>
            <div style="overflow-x: auto;">
              <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem;">
                <thead>
                  <tr style="border-bottom: 2px solid var(--border-subtle); background: var(--bg-surface);">
                    ${t.headers.map(h => `<th style="padding: 10px 14px; font-weight: 700; color: var(--text-secondary);">${h}</th>`).join('')}
                  </tr>
                </thead>
                <tbody>
                  ${t.rows.map(r => `
                    <tr style="border-bottom: 1px solid var(--border-subtle);">
                      ${r.map(cell => `<td style="padding: 10px 14px; color: var(--text-primary); font-family: monospace;">${cell}</td>`).join('')}
                    </tr>
                  `).join('')}
                </tbody>
              </table>
            </div>
          </div>
        `).join('');
      } catch (err) {
        console.error('Error parsing grammar tables:', err);
      }
    }

    let examplesHtml = '';
    if (lesson && lesson.examples_json) {
      try {
        const examples = JSON.parse(lesson.examples_json);
        examplesHtml = `
          <div style="margin-top: 24px;">
            <h3 style="font-family: var(--font-serif); font-size: 1.2rem; margin-bottom: 14px; color: var(--text-primary);">
              Example Sentences in Context
            </h3>
            <div style="display: flex; flex-direction: column; gap: 10px;">
              ${examples.map(ex => `
                <div style="display: flex; align-items: center; justify-content: space-between; background: var(--bg-surface); border: 1px solid var(--border-subtle); padding: 12px 16px; border-radius: var(--radius-md);">
                  <div>
                    <div style="font-weight: 600; color: var(--text-primary); font-size: 1rem;">${ex.it}</div>
                    <div style="color: var(--text-secondary); font-size: 0.85rem; margin-top: 2px;">${ex.en}</div>
                  </div>
                  <button class="audio-btn" style="width: 36px; height: 36px; font-size: 1rem; flex-shrink: 0;" onclick="window.soundEngine.speakItalian('${ex.it.replace(/'/g, "\\'")}')" title="Listen to pronunciation">
                    🔊
                  </button>
                </div>
              `).join('')}
            </div>
          </div>
        `;
      } catch (err) {
        console.error('Error parsing examples:', err);
      }
    }

    // Convert basic markdown in rules_markdown to clean HTML
    let rulesHtml = '';
    if (lesson && lesson.rules_markdown) {
      rulesHtml = lesson.rules_markdown
        .replace(/### (.*)/g, '<h3 style="font-family: var(--font-serif); font-size: 1.3rem; margin: 16px 0 8px; color: var(--text-primary);">$1</h3>')
        .replace(/#### (.*)/g, '<h4 style="font-size: 1.1rem; margin: 14px 0 6px; color: var(--terracotta);">$1</h4>')
        .replace(/> \*\*(.*?)\*\*(.*?)/g, '<div style="background: var(--terracotta-subtle); border-left: 4px solid var(--terracotta); padding: 10px 14px; border-radius: 4px; margin: 12px 0; font-size: 0.9rem;"><strong>$1</strong>$2</div>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/\n- (.*)/g, '<li style="margin-left: 20px; margin-bottom: 4px; color: var(--text-secondary);">$1</li>')
        .replace(/\n\n/g, '<p style="margin-bottom: 12px; line-height: 1.6; color: var(--text-secondary);"></p>');
    }

    let html = `
      <div class="grammar-view">
        <div style="margin-bottom: 24px; display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 12px;">
          <div>
            <h1 style="font-family: var(--font-serif); font-size: 2rem; margin-bottom: 4px; color: var(--text-primary);">
              Grammar in Context
            </h1>
            <p style="color: var(--text-secondary); font-size: 0.9rem;">
              From fundamental A1 structures to advanced Italian verb forms and syntax.
            </p>
          </div>

          <!-- Level Pills -->
          <div style="display: flex; gap: 8px;">
            <button class="nav-btn ${this.currentLevel === '' ? 'active' : ''}" onclick="window.grammarView.setLevel('')">All</button>
            <button class="nav-btn ${this.currentLevel === 'A1' ? 'active' : ''}" onclick="window.grammarView.setLevel('A1')">A1</button>
            <button class="nav-btn ${this.currentLevel === 'A2' ? 'active' : ''}" onclick="window.grammarView.setLevel('A2')">A2</button>
            <button class="nav-btn ${this.currentLevel === 'B1' ? 'active' : ''}" onclick="window.grammarView.setLevel('B1')">B1</button>
          </div>
        </div>

        <div style="display: grid; grid-template-columns: 280px 1fr; gap: 24px; align-items: start;">
          
          <!-- Lessons Sidebar -->
          <div style="display: flex; flex-direction: column; gap: 8px; background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 14px; box-shadow: var(--shadow-sm);">
            <div style="font-size: 0.8rem; font-weight: 800; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.05em; margin-bottom: 6px;">
              Topics (${this.lessons.length})
            </div>
            ${this.lessons.map(l => `
              <div 
                onclick="window.grammarView.selectLesson(${l.id})"
                style="
                  padding: 12px 14px; 
                  border-radius: var(--radius-sm); 
                  cursor: pointer; 
                  background: ${lesson && lesson.id === l.id ? 'var(--terracotta-subtle)' : 'transparent'}; 
                  border: 1px solid ${lesson && lesson.id === l.id ? 'var(--terracotta)' : 'transparent'};
                  transition: all 0.2s ease;
                "
              >
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
                  <span class="gram-badge" style="font-size: 0.65rem;">${l.level} &bull; ${l.category}</span>
                </div>
                <div style="font-weight: 700; font-size: 0.95rem; color: var(--text-primary);">
                  ${l.title}
                </div>
              </div>
            `).join('')}
          </div>

          <!-- Lesson Detail Content -->
          <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 32px; box-shadow: var(--shadow-sm);">
            ${lesson ? `
              <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 12px;">
                <span class="gram-badge" style="background: var(--olive-subtle); color: var(--olive); font-weight: 700;">Level ${lesson.level}</span>
                <span style="font-size: 0.85rem; color: var(--text-muted);">${lesson.category}</span>
              </div>

              <h2 style="font-family: var(--font-serif); font-size: 1.8rem; color: var(--text-primary); margin-bottom: 16px;">
                ${lesson.title}
              </h2>

              ${lesson.summary ? `
                <div style="background: var(--bg-app-alt); border-left: 4px solid var(--amalfi-blue); padding: 12px 16px; border-radius: 4px; color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 24px;">
                  ${lesson.summary}
                </div>
              ` : ''}

              <!-- Rules & Explanations -->
              <div style="font-size: 0.95rem; line-height: 1.7; color: var(--text-primary);">
                ${rulesHtml}
              </div>

              <!-- Conjugation & Grammatical Tables -->
              ${tablesHtml}

              <!-- Real-world Examples with Audio -->
              ${examplesHtml}

              <!-- Action Bar -->
              <div style="margin-top: 36px; padding-top: 20px; border-top: 1px solid var(--border-subtle); display: flex; justify-content: space-between; align-items: center;">
                <button class="btn-secondary" onclick="window.soundEngine.playSuccess(); window.app.triggerConfetti();" title="Mark as understood">
                  ✓ Rule Understood (+15 XP)
                </button>
                <button class="btn-tactile" onclick="window.app.switchView('writing')">
                  ✍️ Practice Writing &rarr;
                </button>
              </div>

            ` : `
              <div style="text-align: center; padding: 40px; color: var(--text-muted);">
                Select a grammar topic from the sidebar.
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
    this.activeLesson = null;
    this.render();
  }

  async selectLesson(lessonId) {
    try {
      this.activeLesson = await window.api.getGrammarLessonDetail(lessonId);
      this.renderLayout();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (e) {
      console.error('Error fetching grammar lesson detail:', e);
    }
  }
}

window.GrammarView = GrammarView;
