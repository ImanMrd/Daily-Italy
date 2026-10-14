/**
 * DAILY-ITALY — Friends & Community Leaderboard View
 * World-Class Gamification: Top-3 Podium, Interactive Metric Filters, & User Highlight
 */

class LeaderboardView {
  constructor(container) {
    this.container = container;
    this.leaders = [];
    this.currentFilter = 'xp'; // 'xp', 'streak', 'mastery'
  }

  async render() {
    if (!window.api.user) {
      this.container.innerHTML = `
        <div class="auth-gate-card">
          <div class="auth-gate-icon">🏆</div>
          <h2 style="font-family: var(--font-serif); font-size: 1.8rem; margin-bottom: 12px; color: var(--text-primary);">
            Community Leaderboard
          </h2>
          <p style="color: var(--text-secondary); max-width: 540px; margin: 0 auto 24px; line-height: 1.6;">
            Compare your learning progress, XP points, and daily streaks with your friends. Log in or create an account to climb the Italian ranks!
          </p>
          <div style="display: flex; gap: 12px; justify-content: center; flex-wrap: wrap;">
            <button class="btn-tactile" onclick="window.app.openAuthModal(false)">🔑 Log In to Account</button>
            <button class="btn-secondary" onclick="window.app.openAuthModal(true)">✨ Create Free Account</button>
          </div>
        </div>
      `;
      return;
    }

    this.container.innerHTML = `
      <div style="text-align: center; padding: 48px; color: var(--text-secondary);">
        <p style="font-size: 1.1rem; font-weight: 600;">Loading leaderboard rankings...</p>
      </div>
    `;

    try {
      this.leaders = await window.api.getLeaderboard();
      this.renderBoard();
    } catch (e) {
      this.container.innerHTML = `
        <div style="text-align: center; padding: 40px; color: #ef4444;">
          <p>Error loading leaderboard: ${e.message}</p>
          <button class="btn-secondary" style="margin-top: 12px;" onclick="window.leaderboardView.render()">Try Again</button>
        </div>
      `;
    }
  }

  setFilter(filter) {
    this.currentFilter = filter;
    this.renderBoard();
  }

  getAvatarColor(name) {
    const gradients = [
      'linear-gradient(135deg, #d94a38 0%, #b83827 100%)',
      'linear-gradient(135deg, #0284c7 0%, #0369a1 100%)',
      'linear-gradient(135deg, #2d6a4f 0%, #1b4332 100%)',
      'linear-gradient(135deg, #d97706 0%, #b45309 100%)',
      'linear-gradient(135deg, #7c3aed 0%, #5b21b6 100%)',
      'linear-gradient(135deg, #db2777 0%, #9d174d 100%)',
      'linear-gradient(135deg, #059669 0%, #047857 100%)'
    ];
    let hash = 0;
    for (let i = 0; i < (name || '').length; i++) {
      hash = name.charCodeAt(i) + ((hash << 5) - hash);
    }
    const idx = Math.abs(hash) % gradients.length;
    return gradients[idx];
  }

  renderBoard() {
    const currentUser = window.api.user;
    
    // Sort according to current active filter
    let sorted = [...this.leaders];
    if (this.currentFilter === 'streak') {
      sorted.sort((a, b) => (b.streak_days || 0) - (a.streak_days || 0));
    } else if (this.currentFilter === 'mastery') {
      sorted.sort((a, b) => (b.mastered_count || 0) - (a.mastered_count || 0));
    } else {
      sorted.sort((a, b) => (b.xp || 0) - (a.xp || 0));
    }

    // Find current user rank
    const userIndex = sorted.findIndex(u => u.username === (currentUser && currentUser.username));
    const userRank = userIndex !== -1 ? userIndex + 1 : null;

    let html = `
      <div class="leaderboard-view">
        <div class="leaderboard-header">
          <div class="hero-pill" style="margin-bottom: 10px;">
            🏆 Community Hall of Fame
          </div>
          <h1>Friends & Community Leaderboard</h1>
          <p>
            Challenge your fellow learners! Earn XP by completing CEFR chapters, scoring 70%+ on placement tests, and maintaining your daily Italian streak.
          </p>

          <!-- Interactive Metric Filter Pills -->
          <div class="leaderboard-tabs">
            <button 
              class="leaderboard-tab-btn ${this.currentFilter === 'xp' ? 'active' : ''}" 
              onclick="window.leaderboardView.setFilter('xp')">
              ⭐ Total XP
            </button>
            <button 
              class="leaderboard-tab-btn ${this.currentFilter === 'streak' ? 'active' : ''}" 
              onclick="window.leaderboardView.setFilter('streak')">
              🔥 Daily Streak
            </button>
            <button 
              class="leaderboard-tab-btn ${this.currentFilter === 'mastery' ? 'active' : ''}" 
              onclick="window.leaderboardView.setFilter('mastery')">
              📚 Words Mastered
            </button>
          </div>
        </div>
    `;

    // Top 3 Podium (rendered if at least 3 users exist)
    if (sorted.length >= 3) {
      const first = sorted[0];
      const second = sorted[1];
      const third = sorted[2];

      const getStatText = (u) => {
        if (this.currentFilter === 'streak') return `${u.streak_days} Days`;
        if (this.currentFilter === 'mastery') return `${u.mastered_count} Words`;
        return `${u.xp} XP`;
      };

      html += `
        <div class="podium-container">
          <!-- 2nd Place (Silver) -->
          <div class="podium-step rank-2">
            <div class="podium-medal">🥈</div>
            <div class="podium-avatar" style="background: ${this.getAvatarColor(second.username)};">
              ${(second.username || 'IT').slice(0, 2).toUpperCase()}
            </div>
            <div class="podium-name" title="${second.username}">${second.username}</div>
            <div class="podium-stat">🔥 ${second.streak_days}d &bull; 📚 ${second.mastered_count}</div>
            <div class="podium-badge">${getStatText(second)}</div>
          </div>

          <!-- 1st Place (Gold) -->
          <div class="podium-step rank-1">
            <div class="podium-medal">🥇</div>
            <div class="podium-avatar" style="background: ${this.getAvatarColor(first.username)};">
              ${(first.username || 'IT').slice(0, 2).toUpperCase()}
            </div>
            <div class="podium-name" title="${first.username}">${first.username}</div>
            <div class="podium-stat">🔥 ${first.streak_days}d &bull; 📚 ${first.mastered_count}</div>
            <div class="podium-badge">${getStatText(first)}</div>
          </div>

          <!-- 3rd Place (Bronze) -->
          <div class="podium-step rank-3">
            <div class="podium-medal">🥉</div>
            <div class="podium-avatar" style="background: ${this.getAvatarColor(third.username)};">
              ${(third.username || 'IT').slice(0, 2).toUpperCase()}
            </div>
            <div class="podium-name" title="${third.username}">${third.username}</div>
            <div class="podium-stat">🔥 ${third.streak_days}d &bull; 📚 ${third.mastered_count}</div>
            <div class="podium-badge">${getStatText(third)}</div>
          </div>
        </div>
      `;
    }

    // Full Ranked List Card
    html += `
      <div class="leaderboard-card">
    `;

    sorted.forEach((u, idx) => {
      const rank = idx + 1;
      let rankClass = '';
      let rankBadge = `${rank}`;
      if (rank === 1) { rankClass = 'top-1'; rankBadge = '🥇'; }
      else if (rank === 2) { rankClass = 'top-2'; rankBadge = '🥈'; }
      else if (rank === 3) { rankClass = 'top-3'; rankBadge = '🥉'; }

      const isCurrent = currentUser && (u.username === currentUser.username);
      const initials = (u.username || 'IT').slice(0, 2).toUpperCase();
      const avatarBg = this.getAvatarColor(u.username);

      let primaryStatBadge = `⭐ ${u.xp} XP`;
      if (this.currentFilter === 'streak') {
        primaryStatBadge = `🔥 ${u.streak_days} Days`;
      } else if (this.currentFilter === 'mastery') {
        primaryStatBadge = `📚 ${u.mastered_count} Words`;
      }

      html += `
        <div class="leader-item ${isCurrent ? 'current-user' : ''}">
          <div class="leader-rank ${rankClass}">${rankBadge}</div>
          <div class="leader-avatar" style="background: ${avatarBg};">
            ${initials}
          </div>
          <div class="leader-info">
            <div class="leader-name-row">
              <span class="leader-name">${u.username}</span>
              ${isCurrent ? `<span class="leader-you-badge">YOU</span>` : ''}
            </div>
            <div class="leader-sub">
              <span>🔥 ${u.streak_days} days streak</span>
              <span>&bull;</span>
              <span>📚 ${u.mastered_count} words mastered</span>
              <span>&bull;</span>
              <span>⭐ ${u.xp} XP</span>
            </div>
          </div>
          <div class="leader-score">${primaryStatBadge}</div>
        </div>
      `;
    });

    html += `
        </div>
      </div>
    `;

    this.container.innerHTML = html;
  }
}

window.LeaderboardView = LeaderboardView;
