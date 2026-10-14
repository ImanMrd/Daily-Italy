/**
 * DAILY-ITALY — Main Application Controller & Router
 */

class Application {
  constructor() {
    this.currentView = 'home';
    this.views = {};
  }

  async init() {
    // Setup views
    this.views['home'] = new window.HomeView(document.getElementById('view-home'));
    this.views['roadmap'] = new window.RoadmapView(document.getElementById('view-roadmap'));
    this.views['flashcards'] = new window.FlashcardView(document.getElementById('view-flashcards'));
    this.views['quiz'] = new window.QuizView(document.getElementById('view-quiz'));
    this.views['grammar'] = new window.GrammarView(document.getElementById('view-grammar'));
    this.views['reading'] = new window.ReadingView(document.getElementById('view-reading'));
    this.views['writing'] = new window.WritingView(document.getElementById('view-writing'));
    this.views['review'] = new window.ReviewView(document.getElementById('view-review'));
    this.views['leaderboard'] = new window.LeaderboardView(document.getElementById('view-leaderboard'));
    this.views['admin'] = new window.AdminView(document.getElementById('view-admin'));

    window.homeView = this.views['home'];
    window.roadmapView = this.views['roadmap'];
    window.flashcardView = this.views['flashcards'];
    window.quizView = this.views['quiz'];
    window.grammarView = this.views['grammar'];
    window.readingView = this.views['reading'];
    window.writingView = this.views['writing'];
    window.reviewView = this.views['review'];
    window.leaderboardView = this.views['leaderboard'];
    window.adminView = this.views['admin'];

    // Verify session
    await window.api.fetchCurrentUser();
    this.updateUserStatsBar();

    // Listen to hash changes for deep linking
    window.addEventListener('hashchange', () => this.handleHashRoute());

    // Setup navigation click handlers
    document.querySelectorAll('.nav-btn[data-view]').forEach(btn => {
      btn.addEventListener('click', () => {
        window.location.hash = btn.dataset.view;
      });
    });

    // Setup horizontal mouse-wheel scrolling and scroll button listeners on nav tabs container
    const navTabs = document.getElementById('main-nav-tabs');
    if (navTabs) {
      navTabs.addEventListener('scroll', () => this.updateNavScrollButtons(), { passive: true });
      navTabs.addEventListener('wheel', (e) => {
        if (e.deltaY !== 0) {
          e.preventDefault();
          navTabs.scrollLeft += e.deltaY;
          this.updateNavScrollButtons();
        }
      }, { passive: false });

      setTimeout(() => this.updateNavScrollButtons(), 250);
      window.addEventListener('resize', () => this.updateNavScrollButtons());
    }

    // Initial route handling
    if (!window.location.hash) {
      window.location.hash = '#home';
    } else {
      this.handleHashRoute();
    }
  }

  scrollNav(offset) {
    const nav = document.getElementById('main-nav-tabs');
    if (!nav) return;
    nav.scrollBy({ left: offset, behavior: 'smooth' });
    if (window.soundEngine && typeof window.soundEngine.playTap === 'function') {
      window.soundEngine.playTap();
    }
    setTimeout(() => this.updateNavScrollButtons(), 300);
  }

  updateNavScrollButtons() {
    const nav = document.getElementById('main-nav-tabs');
    const leftBtn = document.getElementById('nav-scroll-left-btn');
    const rightBtn = document.getElementById('nav-scroll-right-btn');
    if (!nav || !leftBtn || !rightBtn) return;

    const canScrollLeft = nav.scrollLeft > 6;
    const canScrollRight = (nav.scrollLeft + nav.clientWidth) < (nav.scrollWidth - 6);

    leftBtn.classList.toggle('disabled', !canScrollLeft);
    leftBtn.disabled = !canScrollLeft;

    rightBtn.classList.toggle('disabled', !canScrollRight);
    rightBtn.disabled = !canScrollRight;
  }

  handleHashRoute() {
    const hash = window.location.hash.replace('#', '') || 'home';
    const [viewName, param] = hash.split('/');

    if (viewName === 'study' && param) {
      this.startFlashcards(parseInt(param, 10), false);
    } else if (viewName === 'quiz' && param) {
      this.startQuiz(parseInt(param, 10), false);
    } else if (this.views[viewName]) {
      this.switchView(viewName, false);
    } else {
      this.switchView('home', false);
    }
  }

  switchView(viewName, updateHash = true) {
    this.currentView = viewName;

    if (updateHash) {
      window.location.hash = viewName;
    }

    // Update active nav buttons & scroll into view smoothly
    document.querySelectorAll('.nav-btn[data-view]').forEach(btn => {
      const isActive = btn.dataset.view === viewName;
      btn.classList.toggle('active', isActive);
      if (isActive && typeof btn.scrollIntoView === 'function') {
        btn.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
      }
    });

    // Update scroll arrow indicators
    setTimeout(() => this.updateNavScrollButtons(), 350);

    // Toggle views visibility with smooth transition animation re-trigger
    document.querySelectorAll('.view-section').forEach(sec => {
      sec.classList.remove('active');
    });

    const activeEl = document.getElementById(`view-${viewName}`);
    if (activeEl) {
      // Force reflow to re-trigger the CSS entrance animation smoothly
      void activeEl.offsetWidth;
      activeEl.classList.add('active');
    }

    // Play subtle UI tap feedback
    if (window.soundEngine && typeof window.soundEngine.playTap === 'function') {
      window.soundEngine.playTap();
    }

    // Trigger render
    if (this.views[viewName] && typeof this.views[viewName].render === 'function') {
      this.views[viewName].render();
    }

    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  startFlashcards(lessonId, updateHash = true) {
    if (updateHash) window.location.hash = `study/${lessonId}`;
    this.switchView('flashcards', false);
    this.views['flashcards'].loadLesson(lessonId);
  }

  startQuiz(lessonId, updateHash = true) {
    if (updateHash) window.location.hash = `quiz/${lessonId}`;
    this.switchView('quiz', false);
    this.views['quiz'].loadLessonExercises(lessonId);
  }

  updateUserStatsBar() {
    const user = window.api.user;
    const streakEl = document.getElementById('user-streak-val');
    const xpEl = document.getElementById('user-xp-val');
    const heartsEl = document.getElementById('user-hearts-val');
    const profileBtn = document.getElementById('profile-btn-text');
    const adminNavBtn = document.getElementById('admin-nav-tab');

    if (user) {
      if (streakEl) streakEl.textContent = user.streak_days || 1;
      if (xpEl) xpEl.textContent = user.xp || 0;
      if (heartsEl) heartsEl.textContent = user.hearts !== undefined ? user.hearts : 5;
      if (profileBtn) profileBtn.textContent = `${user.username} (Logout)`;
      if (adminNavBtn) {
        adminNavBtn.style.display = (user.role === 'admin') ? 'inline-flex' : 'none';
      }
    } else {
      if (streakEl) streakEl.textContent = '1';
      if (xpEl) xpEl.textContent = '0';
      if (heartsEl) heartsEl.textContent = '5';
      if (profileBtn) profileBtn.textContent = 'Log In';
      if (adminNavBtn) adminNavBtn.style.display = 'none';
    }
  }

  // Modals management
  handleProfileClick() {
    if (window.api.user) {
      if (confirm(`You are logged in as ${window.api.user.username}. Do you want to log out?`)) {
        window.api.clearSession();
        this.updateUserStatsBar();
        this.switchView('home');
      }
    } else {
      this.openAuthModal(false);
    }
  }

  openAuthModal(isRegister = false) {
    const modal = document.getElementById('auth-modal');
    const title = document.getElementById('auth-modal-title');
    const submitBtn = document.getElementById('auth-submit-btn');
    const togglePrompt = document.getElementById('auth-toggle-prompt');

    if (isRegister) {
      title.textContent = 'Create your Account';
      submitBtn.textContent = 'Sign Up';
      togglePrompt.innerHTML = `Already have an account? <a href="#" onclick="window.app.openAuthModal(false)">Log in here</a>`;
      modal.dataset.mode = 'register';
    } else {
      title.textContent = 'Welcome back to Daily-Italy!';
      submitBtn.textContent = 'Log In';
      togglePrompt.innerHTML = `Don't have an account? <a href="#" onclick="window.app.openAuthModal(true)">Sign up now</a>`;
      modal.dataset.mode = 'login';
    }

    modal.classList.add('open');
  }

  closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove('open');
  }

  async handleAuthSubmit(event) {
    event.preventDefault();
    const modal = document.getElementById('auth-modal');
    const mode = modal.dataset.mode || 'login';
    const username = document.getElementById('auth-username').value.trim();
    const password = document.getElementById('auth-password').value.trim();
    const errBox = document.getElementById('auth-error-msg');
    errBox.style.display = 'none';

    try {
      if (mode === 'register') {
        await window.api.register(username, password);
      } else {
        await window.api.login(username, password);
      }
      this.closeModal('auth-modal');
      this.updateUserStatsBar();
      if (this.views[this.currentView] && typeof this.views[this.currentView].render === 'function') {
        this.views[this.currentView].render();
      }
      window.soundEngine.playSuccess();
    } catch (e) {
      errBox.textContent = e.message;
      errBox.style.display = 'block';
      window.soundEngine.playWrong();
    }
  }

  openAddWordModal() {
    if (!window.api.user) {
      this.openAuthModal(false);
      return;
    }
    const modal = document.getElementById('add-word-modal');
    modal.classList.add('open');
  }

  async handleAddWordSubmit(event) {
    event.preventDefault();
    const errBox = document.getElementById('word-error-msg');
    errBox.style.display = 'none';

    const wordData = {
      lesson_id: 1,
      italian: document.getElementById('word-italian').value.trim(),
      word_type: document.getElementById('word-type').value,
      english: document.getElementById('word-english').value.trim(),
      pronunciation: document.getElementById('word-pronunciation').value.trim(),
      example_it: document.getElementById('word-example-it').value.trim(),
      example_en: document.getElementById('word-example-en').value.trim(),
      related_words: document.getElementById('word-related').value.trim()
    };

    try {
      await window.api.addCustomWord(wordData);
      this.closeModal('add-word-modal');
      window.soundEngine.playSuccess();
      alert('Word successfully saved to your vocabulary vault!');
      if (this.currentView === 'review' || this.currentView === 'roadmap' || this.currentView === 'admin') {
        this.views[this.currentView].render();
      }
    } catch (e) {
      errBox.textContent = e.message;
      errBox.style.display = 'block';
    }
  }

  // Level Placement Test Modal
  async openPlacementModal(level) {
    if (!window.api.user) {
      this.openAuthModal(false);
      return;
    }
    const modal = document.getElementById('placement-modal');
    const title = document.getElementById('placement-modal-title');
    const body = document.getElementById('placement-modal-body');
    title.textContent = `Level ${level} Placement Test`;
    body.innerHTML = `
      <div style="text-align: center; padding: 30px; color: var(--text-secondary);">
        <p>Loading placement test questions for Level ${level}...</p>
      </div>
    `;
    modal.classList.add('open');

    try {
      const data = await window.api.getPlacementTest(level);
      this.currentPlacementData = data;
      this.currentPlacementAnswers = {};

      let html = `
        <div style="margin-bottom: 20px;">
          <div style="font-size: 0.95rem; color: var(--text-secondary); line-height: 1.5; margin-bottom: 12px;">
            ${data.description || `Test your knowledge to fast-track directly into Level ${level}.`}
          </div>
          <div style="background: var(--bg-app-alt); border-left: 4px solid var(--tuscan-gold); padding: 10px 14px; border-radius: var(--radius-sm); font-size: 0.85rem; color: var(--text-primary);">
            🎯 <strong>Requirement:</strong> Score at least <strong>${data.passing_score}%</strong> (7 out of 10) to automatically unlock Level ${level} and earn <strong>+50 XP</strong>.
          </div>
        </div>

        <form onsubmit="window.app.handlePlacementSubmit(event, '${level}')">
          <div style="display: flex; flex-direction: column; gap: 18px; margin-bottom: 24px;">
      `;

      data.questions.forEach((q, idx) => {
        html += `
          <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: var(--radius-md); padding: 16px; box-shadow: var(--shadow-sm);">
            <div style="font-weight: 700; font-size: 0.95rem; margin-bottom: 10px; color: var(--text-primary);">
              <span style="display: inline-block; width: 24px; height: 24px; background: var(--terracotta-subtle); color: var(--terracotta); border-radius: 50%; text-align: center; line-height: 24px; font-size: 0.8rem; margin-right: 6px;">${idx + 1}</span>
              ${q.question}
            </div>
            <div style="display: grid; grid-template-columns: 1fr; gap: 8px;">
              ${q.options.map(opt => `
                <label style="display: flex; align-items: center; gap: 10px; padding: 10px 14px; border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); cursor: pointer; font-size: 0.9rem; transition: background 0.15s ease;">
                  <input type="radio" name="pq_${idx}" value="${opt.replace(/"/g, '&quot;')}" onchange="window.app.currentPlacementAnswers['${idx}'] = this.value" required>
                  <span>${opt}</span>
                </label>
              `).join('')}
            </div>
          </div>
        `;
      });

      html += `
          </div>
          <div id="placement-submit-error" style="display: none; background: #fee2e2; border: 1px solid #ef4444; color: #991b1b; padding: 10px; border-radius: var(--radius-sm); font-size: 0.85rem; margin-bottom: 14px;"></div>
          <button type="submit" class="btn-tactile" style="width: 100%; justify-content: center; padding: 14px; font-size: 1rem;">
            Submit Placement Test
          </button>
        </form>
      `;

      body.innerHTML = html;
    } catch (e) {
      body.innerHTML = `
        <div style="text-align: center; padding: 30px; color: #ef4444;">
          <p>Error loading placement test: ${e.message}</p>
          <button class="btn-secondary" style="margin-top: 10px;" onclick="window.app.closeModal('placement-modal')">Close</button>
        </div>
      `;
    }
  }

  async handlePlacementSubmit(event, level) {
    event.preventDefault();
    const body = document.getElementById('placement-modal-body');
    const errBox = document.getElementById('placement-submit-error');
    if (errBox) errBox.style.display = 'none';

    try {
      const res = await window.api.submitPlacementTest(level, this.currentPlacementAnswers || {});
      const passed = res.passed;
      if (passed) {
        window.soundEngine.playSuccess();
        this.triggerConfetti();
      } else {
        window.soundEngine.playWrong();
      }

      body.innerHTML = `
        <div style="text-align: center; padding: 20px 10px;">
          <div style="font-size: 3.5rem; margin-bottom: 12px;">${passed ? '🎉' : '📚'}</div>
          <h2 style="font-family: var(--font-serif); font-size: 1.8rem; color: ${passed ? 'var(--olive)' : 'var(--terracotta)'}; margin-bottom: 8px;">
            ${passed ? 'Placement Test Passed!' : 'Placement Test Not Passed'}
          </h2>
          <p style="font-size: 1rem; color: var(--text-primary); margin-bottom: 14px;">
            ${res.message}
          </p>
          <div style="display: inline-flex; align-items: center; gap: 16px; background: var(--bg-app-alt); padding: 12px 24px; border-radius: var(--radius-md); margin-bottom: 24px;">
            <div>
              <div style="font-size: 1.8rem; font-weight: 800; color: ${passed ? 'var(--olive)' : 'var(--terracotta)'};">${res.score}%</div>
              <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-secondary);">Your Score</div>
            </div>
            <div style="height: 30px; width: 1px; background: var(--border-prominent);"></div>
            <div>
              <div style="font-size: 1.8rem; font-weight: 800; color: var(--text-primary);">${res.correct_count} / ${res.total_questions}</div>
              <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-secondary);">Correct Answers</div>
            </div>
            <div style="height: 30px; width: 1px; background: var(--border-prominent);"></div>
            <div>
              <div style="font-size: 1.8rem; font-weight: 800; color: var(--tuscan-gold);">${res.passing_score}%</div>
              <div style="font-size: 0.75rem; text-transform: uppercase; color: var(--text-secondary);">Passing Score</div>
            </div>
          </div>

          <div style="max-height: 240px; overflow-y: auto; text-align: left; margin-bottom: 24px; border: 1px solid var(--border-subtle); border-radius: var(--radius-sm); padding: 12px; background: var(--bg-surface);">
            <div style="font-weight: 700; font-size: 0.85rem; color: var(--text-secondary); margin-bottom: 8px;">Question Breakdown:</div>
            ${res.evaluations.map((ev, i) => `
              <div style="padding: 8px; border-bottom: 1px solid var(--border-subtle); font-size: 0.85rem;">
                <div style="display: flex; gap: 8px; align-items: flex-start;">
                  <span>${ev.correct ? '✅' : '❌'}</span>
                  <div>
                    <strong>Q${i + 1}: ${ev.question}</strong>
                    ${!ev.correct ? `<div style="color: var(--terracotta); font-size: 0.8rem;">Correct answer: ${ev.correct_answer}</div>` : ''}
                    ${ev.explanation ? `<div style="color: var(--text-secondary); font-size: 0.75rem; font-style: italic;">${ev.explanation}</div>` : ''}
                  </div>
                </div>
              </div>
            `).join('')}
          </div>

          <div style="display: flex; gap: 12px; justify-content: center;">
            <button class="btn-tactile" onclick="window.app.closeModal('placement-modal'); window.app.updateUserStatsBar(); if (window.roadmapView) window.roadmapView.render();">
              ${passed ? '🚀 Go to Unlocked Level' : '🔄 Review Chapters'}
            </button>
          </div>
        </div>
      `;

      // Refresh current user data so stats and unlocked levels are updated
      await window.api.fetchCurrentUser();
      this.updateUserStatsBar();
    } catch (e) {
      if (errBox) {
        errBox.textContent = e.message;
        errBox.style.display = 'block';
      }
    }
  }

  // Lightweight Canvas Confetti
  triggerConfetti() {
    const canvas = document.getElementById('confetti-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const pieces = [];
    const colors = ['#d94a38', '#2d6a4f', '#d97706', '#0284c7', '#ffffff'];

    for (let i = 0; i < 90; i++) {
      pieces.push({
        x: canvas.width / 2,
        y: canvas.height / 2,
        vx: (Math.random() - 0.5) * 16,
        vy: (Math.random() - 0.5) * 16 - 4,
        size: Math.random() * 8 + 4,
        color: colors[Math.floor(Math.random() * colors.length)],
        rotation: Math.random() * 360,
        rSpeed: (Math.random() - 0.5) * 10
      });
    }

    let frame = 0;
    const animate = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      pieces.forEach(p => {
        p.x += p.vx;
        p.y += p.vy;
        p.vy += 0.25;
        p.rotation += p.rSpeed;

        ctx.save();
        ctx.translate(p.x, p.y);
        ctx.rotate((p.rotation * Math.PI) / 180);
        ctx.fillStyle = p.color;
        ctx.fillRect(-p.size / 2, -p.size / 2, p.size, p.size);
        ctx.restore();
      });

      frame++;
      if (frame < 120) {
        requestAnimationFrame(animate);
      } else {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
      }
    };
    animate();
  }
}

window.app = new Application();
document.addEventListener('DOMContentLoaded', () => {
  window.app.init();
});
