/**
 * DAILY-ITALY — RBAC Admin Management Control Panel View
 * Features:
 * - Real-time metrics overview
 * - User Management (search, role toggle, delete, 1-click level unlock)
 * - Placement Test Threshold configurator (default 70%)
 * - Curriculum reseeding & custom vocabulary injection
 */

class AdminView {
  constructor(container) {
    this.container = container;
    this.searchQuery = '';
  }

  async render() {
    this.container.innerHTML = `
      <div style="text-align: center; padding: 40px; color: var(--text-secondary);">
        <p>Loading Admin Control Panel...</p>
      </div>
    `;

    try {
      const overview = await window.api.getAdminOverview();
      const users = await window.api.getAdminUsers(this.searchQuery);
      const placementTests = await window.api.adminGetPlacementTests().catch(() => []);
      this.renderAdminDashboard(overview, users, placementTests);
    } catch (e) {
      this.container.innerHTML = `
        <div style="text-align: center; padding: 40px; max-width: 500px; margin: 40px auto; background: var(--bg-surface); border-radius: var(--radius-lg); border: 1px solid var(--border-prominent);">
          <div style="font-size: 2.5rem; margin-bottom: 12px;">🔒</div>
          <h2 style="font-family: var(--font-serif); font-size: 1.6rem; margin-bottom: 8px;">Access Restricted</h2>
          <p style="color: var(--text-secondary); margin-bottom: 20px;">
            This management control panel requires Administrator privileges (RBAC). Please log in with an administrator account (e.g. <code>admin</code> / <code>admin123</code>).
          </p>
          <button class="btn-tactile" onclick="window.app.openAuthModal(false)">
            Log In as Administrator
          </button>
        </div>
      `;
    }
  }

  renderAdminDashboard(overview, users, placementTests) {
    let html = `
      <div class="admin-view" style="max-width: 1040px; margin: 0 auto 50px;">
        
        <!-- Header -->
        <div style="margin-bottom: 28px; display: flex; justify-content: space-between; align-items: flex-end; flex-wrap: wrap; gap: 14px;">
          <div>
            <div class="hero-pill" style="margin-bottom: 8px; background: #e0f2fe; color: #0284c7; border-color: rgba(2, 132, 199, 0.3);">
              🛡️ RBAC Management Control Panel
            </div>
            <h1 style="font-family: var(--font-serif); font-size: 2.2rem; color: var(--text-primary); margin-bottom: 4px;">
              Daily-Italy Administration
            </h1>
            <p style="color: var(--text-secondary); font-size: 0.95rem;">
              Manage learners, enforce unique usernames, adjust placement pass thresholds, and oversee the 60-chapter curriculum.
            </p>
          </div>
          <div style="display: flex; gap: 10px; flex-wrap: wrap;">
            <button class="btn-tactile" onclick="window.app.openAddWordModal()">
              ➕ Add Vocabulary Word
            </button>
            <button class="btn-secondary" onclick="window.adminView.handleReseedCurriculum()">
              🔄 Reseed Curriculum
            </button>
          </div>
        </div>

        <!-- Metrics Overview Grid -->
        <div class="admin-stats-grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: 16px; margin-bottom: 32px;">
          <div class="admin-card">
            <div style="font-size: 0.8rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700;">Total Users</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: var(--terracotta);">${overview.total_users}</div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">${overview.total_admins} administrators</div>
          </div>
          <div class="admin-card">
            <div style="font-size: 0.8rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700;">Total Words</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: var(--olive);">${overview.total_words}</div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">CEFR Vocabulary Bank</div>
          </div>
          <div class="admin-card">
            <div style="font-size: 0.8rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700;">Curriculum Chapters</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: var(--amalfi-deep);">60</div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">A1 (10) &bull; A2 (10) &bull; B1 (20) &bull; B2 (20)</div>
          </div>
          <div class="admin-card">
            <div style="font-size: 0.8rem; text-transform: uppercase; color: var(--text-muted); font-weight: 700;">Exercises & Quizzes</div>
            <div style="font-size: 2.2rem; font-weight: 800; color: var(--tuscan-gold);">${overview.total_exercises}</div>
            <div style="font-size: 0.75rem; color: var(--text-muted);">Cloze, MCQ & Consolidation</div>
          </div>
        </div>

        <!-- User Management Table with Search -->
        <div class="admin-card" style="margin-bottom: 32px;">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px; flex-wrap: wrap; gap: 12px;">
            <div>
              <h3 style="font-family: var(--font-serif); font-size: 1.3rem; color: var(--text-primary); margin-bottom: 2px;">
                👥 User Management & Access Control
              </h3>
              <p style="font-size: 0.85rem; color: var(--text-secondary);">
                Promote administrators, manually unlock CEFR levels, or remove users.
              </p>
            </div>
            <div>
              <input 
                type="text" 
                id="admin-user-search-input"
                class="form-control" 
                placeholder="Search by username..." 
                value="${this.searchQuery}"
                oninput="window.adminView.handleSearch(this.value)"
                style="padding: 8px 14px; font-size: 0.85rem; width: 220px;"
              >
            </div>
          </div>

          <div style="overflow-x: auto;">
            <table class="admin-table" style="width: 100%; border-collapse: collapse; font-size: 0.88rem;">
              <thead>
                <tr style="border-bottom: 2px solid var(--border-subtle); text-align: left;">
                  <th style="padding: 10px;">ID</th>
                  <th style="padding: 10px;">Username</th>
                  <th style="padding: 10px;">Role</th>
                  <th style="padding: 10px;">Unlocked Levels</th>
                  <th style="padding: 10px;">XP / Streak</th>
                  <th style="padding: 10px;">Actions</th>
                </tr>
              </thead>
              <tbody>
    `;

    if (users.length === 0) {
      html += `
        <tr>
          <td colspan="6" style="padding: 24px; text-align: center; color: var(--text-secondary);">
            No users match the search query.
          </td>
        </tr>
      `;
    } else {
      users.forEach(u => {
        const isAdmin = u.role === 'admin';
        const unlockedLevels = (u.unlocked_levels || 'A1').split(',').map(s => s.trim().toUpperCase());

        html += `
          <tr style="border-bottom: 1px solid var(--border-subtle);">
            <td style="padding: 10px; color: var(--text-muted);">#${u.id}</td>
            <td style="padding: 10px; font-weight: 700; color: var(--text-primary);">${u.username}</td>
            <td style="padding: 10px;">
              <span style="display: inline-block; padding: 2px 10px; border-radius: var(--radius-full); font-size: 0.75rem; font-weight: 700; background: ${isAdmin ? '#e0f2fe' : '#f3f4f6'}; color: ${isAdmin ? '#0284c7' : '#4b5563'};">
                ${isAdmin ? 'Administrator' : 'Learner'}
              </span>
            </td>
            <td style="padding: 10px;">
              <div style="display: flex; gap: 4px; flex-wrap: wrap;">
                ${['A1', 'A2', 'B1', 'B2'].map(lvl => `
                  <span style="font-size: 0.72rem; padding: 2px 6px; border-radius: 4px; background: ${unlockedLevels.includes(lvl) ? 'var(--olive-subtle)' : 'var(--bg-app-alt)'}; color: ${unlockedLevels.includes(lvl) ? 'var(--olive)' : 'var(--text-muted)'}; font-weight: 700;">
                    ${lvl}
                  </span>
                `).join('')}
              </div>
            </td>
            <td style="padding: 10px;">
              ⭐ ${u.xp} XP &bull; 🔥 ${u.streak_days}d
            </td>
            <td style="padding: 10px;">
              <div style="display: flex; gap: 6px; align-items: center; flex-wrap: wrap;">
                <button 
                  class="btn-secondary" 
                  style="padding: 4px 8px; font-size: 0.75rem;" 
                  onclick="window.adminView.toggleRole(${u.id}, '${isAdmin ? 'user' : 'admin'}')"
                >
                  ${isAdmin ? 'Demote to User' : 'Make Admin'}
                </button>
                
                ${!unlockedLevels.includes('A2') ? `
                  <button class="btn-secondary" style="padding: 4px 6px; font-size: 0.72rem; color: var(--tuscan-gold);" onclick="window.adminView.unlockLevel(${u.id}, 'A2')" title="Unlock Level A2">
                    + A2
                  </button>
                ` : ''}
                ${!unlockedLevels.includes('B1') ? `
                  <button class="btn-secondary" style="padding: 4px 6px; font-size: 0.72rem; color: var(--amalfi-blue);" onclick="window.adminView.unlockLevel(${u.id}, 'B1')" title="Unlock Level B1">
                    + B1
                  </button>
                ` : ''}
                ${!unlockedLevels.includes('B2') ? `
                  <button class="btn-secondary" style="padding: 4px 6px; font-size: 0.72rem; color: var(--terracotta);" onclick="window.adminView.unlockLevel(${u.id}, 'B2')" title="Unlock Level B2">
                    + B2
                  </button>
                ` : ''}

                <button 
                  class="btn-secondary" 
                  style="padding: 4px 8px; font-size: 0.75rem; color: #dc2626; border-color: rgba(220, 38, 38, 0.3);" 
                  onclick="window.adminView.deleteUser(${u.id}, '${u.username}')"
                  title="Delete user"
                >
                  🗑️
                </button>
              </div>
            </td>
          </tr>
        `;
      });
    }

    html += `
              </tbody>
            </table>
          </div>
        </div>

        <!-- Placement Test Threshold Configuration -->
        <div class="admin-card">
          <div style="margin-bottom: 16px;">
            <h3 style="font-family: var(--font-serif); font-size: 1.3rem; color: var(--text-primary); margin-bottom: 4px;">
              🎯 Placement Test Thresholds & Level Gates
            </h3>
            <p style="font-size: 0.85rem; color: var(--text-secondary);">
              Configure the minimum passing score percentage required for learners to fast-track directly into advanced CEFR levels (Default: 70%).
            </p>
          </div>

          <div style="overflow-x: auto;">
            <table class="admin-table" style="width: 100%; border-collapse: collapse; font-size: 0.88rem;">
              <thead>
                <tr style="border-bottom: 2px solid var(--border-subtle); text-align: left;">
                  <th style="padding: 10px;">Target Level</th>
                  <th style="padding: 10px;">Test Title</th>
                  <th style="padding: 10px;">Questions</th>
                  <th style="padding: 10px;">Passing Score</th>
                  <th style="padding: 10px;">Update Threshold</th>
                </tr>
              </thead>
              <tbody>
    `;

    placementTests.forEach(pt => {
      html += `
        <tr style="border-bottom: 1px solid var(--border-subtle);">
          <td style="padding: 10px;">
            <span class="stage-level-tag">Level ${pt.target_level}</span>
          </td>
          <td style="padding: 10px; font-weight: 600;">${pt.title}</td>
          <td style="padding: 10px;">${pt.question_count} Questions</td>
          <td style="padding: 10px; font-weight: 800; color: var(--tuscan-gold);">
            ${pt.passing_score}%
          </td>
          <td style="padding: 10px;">
            <div style="display: flex; gap: 8px; align-items: center;">
              <input 
                type="number" 
                id="threshold-input-${pt.target_level}" 
                class="form-control" 
                min="50" 
                max="100" 
                value="${pt.passing_score}" 
                style="width: 75px; padding: 4px 8px; font-size: 0.85rem;"
              >
              <span style="font-size: 0.85rem;">%</span>
              <button 
                class="btn-secondary" 
                style="padding: 4px 10px; font-size: 0.78rem;" 
                onclick="window.adminView.updatePlacementThreshold('${pt.target_level}')"
              >
                Save
              </button>
            </div>
          </td>
        </tr>
      `;
    });

    html += `
              </tbody>
            </table>
          </div>
        </div>

      </div>
    `;

    this.container.innerHTML = html;
  }

  handleSearch(query) {
    this.searchQuery = query;
    // Debounced render
    clearTimeout(this._searchTimer);
    this._searchTimer = setTimeout(() => {
      this.render();
    }, 300);
  }

  async toggleRole(userId, newRole) {
    if (!confirm(`Are you sure you want to change this user's role to "${newRole}"?`)) return;
    try {
      await window.api.updateUserRole(userId, newRole);
      window.soundEngine.playSuccess();
      this.render();
    } catch (e) {
      alert(`Error updating role: ${e.message}`);
    }
  }

  async unlockLevel(userId, level) {
    if (!confirm(`Are you sure you want to manually unlock Level ${level} for this user?`)) return;
    try {
      await window.api.adminUnlockUserLevel(userId, level);
      window.soundEngine.playSuccess();
      this.render();
    } catch (e) {
      alert(`Error unlocking level: ${e.message}`);
    }
  }

  async deleteUser(userId, username) {
    if (!confirm(`Are you sure you want to permanently delete user "${username}" (ID: #${userId})? This action cannot be undone.`)) return;
    try {
      await window.api.adminDeleteUser(userId);
      window.soundEngine.playSuccess();
      this.render();
    } catch (e) {
      alert(`Error deleting user: ${e.message}`);
    }
  }

  async updatePlacementThreshold(level) {
    const input = document.getElementById(`threshold-input-${level}`);
    if (!input) return;
    const newScore = parseInt(input.value, 10);
    if (isNaN(newScore) || newScore < 50 || newScore > 100) {
      alert('Please enter a valid threshold percentage between 50% and 100%.');
      return;
    }

    try {
      await window.api.adminUpdatePlacementThreshold(level, newScore);
      window.soundEngine.playSuccess();
      alert(`Placement test passing threshold for Level ${level} updated to ${newScore}%.`);
      this.render();
    } catch (e) {
      alert(`Error updating threshold: ${e.message}`);
    }
  }

  async handleReseedCurriculum() {
    if (!confirm('Are you sure you want to reseed the curriculum? This refreshes all 60 chapters across A1, A2, B1, and B2.')) return;
    try {
      const res = await window.api.adminReseedCurriculum();
      window.soundEngine.playSuccess();
      alert(res.message || 'Curriculum successfully reseeded!');
      this.render();
    } catch (e) {
      alert(`Error reseeding curriculum: ${e.message}`);
    }
  }
}

window.AdminView = AdminView;
