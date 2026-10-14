/**
 * DAILY-ITALY — CEFR Curriculum & Chapter Studio View
 * Levels: A1 (10 Chapters), A2 (10 Chapters), B1 (20 Chapters), B2 (20 Chapters) = 60 Chapters
 * Features: Sequential progression, Placement Tests (>= 70% unlock), 4-part Chapter Studio
 */

class RoadmapView {
  constructor(container) {
    this.container = container;
    this.currentLevel = 'A1';
    this.activeChapter = null;
    this.activeStudioTab = 'vocab'; // 'vocab', 'grammar', 'reading', 'writing', 'quiz'
    this.levelsData = [];
    this.readingTranslationVisible = false;
    this.writingModelVisible = false;
    this.quizAnswers = {};
    this.readingQuizAnswers = {};
    this.readingEvaluations = {};
    this.writingDraft = '';
    this.chapterExerciseAnswers = {};
    this.chapterExerciseEvaluations = {};
  }

  async render() {
    if (!window.api.user) {
      this.container.innerHTML = `
        <div class="auth-gate-card">
          <div class="auth-gate-icon">🗺️</div>
          <h2 style="font-family: var(--font-serif); font-size: 1.8rem; margin-bottom: 12px; color: var(--text-primary);">
            Italian Curriculum & Chapter Progression
          </h2>
          <p style="color: var(--text-secondary); max-width: 540px; margin: 0 auto 24px; line-height: 1.6;">
            Access all 60 CEFR-aligned chapters across A1, A2, B1, and B2. Each chapter includes 4 dedicated sections: Vocabulary Flashcards, Grammar Rules, Reading Dialogues, and Writing Practice. Log in or create an account to start your journey.
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

    if (this.activeChapter) {
      this.renderChapterStudio();
      return;
    }

    this.container.innerHTML = `
      <div style="text-align: center; padding: 40px; color: var(--text-secondary);">
        <p>Loading Italian curriculum overview...</p>
      </div>
    `;

    try {
      this.levelsData = await window.api.getChaptersOverview();
      this.renderOverview();
    } catch (e) {
      this.container.innerHTML = `
        <div style="text-align: center; padding: 40px; color: #ef4444;">
          <p>Error loading curriculum: ${e.message}</p>
          <button class="btn-secondary" style="margin-top: 12px;" onclick="window.roadmapView.render()">Try Again</button>
        </div>
      `;
    }
  }

  setLevel(level) {
    this.currentLevel = level;
    this.activeChapter = null;
    this.render();
  }

  renderOverview() {
    const activeLevelData = this.levelsData.find(l => l.level === this.currentLevel) || this.levelsData[0];
    if (!activeLevelData) return;

    const levelDescriptions = {
      'A1': 'Beginner — Foundations, greetings, essential verbs (essere, avere, chiamarsi), numbers, and daily survival phrases.',
      'A2': 'Elementary — Daily routines, past actions (passato prossimo), travel, food, directions, and reflexive verbs.',
      'B1': 'Intermediate — Narratives (imperfetto vs passato prossimo), future plans, opinions, work, culture, and conditionals.',
      'B2': 'Upper-Intermediate — Subjunctive mood (congiuntivo), idioms, complex debate, hypothetical periods, and nuances.'
    };

    let html = `
      <div class="roadmap-header" style="margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 12px; margin-bottom: 16px;">
          <div>
            <div class="hero-pill" style="margin-bottom: 8px;">
              🇮🇹 CEFR Structured Curriculum (60 Chapters)
            </div>
            <h1 style="font-family: var(--font-serif); font-size: 2.2rem; color: var(--text-primary); margin-bottom: 4px;">
              Chapters & Progression
            </h1>
            <p style="color: var(--text-secondary); font-size: 0.95rem; max-width: 680px;">
              Each chapter consists of 4 parts: <strong>Vocab</strong>, <strong>Grammar</strong>, <strong>Reading</strong>, and <strong>Writing</strong>. Complete each chapter sequentially or take a placement test to unlock advanced levels.
            </p>
          </div>
        </div>

        <!-- Level Selector Tabs -->
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 24px;">
    `;

    this.levelsData.forEach(lvl => {
      const isSelected = lvl.level === this.currentLevel;
      const isUnlocked = lvl.is_unlocked;
      const pct = Math.round((lvl.completed_chapters / Math.max(lvl.total_chapters, 1)) * 100);

      html += `
        <button 
          onclick="window.roadmapView.setLevel('${lvl.level}')"
          style="
            background: ${isSelected ? 'var(--bg-surface)' : 'var(--bg-app-alt)'};
            border: 2px solid ${isSelected ? 'var(--terracotta)' : 'var(--border-subtle)'};
            border-radius: var(--radius-md);
            padding: 14px 16px;
            text-align: left;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: ${isSelected ? 'var(--shadow-md)' : 'none'};
          "
        >
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
            <span style="font-family: var(--font-serif); font-weight: 800; font-size: 1.15rem; color: ${isSelected ? 'var(--terracotta)' : 'var(--text-primary)'};">
              Level ${lvl.level}
            </span>
            <span style="font-size: 0.85rem;">${isUnlocked ? '🔓' : '🔒'}</span>
          </div>
          <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 8px;">
            ${lvl.total_chapters} Chapters &bull; ${lvl.completed_chapters} Done
          </div>
          <div style="height: 4px; background: var(--border-prominent); border-radius: var(--radius-full); overflow: hidden;">
            <div style="width: ${pct}%; height: 100%; background: var(--olive); transition: width 0.3s ease;"></div>
          </div>
        </button>
      `;
    });

    html += `
        </div>
      </div>
    `;

    // Active Level Banner / Placement Prompt
    if (!activeLevelData.is_unlocked) {
      html += `
        <div style="background: linear-gradient(135deg, #fffbeb, #fef3c7); border: 2px dashed #f59e0b; border-radius: var(--radius-lg); padding: 28px; margin-bottom: 32px; box-shadow: var(--shadow-sm);">
          <div style="display: flex; gap: 20px; align-items: center; flex-wrap: wrap;">
            <div style="font-size: 3rem;">🔒</div>
            <div style="flex: 1; min-width: 260px;">
              <h2 style="font-family: var(--font-serif); font-size: 1.4rem; color: #92400e; margin-bottom: 6px;">
                Level ${activeLevelData.level} is Currently Locked
              </h2>
              <p style="color: #78350f; font-size: 0.92rem; line-height: 1.5; margin-bottom: 16px;">
                You can unlock this level naturally by completing the preceding level chapters, OR take the <strong>10-Question Placement Test</strong> right now. Scoring <strong>70% or higher</strong> instantly unlocks all ${activeLevelData.total_chapters} chapters of Level ${activeLevelData.level}!
              </p>
              <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                <button class="btn-tactile" style="background: #d97706;" onclick="window.app.openPlacementModal('${activeLevelData.level}')">
                  📝 Take Level ${activeLevelData.level} Placement Test (Min. 70%)
                </button>
              </div>
            </div>
          </div>
        </div>
      `;
    } else {
      const pct = Math.round((activeLevelData.completed_chapters / Math.max(activeLevelData.total_chapters, 1)) * 100);
      html += `
        <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: 20px 24px; margin-bottom: 28px; box-shadow: var(--shadow-sm);">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 12px; margin-bottom: 8px;">
            <div>
              <span class="stage-level-tag" style="margin-right: 8px;">LEVEL ${activeLevelData.level}</span>
              <strong style="color: var(--text-primary); font-size: 1.05rem;">Level Unlocked & Active</strong>
            </div>
            <span style="font-size: 0.85rem; font-weight: 700; color: var(--olive);">
              ${activeLevelData.completed_chapters} / ${activeLevelData.total_chapters} Chapters Completed (${pct}%)
            </span>
          </div>
          <p style="color: var(--text-secondary); font-size: 0.88rem; margin-bottom: 12px;">
            ${levelDescriptions[activeLevelData.level] || ''}
          </p>
          <div style="height: 6px; background: var(--bg-app-alt); border-radius: var(--radius-full); overflow: hidden;">
            <div style="width: ${pct}%; height: 100%; background: var(--olive); transition: width 0.3s ease;"></div>
          </div>
        </div>
      `;
    }

    // Chapters Grid
    html += `
      <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 18px; margin-bottom: 40px;">
    `;

    activeLevelData.chapters.forEach(ch => {
      const isLocked = !ch.is_unlocked;
      const isCompleted = ch.is_completed;
      const partsDone = [ch.vocab_done, ch.grammar_done, ch.reading_done, ch.writing_done].filter(Boolean).length;

      html += `
        <div 
          style="
            background: var(--bg-surface);
            border: 2px solid ${isCompleted ? 'var(--olive)' : (isLocked ? 'var(--border-subtle)' : 'var(--border-prominent)')};
            border-radius: var(--radius-lg);
            padding: 22px;
            box-shadow: ${isLocked ? 'none' : 'var(--shadow-sm)'};
            opacity: ${isLocked ? '0.72' : '1'};
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            position: relative;
            transition: all 0.2s ease;
          "
        >
          <div>
            <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
              <span style="
                display: inline-block;
                background: ${isCompleted ? 'var(--olive-subtle)' : 'var(--bg-app-alt)'};
                color: ${isCompleted ? 'var(--olive)' : 'var(--text-secondary)'};
                font-size: 0.75rem;
                font-weight: 800;
                padding: 4px 10px;
                border-radius: var(--radius-full);
                letter-spacing: 0.05em;
              ">
                CHAPTER ${ch.chapter_number}
              </span>
              <span style="font-size: 0.85rem;">
                ${isCompleted ? '✅ Mastered' : (isLocked ? '🔒 Locked' : `⚡ ${partsDone}/4 Parts`)}
              </span>
            </div>

            <h3 style="font-family: var(--font-serif); font-size: 1.15rem; color: var(--text-primary); margin-bottom: 6px;">
              ${ch.title}
            </h3>
            <p style="color: var(--text-secondary); font-size: 0.85rem; line-height: 1.4; margin-bottom: 16px;">
              ${ch.description || 'Vocabulary, grammar rules, cultural reading dialogue, and sentence construction.'}
            </p>

            <!-- 4 Parts Status Indicators -->
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin-bottom: 20px;">
              <div title="15 High-Frequency Words" style="text-align: center; font-size: 0.72rem; padding: 4px; border-radius: var(--radius-sm); background: ${ch.vocab_done ? 'var(--olive-subtle)' : 'var(--bg-app-alt)'}; color: ${ch.vocab_done ? 'var(--olive)' : 'var(--text-muted)'}; font-weight: 700;">
                🃏 Vocab
              </div>
              <div title="Grammar & Conjugation" style="text-align: center; font-size: 0.72rem; padding: 4px; border-radius: var(--radius-sm); background: ${ch.grammar_done ? 'var(--olive-subtle)' : 'var(--bg-app-alt)'}; color: ${ch.grammar_done ? 'var(--olive)' : 'var(--text-muted)'}; font-weight: 700;">
                📖 Gram
              </div>
              <div title="Cultural Dialogue & Quiz" style="text-align: center; font-size: 0.72rem; padding: 4px; border-radius: var(--radius-sm); background: ${ch.reading_done ? 'var(--olive-subtle)' : 'var(--bg-app-alt)'}; color: ${ch.reading_done ? 'var(--olive)' : 'var(--text-muted)'}; font-weight: 700;">
                📚 Read
              </div>
              <div title="Writing & Composition" style="text-align: center; font-size: 0.72rem; padding: 4px; border-radius: var(--radius-sm); background: ${ch.writing_done ? 'var(--olive-subtle)' : 'var(--bg-app-alt)'}; color: ${ch.writing_done ? 'var(--olive)' : 'var(--text-muted)'}; font-weight: 700;">
                ✍️ Write
              </div>
            </div>
          </div>

          <div>
            ${isLocked ? `
              <button class="btn-secondary" disabled style="width: 100%; justify-content: center; opacity: 0.6; cursor: not-allowed; font-size: 0.85rem;">
                🔒 Complete Chapter ${ch.chapter_number - 1} First
              </button>
            ` : `
              <button class="btn-tactile" style="width: 100%; justify-content: center; font-size: 0.88rem;" onclick="window.roadmapView.openChapter(${ch.id})">
                ${isCompleted ? '🔄 Review Chapter' : '🚀 Open Chapter Studio'}
              </button>
            `}
          </div>
        </div>
      `;
    });

    html += `</div>`;
    this.container.innerHTML = html;
  }

  async openChapter(chapterId) {
    this.container.innerHTML = `
      <div style="text-align: center; padding: 50px; color: var(--text-secondary);">
        <p>Loading Chapter Studio...</p>
      </div>
    `;

    try {
      this.activeChapter = await window.api.getChapterDetail(chapterId);
      this.activeStudioTab = 'vocab';
      this.readingTranslationVisible = false;
      this.writingModelVisible = false;
      this.quizAnswers = {};
      this.readingQuizAnswers = {};
      this.renderChapterStudio();
    } catch (e) {
      alert(`Error opening chapter: ${e.message}`);
      this.activeChapter = null;
      this.render();
    }
  }

  closeChapter() {
    this.activeChapter = null;
    this.readingQuizAnswers = {};
    this.readingEvaluations = {};
    this.writingDraft = '';
    this.chapterExerciseAnswers = {};
    this.chapterExerciseEvaluations = {};
    this.render();
  }

  setStudioTab(tab) {
    this.activeStudioTab = tab;
    this.renderChapterStudio();
  }

  async markPartDone(part, extra = {}) {
    if (!this.activeChapter) return;
    try {
      const res = await window.api.completeChapterPart(this.activeChapter.id, part, extra);
      this.activeChapter.vocab_done = res.vocab_done;
      this.activeChapter.grammar_done = res.grammar_done;
      this.activeChapter.reading_done = res.reading_done;
      this.activeChapter.writing_done = res.writing_done;
      this.activeChapter.is_completed = res.chapter_completed;

      window.soundEngine.playSuccess();
      if (res.chapter_completed) {
        window.app.triggerConfetti();
      }

      await window.api.fetchCurrentUser();
      window.app.updateUserStatsBar();
      this.renderChapterStudio();
      return res;
    } catch (e) {
      alert(`Error saving progress: ${e.message}`);
      throw e;
    }
  }

  renderChapterStudio() {
    const ch = this.activeChapter;
    if (!ch) return;

    const partsDone = [ch.vocab_done, ch.grammar_done, ch.reading_done, ch.writing_done].filter(Boolean).length;
    const pct = Math.round((partsDone / 4) * 100);

    let html = `
      <div class="chapter-studio" style="max-width: 900px; margin: 0 auto 50px;">
        
        <!-- Header & Back Button -->
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 12px;">
          <button class="btn-secondary" onclick="window.roadmapView.closeChapter()" style="padding: 6px 14px; font-size: 0.85rem;">
            ← Back to Chapters Overview
          </button>
          <div style="font-size: 0.85rem; font-weight: 700; color: ${ch.is_completed ? 'var(--olive)' : 'var(--text-secondary)'};">
            ${ch.is_completed ? '🎉 Chapter Mastered (100%)' : `Progress: ${partsDone} / 4 Sections Complete (${pct}%)`}
          </div>
        </div>

        <!-- Chapter Title Card -->
        <div style="background: var(--bg-surface); border: 2px solid var(--border-prominent); border-radius: var(--radius-lg); padding: 24px 28px; margin-bottom: 24px; box-shadow: var(--shadow-sm);">
          <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 8px;">
            <span class="stage-level-tag">LEVEL ${ch.level} &bull; CHAPTER ${ch.chapter_number}</span>
          </div>
          <h1 style="font-family: var(--font-serif); font-size: 2rem; color: var(--text-primary); margin-bottom: 6px;">
            ${ch.title}
          </h1>
          <p style="color: var(--text-secondary); font-size: 0.95rem;">
            ${ch.description || 'Master the essential vocabulary, grammar structures, reading dialogue, and writing exercises.'}
          </p>

          <div style="height: 6px; background: var(--bg-app-alt); border-radius: var(--radius-full); overflow: hidden; margin-top: 16px;">
            <div style="width: ${pct}%; height: 100%; background: var(--olive); transition: width 0.3s ease;"></div>
          </div>
        </div>

        <!-- Studio Section Tabs -->
        <div style="display: flex; gap: 8px; margin-bottom: 24px; overflow-x: auto; padding-bottom: 4px;">
          <button 
            class="nav-btn ${this.activeStudioTab === 'vocab' ? 'active' : ''}" 
            onclick="window.roadmapView.setStudioTab('vocab')"
            style="padding: 10px 16px; font-size: 0.9rem;"
          >
            🃏 1. Vocabulary (${ch.words.length}) ${ch.vocab_done ? '✓' : ''}
          </button>
          <button 
            class="nav-btn ${this.activeStudioTab === 'grammar' ? 'active' : ''}" 
            onclick="window.roadmapView.setStudioTab('grammar')"
            style="padding: 10px 16px; font-size: 0.9rem;"
          >
            📖 2. Grammar Rules ${ch.grammar_done ? '✓' : ''}
          </button>
          <button 
            class="nav-btn ${this.activeStudioTab === 'reading' ? 'active' : ''}" 
            onclick="window.roadmapView.setStudioTab('reading')"
            style="padding: 10px 16px; font-size: 0.9rem;"
          >
            📚 3. Reading Dialogue ${ch.reading_done ? '✓' : ''}
          </button>
          <button 
            class="nav-btn ${this.activeStudioTab === 'writing' ? 'active' : ''}" 
            onclick="window.roadmapView.setStudioTab('writing')"
            style="padding: 10px 16px; font-size: 0.9rem;"
          >
            ✍️ 4. Writing Lab ${ch.writing_done ? '✓' : ''}
          </button>
          <button 
            class="nav-btn ${this.activeStudioTab === 'quiz' ? 'active' : ''}" 
            onclick="window.roadmapView.setStudioTab('quiz')"
            style="padding: 10px 16px; font-size: 0.9rem;"
          >
            🎯 5. Consolidation Quiz (${ch.exercises.length})
          </button>
        </div>
    `;

    // Tab Body Rendering
    if (this.activeStudioTab === 'vocab') {
      html += this.renderVocabTab(ch);
    } else if (this.activeStudioTab === 'grammar') {
      html += this.renderGrammarTab(ch);
    } else if (this.activeStudioTab === 'reading') {
      html += this.renderReadingTab(ch);
    } else if (this.activeStudioTab === 'writing') {
      html += this.renderWritingTab(ch);
    } else if (this.activeStudioTab === 'quiz') {
      html += this.renderQuizTab(ch);
    }

    html += `</div>`;
    this.container.innerHTML = html;
  }

  // 1. Vocabulary Tab
  renderVocabTab(ch) {
    let html = `
      <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: 28px; box-shadow: var(--shadow-sm);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
          <div>
            <h2 style="font-family: var(--font-serif); font-size: 1.4rem; color: var(--text-primary);">
              High-Frequency Vocabulary (${ch.words.length} Words)
            </h2>
            <p style="color: var(--text-secondary); font-size: 0.88rem;">
              Click the audio icon to listen to native Italian pronunciation. Review both the Italian term and its context sentence.
            </p>
          </div>
          <button 
            class="btn-tactile" 
            style="padding: 8px 16px; font-size: 0.85rem;"
            onclick="window.roadmapView.markPartDone('vocab')"
          >
            ${ch.vocab_done ? '✓ Vocab Completed' : '✅ Mark Vocab Complete (+10 XP)'}
          </button>
        </div>

        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 14px; margin-bottom: 28px;">
    `;

    ch.words.forEach(w => {
      html += `
        <div style="background: var(--bg-app-alt); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 16px; position: relative;">
          <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 6px;">
            <strong style="font-family: var(--font-serif); font-size: 1.3rem; color: var(--text-primary);">
              ${w.italian}
            </strong>
            <button 
              class="audio-btn" 
              style="width: 32px; height: 32px; font-size: 0.85rem;"
              onclick="window.soundEngine.speakItalian('${w.italian.replace(/'/g, "\\'")}')"
              title="Listen to pronunciation"
            >
              🔊
            </button>
          </div>

          <div style="display: flex; gap: 6px; align-items: center; margin-bottom: 8px;">
            <span class="gram-badge" style="font-size: 0.72rem;">${w.word_type || 'Word'}</span>
            ${w.pronunciation ? `<span style="font-size: 0.75rem; color: var(--text-muted); font-style: italic;">[${w.pronunciation}]</span>` : ''}
          </div>

          <div style="font-size: 0.95rem; font-weight: 700; color: var(--terracotta); margin-bottom: 8px;">
            ${w.english}
          </div>

          ${w.example_it ? `
            <div style="border-top: 1px solid var(--border-prominent); padding-top: 8px; font-size: 0.82rem;">
              <div style="color: var(--text-primary); font-style: italic; margin-bottom: 2px;">
                "${w.example_it}"
              </div>
              <div style="color: var(--text-muted);">
                "${w.example_en || ''}"
              </div>
            </div>
          ` : ''}
        </div>
      `;
    });

    html += `
        </div>

        <div style="text-align: center; border-top: 1px solid var(--border-subtle); padding-top: 20px;">
          <button 
            class="btn-tactile" 
            style="padding: 12px 28px; font-size: 0.95rem;"
            onclick="window.roadmapView.markPartDone('vocab'); window.roadmapView.setStudioTab('grammar');"
          >
            ${ch.vocab_done ? 'Next Section: Grammar →' : 'Save Vocab & Continue to Grammar →'}
          </button>
        </div>
      </div>
    `;

    return html;
  }

  // 2. Grammar Tab
  renderGrammarTab(ch) {
    let tablesHtml = '';
    if (ch.grammar_tables && ch.grammar_tables.length > 0) {
      tablesHtml = ch.grammar_tables.map(t => `
        <div style="margin: 20px 0; background: var(--bg-surface); border: 1px solid var(--border-prominent); border-radius: var(--radius-md); overflow: hidden; box-shadow: var(--shadow-sm);">
          <div style="background: var(--bg-app-alt); padding: 12px 18px; font-weight: 700; font-family: var(--font-serif); font-size: 1.05rem; color: var(--terracotta);">
            ${t.title}
          </div>
          <div style="overflow-x: auto;">
            <table style="width: 100%; border-collapse: collapse; text-align: left; font-size: 0.9rem;">
              <thead>
                <tr style="border-bottom: 2px solid var(--border-subtle); background: var(--bg-surface);">
                  ${(t.headers || []).map(h => `<th style="padding: 10px 14px; font-weight: 700; color: var(--text-secondary);">${h}</th>`).join('')}
                </tr>
              </thead>
              <tbody>
                ${(t.rows || []).map(r => `
                  <tr style="border-bottom: 1px solid var(--border-subtle);">
                    ${r.map(cell => `<td style="padding: 10px 14px; color: var(--text-primary); font-family: var(--font-sans);">${cell}</td>`).join('')}
                  </tr>
                `).join('')}
              </tbody>
            </table>
          </div>
        </div>
      `).join('');
    }

    return `
      <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: 28px; box-shadow: var(--shadow-sm);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 10px;">
          <div>
            <h2 style="font-family: var(--font-serif); font-size: 1.5rem; color: var(--text-primary);">
              ${ch.grammar_title || 'Grammar Rules & Formations'}
            </h2>
            <p style="color: var(--text-secondary); font-size: 0.88rem;">
              English grammatical explanations tailored specifically for English native speakers learning Italian.
            </p>
          </div>
          <button 
            class="btn-tactile" 
            style="padding: 8px 16px; font-size: 0.85rem;"
            onclick="window.roadmapView.markPartDone('grammar')"
          >
            ${ch.grammar_done ? '✓ Grammar Completed' : '✅ Mark Grammar Complete (+15 XP)'}
          </button>
        </div>

        <div style="background: var(--bg-app-alt); border-left: 4px solid var(--amalfi-blue); border-radius: var(--radius-sm); padding: 18px 22px; margin-bottom: 24px; line-height: 1.6; color: var(--text-primary); font-size: 0.95rem;">
          ${ch.grammar_rules ? ch.grammar_rules.replace(/\\n/g, '<br>') : 'Read the conjugation and syntax rules below.'}
        </div>

        ${tablesHtml}

        <div style="text-align: center; border-top: 1px solid var(--border-subtle); padding-top: 24px; margin-top: 24px;">
          <button 
            class="btn-tactile" 
            style="padding: 12px 28px; font-size: 0.95rem;"
            onclick="window.roadmapView.markPartDone('grammar'); window.roadmapView.setStudioTab('reading');"
          >
            ${ch.grammar_done ? 'Next Section: Reading Dialogue →' : 'Save Grammar & Continue to Reading →'}
          </button>
        </div>
      </div>
    `;
  }

  // 3. Reading Tab
  // 3. Reading Tab
  renderReadingTab(ch) {
    let questionsHtml = '';
    const allQuestionsSolved = ch.reading_questions && ch.reading_questions.length > 0 &&
      ch.reading_questions.every((_, i) => this.readingEvaluations[i] && this.readingEvaluations[i].isCorrect);

    if (ch.reading_questions && ch.reading_questions.length > 0) {
      questionsHtml = `
        <div style="margin-top: 32px; border-top: 2px solid var(--border-subtle); padding-top: 24px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; flex-wrap: wrap; gap: 8px;">
            <h3 style="font-family: var(--font-serif); font-size: 1.25rem; color: var(--text-primary);">
              ❓ Reading Comprehension Check
            </h3>
            <span style="font-size: 0.8rem; font-weight: 700; color: var(--terracotta); background: var(--terracotta-subtle); padding: 4px 10px; border-radius: var(--radius-full);">
              * Choose the correct answer to unlock Writing Lab
            </span>
          </div>
          <div style="display: flex; flex-direction: column; gap: 18px;">
            ${ch.reading_questions.map((q, idx) => {
              const selected = this.readingQuizAnswers[idx];
              const evalInfo = this.readingEvaluations[idx];
              const isSolved = evalInfo && evalInfo.isCorrect;

              return `
                <div id="reading-q-card-${idx}" style="background: var(--bg-app-alt); border: 1.5px solid ${isSolved ? '#86efac' : 'var(--border-subtle)'}; border-radius: var(--radius-md); padding: 20px; transition: all 0.2s ease;">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <div style="font-weight: 700; font-size: 1.05rem; color: var(--text-primary); font-family: var(--font-serif);">
                      ${idx + 1}. ${q.question}
                    </div>
                    <span id="rq-status-${idx}" class="gram-badge" style="${isSolved ? 'background: #f0fdf4; color: #15803d; border-color: #86efac;' : ''}">
                      ${isSolved ? '✓ Mastered' : 'Question ' + (idx + 1)}
                    </span>
                  </div>

                  <div class="options-list" style="display: flex; flex-direction: column; gap: 8px;">
                    ${(q.options || []).map((opt, optIdx) => {
                      const isOptSelected = (selected === opt);
                      const isCorrectOpt = isSolved && isOptSelected;

                      let btnClass = 'option-btn';
                      let btnStyle = '';
                      if (isSolved) {
                        if (isCorrectOpt) {
                          btnClass += ' correct';
                          btnStyle = 'border-color: #22c55e !important; background: #f0fdf4 !important; color: #15803d !important; pointer-events: none;';
                        } else {
                          btnStyle = 'opacity: 0.5; pointer-events: none;';
                        }
                      }

                      return `
                        <button 
                          type="button" 
                          class="${btnClass}" 
                          id="rq-btn-${idx}-${optIdx}"
                          style="display: flex; justify-content: space-between; align-items: center; padding: 14px 18px; font-size: 0.95rem; ${btnStyle}"
                          onclick="window.roadmapView.handleReadingOptionClick(${idx}, '${opt.replace(/'/g, "\\'")}', this)"
                        >
                          <span>${opt}</span>
                          <span class="rq-indicator" style="font-weight: 800; font-size: 1.1rem;">${isCorrectOpt ? '✓' : ''}</span>
                        </button>
                      `;
                    }).join('')}
                  </div>

                  <div id="reading-feedback-${idx}" class="quiz-feedback ${isSolved ? 'correct' : ''}" style="${isSolved ? 'display: block;' : 'display: none;'} margin-top: 14px;">
                    ${isSolved ? `✓ <strong>Esatto! (Correct):</strong> ${q.explanation || 'Ben fatto!'}` : ''}
                  </div>
                </div>
              `;
            }).join('')}
          </div>
        </div>
      `;
    }

    return `
      <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: 28px; box-shadow: var(--shadow-sm);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 10px;">
          <div>
            <h2 style="font-family: var(--font-serif); font-size: 1.5rem; color: var(--text-primary);">
              ${ch.reading_title || 'Authentic Reading & Cultural Dialogue'}
            </h2>
            <p style="color: var(--text-secondary); font-size: 0.88rem;">
              Immerse yourself in authentic Italian contexts. Listen to the native audio, read the passage, and select the correct answer for each comprehension question.
            </p>
          </div>
          <div style="display: flex; gap: 8px;">
            <button 
              class="audio-btn" 
              style="width: 40px; height: 40px; font-size: 1.1rem;"
              onclick="window.soundEngine.speakItalian('${(ch.reading_it || '').replace(/'/g, "\\'").replace(/\n/g, ' ')}')"
              title="Listen to full Italian dialogue"
            >
              🔊
            </button>
          </div>
        </div>

        <!-- Italian Passage -->
        <div style="background: var(--bg-app-alt); border-radius: var(--radius-md); padding: 24px; font-family: var(--font-serif); font-size: 1.15rem; line-height: 1.8; color: var(--text-primary); margin-bottom: 18px; border: 1px solid var(--border-subtle);">
          ${(ch.reading_it || '').replace(/\n/g, '<br><br>')}
        </div>

        <!-- Translation Toggle -->
        <div style="margin-bottom: 20px;">
          <button 
            class="btn-secondary" 
            style="padding: 6px 14px; font-size: 0.82rem;"
            onclick="window.roadmapView.readingTranslationVisible = !window.roadmapView.readingTranslationVisible; window.roadmapView.renderChapterStudio();"
          >
            ${this.readingTranslationVisible ? '🙈 Hide English Translation' : '👁️ Show English Translation'}
          </button>

          ${this.readingTranslationVisible ? `
            <div style="margin-top: 12px; background: var(--bg-surface); border: 1px dashed var(--border-prominent); border-radius: var(--radius-md); padding: 18px; font-size: 0.95rem; color: var(--text-secondary); line-height: 1.6;">
              ${(ch.reading_en || '').replace(/\n/g, '<br><br>')}
            </div>
          ` : ''}
        </div>

        ${questionsHtml}

        <!-- Success completion banner when all questions solved -->
        <div id="reading-all-done-banner" style="${(ch.reading_done || allQuestionsSolved) ? 'display: block;' : 'display: none;'} background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border: 2px solid #86efac; border-radius: var(--radius-md); padding: 22px; text-align: center; margin-top: 26px;">
          <div style="font-size: 2.2rem; margin-bottom: 4px;">🎉</div>
          <div style="font-family: var(--font-serif); font-size: 1.3rem; font-weight: 800; color: #166534; margin-bottom: 4px;">
            Perfetto! All Reading Questions Mastered (+20 XP)
          </div>
          <p style="color: #15803d; font-size: 0.92rem; margin-bottom: 16px;">
            You mastered the comprehension check! Advancing to the Writing Lab...
          </p>
          <button class="btn-tactile" style="background: var(--olive); font-size: 0.95rem; padding: 12px 28px;" onclick="window.roadmapView.setStudioTab('writing');">
            ✍️ Continue to Writing Lab →
          </button>
        </div>
      </div>
    `;
  }

  async handleReadingOptionClick(qIdx, selectedOpt, btnEl) {
    const ch = this.activeChapter;
    if (!ch) return;

    const questions = ch.reading_questions || [];
    const q = questions[qIdx];
    if (!q) return;

    const userClean = selectedOpt.trim().toLowerCase();
    const corrClean = (q.correct_answer || '').trim().toLowerCase();
    const isCorrect = (userClean === corrClean);

    const qCard = document.getElementById(`reading-q-card-${qIdx}`);
    const feedbackBox = document.getElementById(`reading-feedback-${qIdx}`);
    const statusBadge = document.getElementById(`rq-status-${qIdx}`);

    if (!isCorrect) {
      // FALSE ANSWER: Turn option RED, shake, play wrong sound, wait for user to pick correct option
      if (window.soundEngine && typeof window.soundEngine.playWrong === 'function') {
        window.soundEngine.playWrong();
      }

      btnEl.classList.remove('correct');
      btnEl.classList.add('wrong');
      btnEl.style.borderColor = '#ef4444';
      btnEl.style.backgroundColor = '#fef2f2';
      btnEl.style.color = '#b91c1c';

      btnEl.style.animation = 'none';
      void btnEl.offsetWidth; // trigger reflow
      btnEl.style.animation = 'shakeWrong 0.4s ease';

      const indicator = btnEl.querySelector('.rq-indicator');
      if (indicator) indicator.textContent = '❌';

      if (feedbackBox) {
        feedbackBox.className = 'quiz-feedback wrong';
        feedbackBox.style.display = 'block';
        feedbackBox.innerHTML = `❌ <strong>Risposta non corretta:</strong> Rivedi il testo sopra e seleziona l'opzione giusta!`;
      }

      this.readingEvaluations[qIdx] = { isCorrect: false, chosen: selectedOpt };
      return;
    }

    // CORRECT ANSWER: Turn option GREEN, pulse, play success chime, lock in answer
    if (window.soundEngine && typeof window.soundEngine.playSuccess === 'function') {
      window.soundEngine.playSuccess();
    }

    // Lock option buttons in this question card
    if (qCard) {
      qCard.querySelectorAll('.option-btn').forEach(b => {
        if (b !== btnEl) {
          b.style.pointerEvents = 'none';
          b.style.opacity = '0.5';
          b.classList.remove('wrong');
        }
      });
    }

    btnEl.classList.remove('wrong');
    btnEl.classList.add('correct');
    btnEl.style.borderColor = '#22c55e';
    btnEl.style.backgroundColor = '#f0fdf4';
    btnEl.style.color = '#15803d';
    btnEl.style.pointerEvents = 'none';

    btnEl.style.animation = 'none';
    void btnEl.offsetWidth; // trigger reflow
    btnEl.style.animation = 'successPulse 0.35s ease';

    const indicator = btnEl.querySelector('.rq-indicator');
    if (indicator) indicator.textContent = '✓';

    if (statusBadge) {
      statusBadge.style.background = '#f0fdf4';
      statusBadge.style.color = '#15803d';
      statusBadge.style.borderColor = '#86efac';
      statusBadge.textContent = '✓ Mastered';
    }

    if (feedbackBox) {
      feedbackBox.className = 'quiz-feedback correct';
      feedbackBox.style.display = 'block';
      feedbackBox.innerHTML = `✓ <strong>Esatto! (Correct):</strong> ${q.explanation || 'Ben fatto!'}`;
    }

    this.readingQuizAnswers[qIdx] = selectedOpt;
    this.readingEvaluations[qIdx] = { isCorrect: true, chosen: selectedOpt, explanation: q.explanation || '' };

    // Check if ALL questions are answered correctly
    const allQuestionsSolved = questions.length > 0 && questions.every((_, i) => this.readingEvaluations[i] && this.readingEvaluations[i].isCorrect);

    if (allQuestionsSolved) {
      try {
        await this.markPartDone('reading', { answers: this.readingQuizAnswers });
        if (window.app && typeof window.app.triggerConfetti === 'function') {
          window.app.triggerConfetti();
        }
      } catch (e) {
        console.error('Error auto-saving reading part:', e);
      }

      const allDoneBanner = document.getElementById('reading-all-done-banner');
      if (allDoneBanner) {
        allDoneBanner.style.display = 'block';
        allDoneBanner.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }

      // Automatically advance to the Writing Lab after a brief celebration (1.2s)!
      setTimeout(() => {
        this.setStudioTab('writing');
        window.scrollTo({ top: 0, behavior: 'smooth' });
      }, 1200);
    }
  }

  // 4. Writing Tab
  renderWritingTab(ch) {
    const starterChips = ch.writing_starter_words || [];
    const currentDraft = this.writingDraft || '';

    return `
      <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: 28px; box-shadow: var(--shadow-sm);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 10px;">
          <div>
            <h2 style="font-family: var(--font-serif); font-size: 1.5rem; color: var(--text-primary);">
              Writing Lab & Sentence Construction
            </h2>
            <p style="color: var(--text-secondary); font-size: 0.88rem;">
              Draft your Italian response using the prompt and starter tiles below. Responses must be written in Italian.
            </p>
          </div>
          <button 
            class="btn-tactile" 
            style="padding: 8px 16px; font-size: 0.85rem;"
            onclick="window.roadmapView.checkAndCompleteWriting()"
          >
            ${ch.writing_done ? '✓ Writing Submitted (+25 XP)' : '✍️ Check & Submit Writing (+25 XP)'}
          </button>
        </div>

        <!-- Prompt Banner -->
        <div style="background: var(--bg-app-alt); border-left: 4px solid var(--terracotta); border-radius: var(--radius-sm); padding: 16px 20px; margin-bottom: 20px;">
          <div style="font-weight: 800; font-size: 0.8rem; text-transform: uppercase; color: var(--terracotta); letter-spacing: 0.05em; margin-bottom: 4px;">
            Writing Prompt
          </div>
          <div style="font-size: 1.05rem; color: var(--text-primary); font-family: var(--font-serif); line-height: 1.5;">
            ${ch.writing_prompt || 'Describe yourself or complete the chapter scenario in Italian.'}
          </div>
        </div>

        <!-- Starter Chips -->
        ${starterChips.length > 0 ? `
          <div style="margin-bottom: 16px;">
            <div style="font-size: 0.8rem; font-weight: 700; color: var(--text-muted); text-transform: uppercase; margin-bottom: 8px;">
              Starter Words (Click to insert into your response):
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
              ${starterChips.map(chip => `
                <button 
                  type="button" 
                  class="btn-secondary starter-chip-btn" 
                  style="padding: 4px 10px; font-size: 0.82rem; border-radius: var(--radius-full);"
                  onclick="const area = document.getElementById('chapter-writing-area'); area.value = (area.value ? area.value + ' ' : '') + '${chip.replace(/'/g, "\\'")}'; area.focus(); window.roadmapView.writingDraft = area.value;"
                >
                  ➕ ${chip}
                </button>
              `).join('')}
            </div>
          </div>
        ` : ''}

        <!-- Text Area -->
        <div style="margin-bottom: 20px;">
          <textarea 
            id="chapter-writing-area" 
            class="form-control" 
            rows="5" 
            placeholder="Scrivi qui la tua risposta in italiano... (Minimum 3 Italian words / 10 characters required)" 
            style="width: 100%; font-family: var(--font-sans); font-size: 1rem; line-height: 1.6; padding: 14px; border: 2px solid var(--border-prominent); border-radius: var(--radius-md);"
            oninput="window.roadmapView.writingDraft = this.value; this.style.borderColor = 'var(--border-prominent)';"
          >${currentDraft}</textarea>
        </div>

        <!-- Model Solution Accordion -->
        <div style="margin-bottom: 24px;">
          <button 
            type="button"
            class="btn-secondary" 
            style="padding: 6px 14px; font-size: 0.82rem;"
            onclick="window.roadmapView.writingModelVisible = !window.roadmapView.writingModelVisible; window.roadmapView.renderChapterStudio();"
          >
            ${this.writingModelVisible ? '🙈 Hide Model Answer' : '💡 Compare with Model Italian Solution'}
          </button>

          ${this.writingModelVisible && ch.writing_sample_solution ? `
            <div style="margin-top: 12px; background: var(--olive-subtle); border: 1px solid rgba(45, 106, 79, 0.3); border-radius: var(--radius-md); padding: 16px; font-size: 0.95rem; color: var(--olive); line-height: 1.6;">
              <strong>Model Italian Solution:</strong><br>
              <em>"${ch.writing_sample_solution}"</em>
            </div>
          ` : ''}
        </div>

        <div style="text-align: center; border-top: 1px solid var(--border-subtle); padding-top: 24px; display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
          <button 
            class="btn-tactile" 
            style="padding: 12px 28px; font-size: 0.95rem;"
            onclick="window.roadmapView.checkAndCompleteWriting()"
          >
            ${ch.writing_done ? '✓ Re-submit Writing' : '✍️ Check & Submit Writing (+25 XP)'}
          </button>
          ${ch.writing_done ? `
            <button 
              class="btn-secondary" 
              style="padding: 12px 24px; font-size: 0.95rem;"
              onclick="window.roadmapView.setStudioTab('quiz')"
            >
              Next Section: Consolidation Quiz →
            </button>
          ` : ''}
        </div>
      </div>
    `;
  }

  async checkAndCompleteWriting() {
    const ch = this.activeChapter;
    if (!ch) return;

    const area = document.getElementById('chapter-writing-area');
    const text = (area ? area.value : this.writingDraft || '').trim();
    const words = text ? text.split(/\s+/).filter(Boolean) : [];

    if (text.length < 10 || words.length < 3) {
      if (window.soundEngine) window.soundEngine.playError();
      if (area) {
        area.style.borderColor = '#ef4444';
        area.style.boxShadow = '0 0 0 4px rgba(239, 68, 68, 0.2)';
        area.focus();
      }
      alert('⚠️ Response Required: Please compose your Italian response before submitting (minimum 3 Italian words / 10 characters). Click on the starter tiles above to help compose your sentence!');
      return;
    }

    this.writingDraft = text;
    try {
      await this.markPartDone('writing', { writing_text: text });
      if (window.soundEngine) window.soundEngine.playSuccess();
      this.writingModelVisible = true;
      this.renderChapterStudio();
      alert('🎉 Ottimo lavoro! Your Italian writing response has been saved (+25 XP). Check the model solution below to see native phrasing!');
    } catch (e) {
      alert(`Error submitting writing: ${e.message}`);
    }
  }

  // 5. Quiz Tab
  renderQuizTab(ch) {
    if (!ch.exercises || ch.exercises.length === 0) {
      return `
        <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: 40px; text-align: center;">
          <div style="font-size: 3rem; margin-bottom: 12px;">🎉</div>
          <h2 style="font-family: var(--font-serif); font-size: 1.6rem; color: var(--text-primary); margin-bottom: 8px;">
            Chapter Practice Complete!
          </h2>
          <p style="color: var(--text-secondary); max-width: 500px; margin: 0 auto 20px;">
            You have reviewed all learning materials for this chapter. Head back to the overview to continue to the next chapter.
          </p>
          <button class="btn-tactile" onclick="window.roadmapView.closeChapter()">
            🗺️ Return to Chapters Overview
          </button>
        </div>
      `;
    }

    return `
      <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-lg); padding: 28px; box-shadow: var(--shadow-sm);">
        <div style="margin-bottom: 24px;">
          <h2 style="font-family: var(--font-serif); font-size: 1.5rem; color: var(--text-primary); margin-bottom: 4px;">
            Consolidation Exercises (${ch.exercises.length})
          </h2>
          <p style="color: var(--text-secondary); font-size: 0.88rem;">
            Test your understanding of the words and grammar introduced in Chapter ${ch.chapter_number}. Click an option to check your answer instantly.
          </p>
        </div>

        <div style="display: flex; flex-direction: column; gap: 20px; margin-bottom: 28px;">
          ${ch.exercises.map((ex, idx) => {
            const selected = this.chapterExerciseAnswers[ex.id];
            const evalInfo = this.chapterExerciseEvaluations[ex.id];
            const isSolved = evalInfo && evalInfo.isCorrect;

            return `
              <div id="chapter-ex-card-${ex.id}" style="background: var(--bg-app-alt); border: 1.5px solid ${isSolved ? '#86efac' : 'var(--border-subtle)'}; border-radius: var(--radius-md); padding: 18px; transition: all 0.2s ease;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                  <span class="gram-badge" style="font-size: 0.72rem;">Question ${idx + 1}</span>
                  <span id="ex-status-${ex.id}" style="font-size: 0.82rem; font-weight: 800; color: ${isSolved ? '#15803d' : 'var(--text-muted)'};">
                    ${isSolved ? '✓ Corretto!' : ''}
                  </span>
                </div>
                <div style="font-size: 1.05rem; font-weight: 600; color: var(--text-primary); margin-bottom: 12px; font-family: var(--font-serif);">
                  ${ex.prompt}
                </div>
                <div class="options-list" style="display: flex; flex-direction: column; gap: 8px;">
                  ${(ex.options || []).map((opt, optIdx) => {
                    const isCorrectOpt = isSolved && (selected === opt);
                    let btnClass = 'option-btn';
                    let btnStyle = '';
                    if (isSolved) {
                      if (isCorrectOpt) {
                        btnClass += ' correct';
                        btnStyle = 'border-color: #22c55e !important; background: #f0fdf4 !important; color: #15803d !important; pointer-events: none;';
                      } else {
                        btnStyle = 'opacity: 0.5; pointer-events: none;';
                      }
                    }

                    return `
                      <button 
                        type="button" 
                        class="${btnClass}" 
                        id="ex-btn-${ex.id}-${optIdx}"
                        style="display: flex; justify-content: space-between; align-items: center; padding: 12px 16px; font-size: 0.95rem; ${btnStyle}"
                        onclick="window.roadmapView.handleQuizOptionClick(${ex.id}, '${opt.replace(/'/g, "\\'")}', this)"
                      >
                        <span>${opt}</span>
                        <span class="ex-indicator" style="font-weight: 800; font-size: 1.05rem;">${isCorrectOpt ? '✓' : ''}</span>
                      </button>
                    `;
                  }).join('')}
                </div>
                <div id="ex-feedback-${ex.id}" class="quiz-feedback ${isSolved ? 'correct' : ''}" style="${isSolved ? 'display: block;' : 'display: none;'} margin-top: 12px;">
                  ${isSolved ? `✓ <strong>Esatto!</strong> ${ex.explanation || ''}` : ''}
                </div>
              </div>
            `;
          }).join('')}
        </div>

        <div style="text-align: center; border-top: 1px solid var(--border-subtle); padding-top: 24px;">
          <button 
            class="btn-tactile" 
            style="padding: 14px 32px; font-size: 1rem;"
            onclick="window.roadmapView.checkAndCompleteQuiz()"
          >
            🎉 Finish Chapter & Return to Curriculum
          </button>
        </div>
      </div>
    `;
  }

  async handleQuizOptionClick(exId, selectedOpt, btnEl) {
    const ch = this.activeChapter;
    if (!ch) return;

    try {
      const evaluation = await window.api.checkAnswer(exId, selectedOpt);
      const card = document.getElementById(`chapter-ex-card-${exId}`);
      const feedbackBox = document.getElementById(`ex-feedback-${exId}`);
      const statusBadge = document.getElementById(`ex-status-${exId}`);

      if (!evaluation.correct) {
        // Wrong answer: turn red, shake, play wrong tone, wait for user to pick another
        if (window.soundEngine && typeof window.soundEngine.playWrong === 'function') {
          window.soundEngine.playWrong();
        }

        btnEl.classList.remove('correct');
        btnEl.classList.add('wrong');
        btnEl.style.borderColor = '#ef4444';
        btnEl.style.backgroundColor = '#fef2f2';
        btnEl.style.color = '#b91c1c';

        btnEl.style.animation = 'none';
        void btnEl.offsetWidth;
        btnEl.style.animation = 'shakeWrong 0.4s ease';

        const indicator = btnEl.querySelector('.ex-indicator');
        if (indicator) indicator.textContent = '❌';

        if (feedbackBox) {
          feedbackBox.className = 'quiz-feedback wrong';
          feedbackBox.style.display = 'block';
          feedbackBox.innerHTML = `❌ <strong>Non corretto:</strong> Riprova! (Try again)`;
        }
        return;
      }

      // Correct answer: turn green, pulse, play success tone, lock in
      if (window.soundEngine && typeof window.soundEngine.playSuccess === 'function') {
        window.soundEngine.playSuccess();
      }

      if (card) {
        card.querySelectorAll('.option-btn').forEach(b => {
          if (b !== btnEl) {
            b.style.pointerEvents = 'none';
            b.style.opacity = '0.5';
            b.classList.remove('wrong');
          }
        });
      }

      btnEl.classList.remove('wrong');
      btnEl.classList.add('correct');
      btnEl.style.borderColor = '#22c55e';
      btnEl.style.backgroundColor = '#f0fdf4';
      btnEl.style.color = '#15803d';
      btnEl.style.pointerEvents = 'none';

      btnEl.style.animation = 'none';
      void btnEl.offsetWidth;
      btnEl.style.animation = 'successPulse 0.35s ease';

      const indicator = btnEl.querySelector('.ex-indicator');
      if (indicator) indicator.textContent = '✓';

      if (statusBadge) {
        statusBadge.textContent = '✓ Corretto!';
        statusBadge.style.color = '#15803d';
      }

      if (feedbackBox) {
        feedbackBox.className = 'quiz-feedback correct';
        feedbackBox.style.display = 'block';
        feedbackBox.innerHTML = `✓ <strong>Esatto! (Correct):</strong> ${evaluation.explanation || ''}`;
      }

      this.chapterExerciseAnswers[exId] = selectedOpt;
      this.chapterExerciseEvaluations[exId] = { isCorrect: true, chosen: selectedOpt, explanation: evaluation.explanation || '' };
    } catch (e) {
      console.error('Error checking exercise answer:', e);
    }
  }

  async checkAndCompleteQuiz() {
    const ch = this.activeChapter;
    if (!ch) return;

    const exercises = ch.exercises || [];
    if (exercises.length === 0) {
      this.closeChapter();
      return;
    }

    const unanswered = [];
    exercises.forEach((ex, idx) => {
      if (!this.chapterExerciseAnswers[ex.id]) {
        unanswered.push(idx + 1);
      }
    });

    if (unanswered.length > 0) {
      if (window.soundEngine) window.soundEngine.playError();
      const firstUnansweredCard = document.getElementById(`chapter-ex-card-${exercises[unanswered[0] - 1].id}`);
      if (firstUnansweredCard) {
        firstUnansweredCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
      alert(`⚠️ Please answer Question ${unanswered.join(', ')} before finishing the chapter.`);
      return;
    }

    if (window.soundEngine) window.soundEngine.playSuccess();
    if (window.app) window.app.triggerConfetti();
    alert('🎉 Complimenti! You completed all chapter exercises and successfully mastered this chapter!');
    this.closeChapter();
  }
}

window.RoadmapView = RoadmapView;
