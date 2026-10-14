/**
 * PAROLE 3000 - Central API Client
 */

const API_BASE = '/api';

class ApiClient {
  constructor() {
    this.token = localStorage.getItem('parole_token') || null;
    this.user = null;
    const cachedUser = localStorage.getItem('parole_user');
    if (cachedUser) {
      try { this.user = JSON.parse(cachedUser); } catch (e) {}
    }
  }

  setSession(token, user) {
    this.token = token;
    this.user = user;
    localStorage.setItem('parole_token', token);
    localStorage.setItem('parole_user', JSON.stringify(user));
  }

  clearSession() {
    this.token = null;
    this.user = null;
    localStorage.removeItem('parole_token');
    localStorage.removeItem('parole_user');
  }

  async request(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const headers = {
      'Content-Type': 'application/json',
      ...(options.headers || {})
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    const response = await fetch(url, { ...options, headers });

    if (response.status === 401) {
      // Clear expired session
      this.clearSession();
      window.dispatchEvent(new CustomEvent('auth-changed'));
    }

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Network request failed' }));
      throw new Error(errorData.detail || 'Request failed');
    }

    return response.json();
  }

  // Auth methods
  async register(username, password, email) {
    const data = await this.request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ username, password, email })
    });
    this.setSession(data.access_token, data.user);
    return data.user;
  }

  async login(username, password) {
    const data = await this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    });
    this.setSession(data.access_token, data.user);
    return data.user;
  }

  async fetchCurrentUser() {
    if (!this.token) return null;
    try {
      const user = await this.request('/auth/me');
      this.user = user;
      localStorage.setItem('parole_user', JSON.stringify(user));
      return user;
    } catch (e) {
      return null;
    }
  }

  // Curriculum & Learning
  async getStages() {
    return this.request('/curriculum/stages');
  }

  async getLessonDetail(lessonId) {
    return this.request(`/curriculum/lesson/${lessonId}`);
  }

  async getWords(lessonId) {
    return this.request(`/words/lesson/${lessonId}`);
  }

  async getExercises(lessonId) {
    return this.request(`/exercises/lesson/${lessonId}`);
  }

  async checkAnswer(exerciseId, userAnswer) {
    return this.request('/exercises/check-answer', {
      method: 'POST',
      body: JSON.stringify({ exercise_id: exerciseId, user_answer: userAnswer })
    });
  }

  async submitExercises(lessonId, submissions) {
    return this.request('/exercises/submit', {
      method: 'POST',
      body: JSON.stringify({ lesson_id: lessonId, submissions })
    });
  }

  // Spaced Repetition (SRS) Smart Review
  async getReviewQueue(filterMode = 'all') {
    return this.request(`/review/queue?filter_mode=${filterMode}`);
  }

  // Chapters Curriculum (A1: 10, A2: 10, B1: 20, B2: 20)
  async getChaptersOverview() {
    return this.request('/chapters/overview');
  }

  async getChapterDetail(chapterId) {
    return this.request(`/chapters/chapter/${chapterId}`);
  }

  async completeChapterPart(chapterId, part, extra = {}) {
    return this.request(`/chapters/chapter/${chapterId}/complete-part`, {
      method: 'POST',
      body: JSON.stringify({ part, ...extra })
    });
  }

  // Level Placement Tests
  async getPlacementTest(level) {
    return this.request(`/chapters/placement/${level}`);
  }

  async submitPlacementTest(level, answers) {
    return this.request(`/chapters/placement/${level}/submit`, {
      method: 'POST',
      body: JSON.stringify({ answers })
    });
  }

  // RBAC Admin Methods
  async getAdminOverview() {
    return this.request('/admin/overview');
  }

  async getAdminUsers(query = '') {
    const url = query ? `/admin/users?query=${encodeURIComponent(query)}` : '/admin/users';
    return this.request(url);
  }

  async updateUserRole(userId, role) {
    return this.request(`/admin/users/${userId}/role`, {
      method: 'PUT',
      body: JSON.stringify({ role })
    });
  }

  async adminUnlockUserLevel(userId, level) {
    return this.request(`/admin/users/${userId}/unlock-level`, {
      method: 'PUT',
      body: JSON.stringify({ level })
    });
  }

  async adminDeleteUser(userId) {
    return this.request(`/admin/users/${userId}`, {
      method: 'DELETE'
    });
  }

  async adminGetPlacementTests() {
    return this.request('/admin/placement-tests');
  }

  async adminUpdatePlacementThreshold(level, passingScore) {
    return this.request(`/admin/placement-tests/${level}/threshold`, {
      method: 'PUT',
      body: JSON.stringify({ passing_score: passingScore })
    });
  }

  async adminReseedCurriculum() {
    return this.request('/admin/curriculum/reseed', {
      method: 'POST'
    });
  }


  async submitReviewRating(wordId, rating) {
    return this.request('/review/submit', {
      method: 'POST',
      body: JSON.stringify({ word_id: wordId, rating })
    });
  }

  async submitReview(wordId, rating) {
    return this.submitReviewRating(wordId, rating);
  }

  // Grammar Lessons
  async getGrammarLessons(level = '') {
    const url = level ? `/grammar/lessons?level=${encodeURIComponent(level)}` : '/grammar/lessons';
    return this.request(url);
  }

  async getGrammarLessonDetail(lessonId) {
    return this.request(`/grammar/lesson/${lessonId}`);
  }

  // Reading Passages
  async getReadingPassages(level = '') {
    const url = level ? `/readings?level=${encodeURIComponent(level)}` : '/readings';
    return this.request(url);
  }

  async getReadingPassageDetail(passageId) {
    return this.request(`/readings/${passageId}`);
  }

  async submitReadingAnswers(passageId, answers) {
    return this.request(`/readings/${passageId}/submit`, {
      method: 'POST',
      body: JSON.stringify({ answers })
    });
  }

  // Writing Prompts
  async getWritingPrompts(level = '') {
    const url = level ? `/writing/prompts?level=${encodeURIComponent(level)}` : '/writing/prompts';
    return this.request(url);
  }

  async evaluateWriting(promptId, userText) {
    return this.request('/writing/evaluate', {
      method: 'POST',
      body: JSON.stringify({ prompt_id: promptId, user_text: userText })
    });
  }

  // Stats & Leaderboard
  async getStats() {
    return this.request('/stats/summary');
  }

  async getLeaderboard() {
    return this.request('/stats/leaderboard');
  }

  // Content Extension
  async addCustomWord(wordData) {
    return this.request('/words/custom', {
      method: 'POST',
      body: JSON.stringify(wordData)
    });
  }
}

window.api = new ApiClient();
