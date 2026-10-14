/**
 * DAILY-ITALY — Home / Landing Page View
 * English Interface with Italian Target Language immersion
 */

class HomeView {
  constructor(container) {
    this.container = container;
  }

  render() {
    const user = window.api.user;

    this.container.innerHTML = `
      <div class="hero-section">
        
        <div class="hero-pill">
          🇮🇹 Complete Italian Language Learning Platform (CEFR A1–B2)
        </div>

        <h1 class="hero-title">
          Master Real Italian,<br>
          <span>One Step at a Time.</span>
        </h1>

        <p class="hero-subtitle">
          Daily-Italy combines 60 structured CEFR chapters across A1, A2, B1, and B2: high-frequency vocabulary flashcards, grammar rules with conjugation tables, cultural reading dialogues with native audio, guided writing, and Spaced Repetition (SRS).
        </p>

        ${user ? `
          <div style="background: var(--bg-surface); border: 2px solid var(--border-subtle); border-radius: var(--radius-lg); padding: 24px; max-width: 540px; margin: 0 auto 36px; box-shadow: var(--shadow-sm); text-align: left;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
              <span style="font-weight: 800; font-family: var(--font-serif); font-size: 1.2rem; color: var(--text-primary);">
                Welcome back, ${user.username}!
              </span>
              <span class="gram-badge" style="background: var(--olive-subtle); color: var(--olive);">Active Learner</span>
            </div>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 16px;">
              Ready to continue your Italian journey today? Keep your daily streak alive!
            </p>
            <div style="display: flex; gap: 10px; flex-wrap: wrap;">
              <button class="btn-tactile" onclick="window.app.switchView('roadmap')">
                🗺️ Explore Chapters & Levels
              </button>
              <button class="btn-secondary" onclick="window.app.switchView('review')">
                🧠 Smart Review
              </button>
            </div>
          </div>
        ` : `
          <div class="hero-actions">
            <button class="btn-tactile" style="font-size: 1.05rem; padding: 14px 28px;" onclick="window.app.openAuthModal(true)">
              ✨ Sign Up to Start Learning
            </button>
            <button class="btn-secondary" style="font-size: 1.05rem; padding: 14px 24px;" onclick="window.app.openAuthModal(false)">
              🔑 Log In to Your Account
            </button>
          </div>
        `}

        <!-- Word of the Day Spotlight -->
        <div style="max-width: 560px; margin: 0 auto 48px; background: var(--bg-surface); border: 2px solid var(--border-prominent); border-radius: var(--radius-lg); padding: 26px; box-shadow: var(--shadow-md); text-align: left;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <span style="font-size: 0.75rem; font-weight: 800; text-transform: uppercase; color: var(--terracotta); letter-spacing: 0.08em;">
              ✨ Word of the Day
            </span>
            <button class="audio-btn" style="width: 36px; height: 36px; font-size: 1rem;" onclick="window.soundEngine.speakItalian('Buongiorno')" title="Listen to native Italian pronunciation">
              🔊
            </button>
          </div>
          <div style="display: flex; align-items: baseline; gap: 12px; margin-bottom: 6px;">
            <span style="font-family: var(--font-serif); font-size: 2.2rem; font-weight: 700; color: var(--text-primary);">
              Buongiorno
            </span>
            <span class="gram-badge">Greeting / Formula of Politeness</span>
          </div>
          <p style="color: var(--text-secondary); font-size: 0.95rem; margin-bottom: 12px;">
            Good morning / Good day — Used from morning until mid-afternoon in all formal and informal contexts.
          </p>
          <div style="background: var(--bg-app-alt); padding: 12px 16px; border-radius: var(--radius-sm); font-size: 0.9rem; color: var(--text-secondary); font-style: italic;">
            "Buongiorno a tutti, oggi è una splendida giornata per imparare!"
          </div>
        </div>

        <!-- 4 Core Learning Pillars -->
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 18px; max-width: 1100px; margin: 0 auto 40px; text-align: left;">
          
          <div class="stat-card" style="cursor: pointer; transition: transform 0.2s ease;" onclick="window.app.switchView('roadmap')">
            <div style="font-size: 2rem; margin-bottom: 10px;">🗺️</div>
            <div style="font-family: var(--font-serif); font-weight: 700; font-size: 1.15rem; color: var(--text-primary); margin-bottom: 6px;">
              Chapters & Levels (A1–B2)
            </div>
            <p style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5;">
              60 CEFR-structured chapters across 4 levels, with sequential unlocking and fast-track placement tests.
            </p>
          </div>

          <div class="stat-card" style="cursor: pointer; transition: transform 0.2s ease;" onclick="window.app.switchView('grammar')">
            <div style="font-size: 2rem; margin-bottom: 10px;">📖</div>
            <div style="font-family: var(--font-serif); font-weight: 700; font-size: 1.15rem; color: var(--text-primary); margin-bottom: 6px;">
              Grammar in Context
            </div>
            <p style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5;">
              Clear English explanations of Italian grammar, interactive conjugation tables, and syntax guidelines.
            </p>
          </div>

          <div class="stat-card" style="cursor: pointer; transition: transform 0.2s ease;" onclick="window.app.switchView('reading')">
            <div style="font-size: 2rem; margin-bottom: 10px;">📚</div>
            <div style="font-family: var(--font-serif); font-weight: 700; font-size: 1.15rem; color: var(--text-primary); margin-bottom: 6px;">
              Readings & Culture
            </div>
            <p style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5;">
              Authentic Italian dialogues and cultural stories with native voice audio and comprehension checks.
            </p>
          </div>

          <div class="stat-card" style="cursor: pointer; transition: transform 0.2s ease;" onclick="window.app.switchView('writing')">
            <div style="font-size: 2rem; margin-bottom: 10px;">✍️</div>
            <div style="font-family: var(--font-serif); font-weight: 700; font-size: 1.15rem; color: var(--text-primary); margin-bottom: 6px;">
              Writing & Composition
            </div>
            <p style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5;">
              Sentence construction with interactive starter tiles and immediate comparison with native model answers.
            </p>
          </div>

        </div>

      </div>
    `;
  }
}

window.HomeView = HomeView;
