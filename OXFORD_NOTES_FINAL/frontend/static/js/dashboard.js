/* Oxford LMS — Dashboard SPA */
'use strict';

// ─── STATE ────────────────────────────────────────────────────────────────────
let G = { user: null, page: 'dashboard' };

// ─── SVG ICONS ────────────────────────────────────────────────────────────────
const I = {
  dashboard:  `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>`,
  students:   `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 00-3-3.87M16 3.13a4 4 0 010 7.75"/></svg>`,
  courses:    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"/></svg>`,
  batches:    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>`,
  attendance: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/></svg>`,
  fees:       `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="5" width="20" height="14" rx="2"/><path d="M2 10h20"/></svg>`,
  notes:      `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>`,
  reports:    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>`,
  activity:   `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>`,
  settings:   `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-4 0v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83-2.83l.06-.06A1.65 1.65 0 004.68 15a1.65 1.65 0 00-1.51-1H3a2 2 0 010-4h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 012.83-2.83l.06.06A1.65 1.65 0 009 4.68a1.65 1.65 0 001-1.51V3a2 2 0 014 0v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 2.83l-.06.06A1.65 1.65 0 0019.4 9a1.65 1.65 0 001.51 1H21a2 2 0 010 4h-.09a1.65 1.65 0 00-1.51 1z"/></svg>`,
  favorites:  `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>`,
  plus:       `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>`,
  edit:       `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>`,
  trash:      `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 01-2 2H8a2 2 0 01-2-2L5 6m3 0V4a1 1 0 011-1h4a1 1 0 011 1v2"/></svg>`,
  eye:        `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>`,
  download:   `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>`,
  receipt:    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 00-2 2v16l3-2 3 2 3-2 3 2 3-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>`,
  alert_tri: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`,
  export:     `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>`,
  profile:    `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>`,
};

// ─── HELPERS ──────────────────────────────────────────────────────────────────
const el   = id => document.getElementById(id);
const html = (id, content) => { const e = el(id); if (e) e.innerHTML = content; };
const api  = async (url, opts={}) => {
  const res  = await fetch(url, opts);
  const data = await res.json().catch(() => ({}));
  return { ok: res.ok, status: res.status, data };
};
const fmtDate  = d => d ? new Date(d).toLocaleDateString('en-IN') : '—';
const fmtMoney = v => v != null ? `Rs. ${parseFloat(v).toLocaleString('en-IN', {minimumFractionDigits:0})}` : '—';
const spinner  = () => `<div class="spinner-wrap"><div class="spinner"></div></div>`;
const emptyState = (msg='No data found') => `<div class="empty-state"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" width="48" height="48"><path d="M20 13V6a2 2 0 00-2-2H6a2 2 0 00-2 2v7m16 0v5a2 2 0 01-2 2H6a2 2 0 01-2-2v-5m16 0h-2.586a1 1 0 00-.707.293l-2.414 2.414a1 1 0 01-.707.293h-3.172a1 1 0 01-.707-.293l-2.414-2.414A1 1 0 006.586 13H4"/></svg><p>${msg}</p></div>`;
const badge = (text, type='gray') => `<span class="badge badge-${type}">${text}</span>`;

function statusBadge(status) {
  const map = {
    active:'success', completed:'info', on_hold:'warning', dropped:'danger',
    present:'success', absent:'danger', late:'warning', excused:'info',
    paid:'success', due_soon:'warning', overdue:'danger',
    archived:'gray', inactive:'gray'
  };
  return badge(status?.replace(/_/g,' ') || '—', map[status] || 'gray');
}

// ─── MODAL ────────────────────────────────────────────────────────────────────
function showModal(content, size='modal-md') {
  const root = el('modalRoot');
  root.innerHTML = `<div class="modal-overlay" id="modalOverlay" onclick="if(event.target===this)closeModal()">
    <div class="modal-box ${size}">${content}</div></div>`;
}
function closeModal() { const r = el('modalRoot'); if (r) r.innerHTML = ''; }

function modalHeader(title) {
  return `<div class="modal-header"><h3>${title}</h3>
    <button class="modal-close" onclick="closeModal()">&#x2715;</button></div>`;
}

// Confirmation dialog
function confirmDialog(message, onConfirm) {
  showModal(`
    ${modalHeader('Confirm Action')}
    <div class="modal-body"><p style="font-size:14px;color:var(--gray-700);">${message}</p></div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-danger" onclick="(${onConfirm.toString()})();closeModal()">Confirm</button>
    </div>`, 'modal-sm');
}

// Toast notification
function toast(message, type='success') {
  const t = document.createElement('div');
  t.className = `alert alert-${type}`;
  t.style.cssText = 'position:fixed;bottom:24px;right:24px;z-index:9999;min-width:280px;box-shadow:var(--shadow-lg);animation:slideUp .2s ease';
  t.innerHTML = message;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 3500);
}

// ─── INIT ─────────────────────────────────────────────────────────────────────
async function init() {
  const { ok, data } = await api('/api/auth/me');
  if (!ok) { window.location.href = '/login'; return; }
  G.user = data.user;
  buildSidebar();
  updateTopbarProfile();
  loadNotifCount();
  navigate('dashboard');
}

function buildSidebar() {
  const u = G.user;
  const avatarUrl = u.profile_image
    ? `/api/profile-image/${u.profile_image}`
    : `https://ui-avatars.com/api/?name=${encodeURIComponent(u.full_name||u.username)}&background=1e3a5f&color=f59e0b&size=64`;

  el('sidebarAvatar').src = avatarUrl;
  el('sidebarName').textContent   = u.full_name || u.username;
  el('sidebarRole').textContent   = u.role.toUpperCase();

  const adminNav = [
    { section: 'Main' },
    { id:'dashboard',  label:'Dashboard',   icon: I.dashboard },
    { section: 'Institute' },
    { id:'students',   label:'Students',    icon: I.students },
    { id:'courses',    label:'Courses',     icon: I.courses },
    { id:'batches',    label:'Batches',     icon: I.batches },
    { section: 'Operations' },
    { id:'attendance', label:'Attendance',  icon: I.attendance },
    { id:'fees',       label:'Fees',        icon: I.fees },
    { id:'notes',      label:'Study Notes', icon: I.notes },
    { section: 'System' },
    { id:'reports',    label:'Reports',     icon: I.reports },
    { id:'activity',   label:'Activity',    icon: I.activity },
    { id:'settings',   label:'Settings',    icon: I.settings },
  ];

  const studentNav = [
    { section: 'Menu' },
    { id:'dashboard',      label:'Dashboard',  icon: I.dashboard },
    { id:'my-course',      label:'My Course',  icon: I.courses },
    { id:'my-attendance',  label:'Attendance', icon: I.attendance },
    { id:'my-fees',        label:'Fees',       icon: I.fees },
    { id:'my-notes',       label:'Notes',      icon: I.notes },
    { id:'favorites',      label:'Favorites',  icon: I.favorites },
    { id:'my-profile',     label:'Profile',    icon: I.profile },
  ];

  const items = u.role === 'student' ? studentNav : adminNav;
  el('sidebarNav').innerHTML = items.map(item => {
    if (item.section) return `<div class="nav-section-label">${item.section}</div>`;
    return `<div class="nav-item" data-page="${item.id}" onclick="navigate('${item.id}')">
      ${item.icon}<span>${item.label}</span></div>`;
  }).join('');
}

function updateTopbarProfile() {
  const u = G.user;
  const src = u.profile_image
    ? `/api/profile-image/${u.profile_image}`
    : `https://ui-avatars.com/api/?name=${encodeURIComponent(u.full_name||u.username)}&background=1e3a5f&color=f59e0b&size=64`;
  el('topbarAvatar').src = src;
}

async function loadNotifCount() {
  const { ok, data } = await api('/api/dashboard/notifications');
  if (!ok) return;
  const badge = el('notifBadge');
  if (data.unread_count > 0) {
    badge.textContent = data.unread_count; badge.style.display = 'flex';
  } else {
    badge.style.display = 'none';
  }
}

// ─── NAVIGATION ───────────────────────────────────────────────────────────────
function navigate(page) {
  G.page = page;
  // Update active nav
  document.querySelectorAll('.nav-item').forEach(n => {
    n.classList.toggle('active', n.dataset.page === page);
  });
  const titles = {
    dashboard:'Dashboard', students:'Students', courses:'Courses', batches:'Batches',
    attendance:'Attendance', fees:'Fees', notes:'Study Notes', reports:'Reports',
    activity:'Activity Log', settings:'Settings', favorites:'Favorites',
    'my-course':'My Course', 'my-attendance':'My Attendance',
    'my-fees':'My Fees', 'my-notes':'My Notes', 'my-profile':'Profile'
  };
  el('pageTitle').textContent = titles[page] || page;
  html('pageContent', spinner());

  const loaders = {
    dashboard:     loadDashboard,
    students:      loadStudents,
    courses:       loadCourses,
    batches:       loadBatches,
    attendance:    loadAttendance,
    fees:          loadFees,
    notes:         loadNotes,
    reports:       loadReports,
    activity:      loadActivity,
    settings:      loadSettings,
    favorites:     loadFavorites,
    'my-course':   loadMyCourse,
    'my-attendance': loadMyAttendance,
    'my-fees':     loadMyFees,
    'my-notes':    loadMyNotes,
    'my-profile':  loadMyProfile,
  };
  if (loaders[page]) loaders[page]();
}

async function logout() {
  await api('/api/auth/logout', { method:'POST' });
  window.location.href = '/login';
}

// ─── DASHBOARD ────────────────────────────────────────────────────────────────
async function loadDashboard() {
  const { ok, data } = await api('/api/dashboard/');
  if (!ok) { html('pageContent', `<div class="alert alert-error">Failed to load dashboard</div>`); return; }
  if (G.user.role === 'student') renderStudentDashboard(data);
  else renderAdminDashboard(data);
}

function renderAdminDashboard(d) {
  const ov = d.overview;
  html('pageContent', `
    <!-- Quick Actions -->
    <div class="card" style="margin-bottom:16px;">
      <div class="card-header"><h3>Quick Actions</h3></div>
      <div class="quick-actions">
        <button class="quick-btn" onclick="navigate('students');setTimeout(showAddStudentModal,200)">${I.plus} Add Student</button>
        <button class="quick-btn" onclick="navigate('batches');setTimeout(showAddBatchModal,200)">${I.plus} Create Batch</button>
        <button class="quick-btn" onclick="navigate('attendance')">${I.attendance} Mark Attendance</button>
        <button class="quick-btn" onclick="navigate('notes');setTimeout(showUploadNoteModal,200)">${I.plus} Upload Notes</button>
        <button class="quick-btn" onclick="navigate('fees');setTimeout(showRecordPaymentModal,200)">${I.fees} Record Payment</button>
      </div>
    </div>

    <!-- Stats -->
    <div class="stats-row">
      <div class="stat-card">
        <div class="stat-icon-box blue">${I.students}</div>
        <div class="stat-body"><div class="stat-value">${ov.total_students}</div><div class="stat-label">Total Students</div></div>
      </div>
      <div class="stat-card">
        <div class="stat-icon-box green">${I.batches}</div>
        <div class="stat-body"><div class="stat-value">${ov.active_batches}</div><div class="stat-label">Active Batches</div></div>
      </div>
      <div class="stat-card">
        <div class="stat-icon-box amber">${I.attendance}</div>
        <div class="stat-body"><div class="stat-value">${ov.today_present}/${ov.today_total}</div><div class="stat-label">Today's Attendance</div></div>
      </div>
      <div class="stat-card">
        <div class="stat-icon-box red">${I.alert_tri}</div>
        <div class="stat-body"><div class="stat-value">${ov.overdue_fee_students + ov.upcoming_fee_students}</div><div class="stat-label">Fee Attention</div></div>
      </div>
    </div>

    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:16px;">
      <!-- Today's Batches -->
      <div class="card">
        <div class="card-header"><h3>Today's Batches</h3>
          <button class="btn btn-secondary btn-sm" onclick="navigate('batches')">View All</button>
        </div>
        ${d.todays_batches.length === 0 ? emptyState('No active batches') : `
        <div class="table-wrap"><table>
          <thead><tr><th>Batch</th><th>Course</th><th>Timing</th><th>Students</th><th>Att.</th></tr></thead>
          <tbody>
            ${d.todays_batches.map(b => `<tr>
              <td><strong>${b.name}</strong><br><span class="text-muted text-small">${b.code||''}</span></td>
              <td>${b.course_name}</td>
              <td>${b.start_time||'—'} ${b.end_time ? '- '+b.end_time : ''}</td>
              <td>${b.student_count}</td>
              <td>${b.attendance_marked ? badge('Done','success') : badge('Pending','warning')}</td>
            </tr>`).join('')}
          </tbody>
        </table></div>`}
      </div>

      <!-- Fee Attention -->
      <div class="card">
        <div class="card-header"><h3>Fee Attention</h3>
          <button class="btn btn-secondary btn-sm" onclick="navigate('fees')">View All</button>
        </div>
        ${d.fee_attention.length === 0 ? emptyState('No pending fees') : `
        <div class="table-wrap"><table>
          <thead><tr><th>Student</th><th>Remaining</th><th>Due Date</th><th>Status</th></tr></thead>
          <tbody>
            ${d.fee_attention.map(f => `<tr>
              <td><strong>${f.student_name}</strong><br><span class="text-muted text-small">${f.student_id} &bull; ${f.batch||f.course}</span></td>
              <td style="color:var(--danger);font-weight:700;">${fmtMoney(f.remaining)}</td>
              <td>${fmtDate(f.next_due_date)}</td>
              <td>${statusBadge(f.status)}</td>
            </tr>`).join('')}
          </tbody>
        </table></div>`}
      </div>
    </div>

    <!-- Recent Notes -->
    <div class="card">
      <div class="card-header"><h3>Recent Study Materials</h3>
        <button class="btn btn-secondary btn-sm" onclick="navigate('notes')">View All</button>
      </div>
      ${d.recent_notes.length === 0 ? emptyState('No notes uploaded yet') : `
      <div class="table-wrap"><table>
        <thead><tr><th>Title</th><th>Course</th><th>Category</th><th>Uploaded</th><th>Access</th><th></th></tr></thead>
        <tbody>
          ${d.recent_notes.map(n => `<tr>
            <td><strong>${n.title}</strong></td>
            <td>${n.course_name || '—'}</td>
            <td>${badge(n.category||'General','info')}</td>
            <td>${fmtDate(n.uploaded_at)}</td>
            <td>${n.is_downloadable ? badge('View + Download','success') : badge('View Only','warning')}</td>
            <td><button class="btn btn-xs btn-secondary"
              onclick="openNoteViewer(${JSON.stringify(n).replace(/"/g,'&quot;')}, ${JSON.stringify(G.user).replace(/"/g,'&quot;')})"
            >${I.eye} Open</button></td>
          </tr>`).join('')}
        </tbody>
      </table></div>`}
    </div>`);
}

function renderStudentDashboard(d) {
  const s  = d.student;
  const at = d.attendance;
  const fe = d.fees;
  const pct = at.percentage;
  html('pageContent', `
    <!-- Profile banner -->
    <div class="student-profile-header" style="margin-bottom:16px;">
      <img class="student-profile-avatar"
        src="${s.profile_image
          ? `/api/profile-image/${s.profile_image}`
          : `https://ui-avatars.com/api/?name=${encodeURIComponent(s.full_name)}&background=1e3a5f&color=f59e0b&size=80`}"
        onerror="this.src='https://ui-avatars.com/api/?name=${encodeURIComponent(s.full_name)}&background=1e3a5f&color=f59e0b&size=80'"
        alt="Avatar">
      <div class="student-profile-info">
        <h3>Welcome, ${s.first_name}!</h3>
        <p>ID: ${s.student_id} &nbsp;&bull;&nbsp; ${s.course||'No course assigned'} &nbsp;&bull;&nbsp; ${s.batch||'No batch assigned'}</p>
      </div>
    </div>

    <!-- Stats -->
    <div class="stats-row" style="grid-template-columns:repeat(3,1fr);margin-bottom:16px;">
      <div class="stat-card">
        <div class="stat-icon-box green">${I.attendance}</div>
        <div class="stat-body"><div class="stat-value">${pct}%</div><div class="stat-label">Attendance (30 days)</div></div>
      </div>
      <div class="stat-card">
        <div class="stat-icon-box blue">${I.fees}</div>
        <div class="stat-body"><div class="stat-value">${fmtMoney(fe.total_paid)}</div><div class="stat-label">Fees Paid</div></div>
      </div>
      <div class="stat-card">
        <div class="stat-icon-box ${fe.remaining > 0 ? 'red' : 'green'}">${I.fees}</div>
        <div class="stat-body"><div class="stat-value">${fmtMoney(fe.remaining)}</div><div class="stat-label">Remaining Fee</div>
        ${fe.next_due_date ? `<div class="text-small text-muted">Due: ${fmtDate(fe.next_due_date)}</div>` : ''}
        </div>
      </div>
    </div>

    <!-- Attendance bar -->
    <div class="card" style="margin-bottom:16px;">
      <div class="card-header"><h3>Attendance (Last 30 Days)</h3></div>
      <div style="margin-bottom:8px;display:flex;justify-content:space-between;font-size:12px;color:var(--gray-500);">
        <span>${at.present} present of ${at.total_days} days</span><span>${pct}%</span>
      </div>
      <div class="progress-bar-wrap">
        <div class="progress-bar-fill" style="width:${pct}%;background:${pct>=75?'var(--success)':pct>=50?'var(--warning)':'var(--danger)'}"></div>
      </div>
    </div>

    <!-- Recent Notes -->
    <div class="card">
      <div class="card-header"><h3>Recent Study Materials</h3>
        <button class="btn btn-secondary btn-sm" onclick="navigate('my-notes')">View All</button>
      </div>
      ${d.recent_notes.length === 0 ? emptyState('No notes available') : `
      <div class="table-wrap"><table>
        <thead><tr><th>Title</th><th>Category</th><th>Date</th><th>Actions</th></tr></thead>
        <tbody>
          ${d.recent_notes.map(n => `<tr>
            <td><strong>${n.title}</strong></td>
            <td>${badge(n.category||'General','info')}</td>
            <td>${fmtDate(n.uploaded_at)}</td>
            <td style="display:flex;gap:6px;">
              <button class="btn btn-xs btn-secondary"
                onclick="openNoteViewer(${JSON.stringify(n).replace(/&quot;/g,'&amp;quot;').replace(/"/g,'&quot;')}, ${JSON.stringify(G.user).replace(/"/g,'&quot;')})"
              >${I.eye} Open</button>
              ${n.is_downloadable ? `<button class="btn btn-xs btn-primary" onclick="window.open('/api/notes/${n.id}/download','_blank')">${I.download}</button>` : ''}
            </td>
          </tr>`).join('')}
        </tbody>
      </table></div>`}
    </div>`);
}

// ─── COURSES ──────────────────────────────────────────────────────────────────
async function loadCourses() {
  const { ok, data } = await api('/api/courses/');
  if (!ok) { html('pageContent', `<div class="alert alert-error">Failed to load courses</div>`); return; }
  html('pageContent', `
    <div class="page-header">
      <h2>Courses</h2>
      <div class="page-actions">
        <button class="btn btn-primary" onclick="showAddCourseModal()">${I.plus} Add Course</button>
      </div>
    </div>
    <div class="card">
      <div class="table-wrap">
        <table>
          <thead><tr><th>Course</th><th>Code</th><th>Duration</th><th>Default Fee</th><th>Status</th><th>Actions</th></tr></thead>
          <tbody id="coursesBody">
            ${data.courses.length === 0 ? `<tr><td colspan="6">${emptyState('No courses yet')}</td></tr>` :
              data.courses.map(c => `<tr>
                <td><strong>${c.name}</strong>${c.description ? `<br><span class="text-muted text-small">${c.description.substring(0,60)}</span>` : ''}</td>
                <td>${badge(c.code||'—','purple')}</td>
                <td>${c.duration||'—'}</td>
                <td>${fmtMoney(c.default_fee)}</td>
                <td>${statusBadge(c.status)}</td>
                <td style="white-space:nowrap;">
                  <button class="btn btn-xs btn-secondary" onclick="showEditCourseModal(${c.id})">${I.edit}</button>
                  <button class="btn btn-xs btn-danger"  onclick="deleteCourse(${c.id})">${I.trash}</button>
                </td>
              </tr>`).join('')}
          </tbody>
        </table>
      </div>
    </div>`);
}

function showAddCourseModal(prefill={}) {
  showModal(`
    ${modalHeader(prefill.id ? 'Edit Course' : 'Add Course')}
    <div class="modal-body">
      <div class="form-row">
        <div class="form-group"><label>Course Name *</label>
          <input class="form-control" id="cName" value="${prefill.name||''}" placeholder="e.g. Cloud Computing"></div>
        <div class="form-group"><label>Course Code *</label>
          <input class="form-control" id="cCode" value="${prefill.code||''}" placeholder="e.g. CC" style="text-transform:uppercase;"></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>Duration</label>
          <input class="form-control" id="cDur" value="${prefill.duration||''}" placeholder="e.g. 12 Months"></div>
        <div class="form-group"><label>Default Fee (Rs.)</label>
          <input class="form-control" type="number" id="cFee" value="${prefill.default_fee||''}" placeholder="0"></div>
      </div>
      <div class="form-group"><label>Description</label>
        <textarea class="form-control" id="cDesc" rows="2" placeholder="Short description">${prefill.description||''}</textarea></div>
      <div class="form-group"><label>Status</label>
        <select class="form-control" id="cStatus">
          <option value="active" ${prefill.status==='active'||!prefill.status?'selected':''}>Active</option>
          <option value="inactive" ${prefill.status==='inactive'?'selected':''}>Inactive</option>
        </select></div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="saveCourse(${prefill.id||'null'})">${prefill.id?'Update':'Create'} Course</button>
    </div>`, 'modal-md');
}

async function showEditCourseModal(id) {
  const { ok, data } = await api(`/api/courses/${id}`);
  if (ok) showAddCourseModal(data.course);
}

async function saveCourse(id) {
  const payload = {
    name: el('cName').value.trim(), code: el('cCode').value.trim().toUpperCase(),
    duration: el('cDur').value.trim(), default_fee: el('cFee').value||0,
    description: el('cDesc').value.trim(), status: el('cStatus').value
  };
  if (!payload.name || !payload.code) { toast('Name and code are required','warning'); return; }
  const url = id ? `/api/courses/${id}` : '/api/courses/';
  const { ok, data } = await api(url, {
    method: id ? 'PUT' : 'POST',
    headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload)
  });
  if (ok) { closeModal(); toast(data.message); loadCourses(); }
  else toast(data.error||'Failed','danger');
}

async function deleteCourse(id) {
  confirmDialog('Delete or archive this course?', async () => {
    const { ok, data } = await api(`/api/courses/${id}`, { method:'DELETE' });
    if (ok) { toast(data.message); loadCourses(); }
    else toast(data.error||'Failed','danger');
  });
}

// ─── BATCHES ──────────────────────────────────────────────────────────────────
async function loadBatches() {
  const [br, cr] = await Promise.all([api('/api/batches/'), api('/api/courses/')]);
  if (!br.ok) { html('pageContent', `<div class="alert alert-error">Failed to load batches</div>`); return; }
  const courses = cr.data.courses || [];
  html('pageContent', `
    <div class="page-header">
      <h2>Batches</h2>
      <div class="page-actions">
        <button class="btn btn-primary" onclick="showAddBatchModal(null,${JSON.stringify(courses).replace(/"/g,'&quot;')})">${I.plus} Create Batch</button>
      </div>
    </div>
    <div class="card">
      <div class="table-wrap">
        <table>
          <thead><tr><th>Batch</th><th>Code</th><th>Course</th><th>Faculty</th><th>Timing</th><th>Students</th><th>Status</th><th>Actions</th></tr></thead>
          <tbody>
            ${br.data.batches.length === 0 ? `<tr><td colspan="8">${emptyState('No batches yet')}</td></tr>` :
              br.data.batches.map(b => `<tr>
                <td><strong>${b.name}</strong></td>
                <td>${badge(b.code||'—','purple')}</td>
                <td>${b.course_name||'—'}</td>
                <td>${b.faculty||'—'}</td>
                <td>${b.start_time||'—'}${b.end_time?' - '+b.end_time:''}<br><span class="text-muted text-small">${b.schedule||''}</span></td>
                <td><strong>${b.student_count}</strong>${b.max_students?'/'+b.max_students:''}</td>
                <td>${statusBadge(b.status)}</td>
                <td style="white-space:nowrap;">
                  <button class="btn btn-xs btn-secondary" onclick="viewBatch(${b.id})">${I.eye}</button>
                  <button class="btn btn-xs btn-secondary" onclick="editBatch(${b.id})">${I.edit}</button>
                  <button class="btn btn-xs btn-danger"   onclick="deleteBatch(${b.id})">${I.trash}</button>
                </td>
              </tr>`).join('')}
          </tbody>
        </table>
      </div>
    </div>`);
}

async function showAddBatchModal(prefill={}, coursesArg) {
  let courses = coursesArg;
  if (!courses) { const r = await api('/api/courses/'); courses = r.data.courses||[]; }
  if (!prefill) prefill = {};
  showModal(`
    ${modalHeader(prefill.id ? 'Edit Batch' : 'Create Batch')}
    <div class="modal-body">
      <div class="form-row">
        <div class="form-group"><label>Batch Name *</label>
          <input class="form-control" id="bName" value="${prefill.name||''}" placeholder="e.g. Cloud Morning Batch"></div>
        <div class="form-group"><label>Batch Code *</label>
          <input class="form-control" id="bCode" value="${prefill.code||''}" placeholder="e.g. CC-2026-M01" style="text-transform:uppercase;"></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>Course *</label>
          <select class="form-control" id="bCourse">
            <option value="">Select Course</option>
            ${courses.map(c=>`<option value="${c.id}" ${prefill.course_id==c.id?'selected':''}>${c.name}</option>`).join('')}
          </select></div>
        <div class="form-group"><label>Faculty</label>
          <input class="form-control" id="bFaculty" value="${prefill.faculty||''}" placeholder="Faculty name"></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>Start Date</label>
          <input class="form-control" type="date" id="bStart" value="${prefill.start_date||''}"></div>
        <div class="form-group"><label>Expected End Date</label>
          <input class="form-control" type="date" id="bEnd" value="${prefill.end_date||''}"></div>
      </div>
      <div class="form-row-3">
        <div class="form-group"><label>Start Time</label>
          <input class="form-control" type="time" id="bStartT" value="${prefill.start_time||''}"></div>
        <div class="form-group"><label>End Time</label>
          <input class="form-control" type="time" id="bEndT" value="${prefill.end_time||''}"></div>
        <div class="form-group"><label>Max Students</label>
          <input class="form-control" type="number" id="bMax" value="${prefill.max_students||''}" placeholder="Optional"></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>Schedule</label>
          <input class="form-control" id="bSchedule" value="${prefill.schedule||''}" placeholder="e.g. Mon-Fri"></div>
        <div class="form-group"><label>Status</label>
          <select class="form-control" id="bStatus">
            <option value="active" ${!prefill.status||prefill.status==='active'?'selected':''}>Active</option>
            <option value="completed" ${prefill.status==='completed'?'selected':''}>Completed</option>
            <option value="archived" ${prefill.status==='archived'?'selected':''}>Archived</option>
          </select></div>
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="saveBatch(${prefill.id||'null'})">${prefill.id?'Update':'Create'} Batch</button>
    </div>`, 'modal-lg');
}

async function editBatch(id) {
  const { ok, data } = await api(`/api/batches/${id}`);
  if (ok) showAddBatchModal(data.batch);
}

async function saveBatch(id) {
  const payload = {
    name: el('bName').value.trim(), code: el('bCode').value.trim().toUpperCase(),
    course_id: el('bCourse').value||null, faculty: el('bFaculty').value.trim(),
    start_date: el('bStart').value||null, end_date: el('bEnd').value||null,
    start_time: el('bStartT').value||null, end_time: el('bEndT').value||null,
    max_students: el('bMax').value||null, schedule: el('bSchedule').value.trim(),
    status: el('bStatus').value
  };
  if (!payload.name || !payload.code) { toast('Name and code required','warning'); return; }
  const url = id ? `/api/batches/${id}` : '/api/batches/';
  const { ok, data } = await api(url, {
    method: id ? 'PUT' : 'POST',
    headers: {'Content-Type':'application/json'}, body: JSON.stringify(payload)
  });
  if (ok) { closeModal(); toast(data.message); loadBatches(); }
  else toast(data.error||'Failed','danger');
}

async function deleteBatch(id) {
  confirmDialog('Delete or archive this batch?', async () => {
    const { ok, data } = await api(`/api/batches/${id}`, { method:'DELETE' });
    if (ok) { toast(data.message); loadBatches(); }
    else toast(data.error||'Failed','danger');
  });
}

async function viewBatch(id) {
  const { ok, data } = await api(`/api/batches/${id}`);
  if (!ok) { toast('Failed to load batch','danger'); return; }
  const b = data.batch;
  showModal(`
    ${modalHeader(`Batch: ${b.name}`)}
    <div class="modal-body">
      <div class="detail-grid" style="margin-bottom:16px;">
        <div class="detail-item"><div class="label">Code</div><div class="value">${badge(b.code||'—','purple')}</div></div>
        <div class="detail-item"><div class="label">Course</div><div class="value">${b.course_name||'—'}</div></div>
        <div class="detail-item"><div class="label">Faculty</div><div class="value">${b.faculty||'—'}</div></div>
        <div class="detail-item"><div class="label">Timing</div><div class="value">${b.start_time||'—'} ${b.end_time?'- '+b.end_time:''}</div></div>
        <div class="detail-item"><div class="label">Schedule</div><div class="value">${b.schedule||'—'}</div></div>
        <div class="detail-item"><div class="label">Status</div><div class="value">${statusBadge(b.status)}</div></div>
        <div class="detail-item"><div class="label">Start Date</div><div class="value">${fmtDate(b.start_date)}</div></div>
        <div class="detail-item"><div class="label">End Date</div><div class="value">${fmtDate(b.end_date)}</div></div>
      </div>
      <div class="form-section-title">Students (${b.students.length})</div>
      ${b.students.length === 0 ? emptyState('No students in this batch') : `
      <div class="table-wrap"><table>
        <thead><tr><th>ID</th><th>Name</th><th>Status</th></tr></thead>
        <tbody>${b.students.map(s=>`<tr>
          <td>${s.student_id}</td>
          <td>${s.first_name} ${s.last_name}</td>
          <td>${statusBadge(s.status)}</td>
        </tr>`).join('')}</tbody>
      </table></div>`}
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="closeModal()">Close</button>
      <button class="btn btn-primary" onclick="closeModal();navigate('attendance')">Mark Attendance</button>
    </div>`, 'modal-lg');
}

// ─── STUDENTS ─────────────────────────────────────────────────────────────────
async function loadStudents() {
  const { ok, data } = await api('/api/students/');
  if (!ok) { html('pageContent', `<div class="alert alert-error">Failed to load students</div>`); return; }
  html('pageContent', `
    <div class="page-header">
      <h2>Students</h2>
      <div class="page-actions">
        <button class="btn btn-primary" onclick="showAddStudentModal()">${I.plus} Add Student</button>
      </div>
    </div>
    <div class="card">
      <div class="search-bar" style="margin-bottom:12px;">
        <input class="form-control" id="studentSearch" placeholder="Search by name, ID or email…" oninput="searchStudents(this.value)" style="max-width:300px;">
      </div>
      <div class="table-wrap" id="studentsTableWrap">
        ${renderStudentsTable(data.students)}
      </div>
    </div>`);
}

function renderStudentsTable(students) {
  if (!students.length) return emptyState('No students found');
  return `<table>
    <thead><tr><th>ID</th><th>Name</th><th>Course</th><th>Batch</th><th>Phone</th><th>Status</th><th>Actions</th></tr></thead>
    <tbody>
      ${students.map(s=>`<tr>
        <td>${badge(s.student_id,'purple')}</td>
        <td><strong>${s.first_name} ${s.last_name}</strong><br><span class="text-muted text-small">${s.email||''}</span></td>
        <td>${s.course||'—'}</td>
        <td>${s.batch||'—'}</td>
        <td>${s.phone||'—'}</td>
        <td>${statusBadge(s.status||'active')}</td>
        <td style="white-space:nowrap;">
          <button class="btn btn-xs btn-secondary" onclick="viewStudentProfile(${s.id})">${I.eye}</button>
          <button class="btn btn-xs btn-secondary" onclick="showEditStudentModal(${s.id})">${I.edit}</button>
          <button class="btn btn-xs btn-danger"   onclick="deleteStudent(${s.id})">${I.trash}</button>
        </td>
      </tr>`).join('')}
    </tbody>
  </table>`;
}

let searchTimer;
async function searchStudents(q) {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(async () => {
    const { data } = await api(`/api/students/?query=${encodeURIComponent(q)}`);
    html('studentsTableWrap', renderStudentsTable(data.students||[]));
  }, 300);
}

async function showAddStudentModal() {
  const [cr, br] = await Promise.all([api('/api/courses/'), api('/api/batches/')]);
  const courses = cr.data.courses||[];
  const batches = br.data.batches||[];
  showModal(`
    ${modalHeader('Add New Student')}
    <div class="modal-body">
      <div class="form-section-title">Student Information</div>
      <div class="form-row">
        <div class="form-group"><label>Student ID *</label>
          <input class="form-control" id="sID" placeholder="e.g. OXF-001"></div>
        <div class="form-group"><label>Email *</label>
          <input class="form-control" type="email" id="sEmail" placeholder="student@email.com"></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>First Name *</label>
          <input class="form-control" id="sFirst"></div>
        <div class="form-group"><label>Last Name *</label>
          <input class="form-control" id="sLast"></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>Phone</label>
          <input class="form-control" id="sPhone" placeholder="9876543210"></div>
        <div class="form-group"><label>Date of Birth</label>
          <input class="form-control" type="date" id="sDOB"></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>Gender</label>
          <select class="form-control" id="sGender">
            <option value="">Select</option>
            <option>Male</option><option>Female</option><option>Other</option>
          </select></div>
        <div class="form-group"><label>Joining Date</label>
          <input class="form-control" type="date" id="sJoin" value="${new Date().toISOString().split('T')[0]}"></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>Course</label>
          <select class="form-control" id="sCourse" onchange="filterBatchesByCourse(this.value)">
            <option value="">Select Course</option>
            ${courses.map(c=>`<option value="${c.id}">${c.name}</option>`).join('')}
          </select></div>
        <div class="form-group"><label>Batch</label>
          <select class="form-control" id="sBatch">
            <option value="">Select Batch</option>
            ${batches.map(b=>`<option value="${b.id}">${b.name}</option>`).join('')}
          </select></div>
      </div>
      <div class="form-group"><label>Address</label>
        <textarea class="form-control" id="sAddr" rows="2"></textarea></div>
      <div class="form-row">
        <div class="form-group"><label>Guardian Name</label>
          <input class="form-control" id="sGuard"></div>
        <div class="form-group"><label>Guardian Phone</label>
          <input class="form-control" id="sGuardPh"></div>
      </div>
      <div class="form-section-title" style="margin-top:8px;">Fee Setup</div>
      <div class="form-row">
        <div class="form-group"><label>Total Course Fee (Rs.)</label>
          <input class="form-control" type="number" id="sTotalFee" placeholder="Leave blank to use course default"></div>
        <div class="form-group"><label>Installment Amount (Rs.)</label>
          <input class="form-control" type="number" id="sInstAmt" placeholder="Optional"></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>Installment Frequency</label>
          <select class="form-control" id="sInstFreq">
            <option value="">None</option>
            <option value="monthly">Monthly</option>
            <option value="quarterly">Quarterly</option>
            <option value="custom">Custom</option>
          </select></div>
        <div class="form-group"><label>First Due Date</label>
          <input class="form-control" type="date" id="sDueDate"></div>
      </div>
      <div class="form-section-title" style="margin-top:8px;">Login Credentials</div>
      <div class="form-hint" style="margin-bottom:10px;">Student will login using their Student ID and this password.</div>
      <div class="form-group"><label>Password *</label>
        <input class="form-control" type="password" id="sPass" placeholder="Minimum 6 characters"></div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="saveStudent(null)">Create Student Account</button>
    </div>`, 'modal-xl');

  // Store batches for filtering
  window._allBatches = batches;
}

function filterBatchesByCourse(courseId) {
  const sel = el('sBatch');
  const filtered = courseId
    ? (window._allBatches||[]).filter(b => String(b.course_id) === String(courseId))
    : (window._allBatches||[]);
  sel.innerHTML = `<option value="">Select Batch</option>` +
    filtered.map(b=>`<option value="${b.id}">${b.name}</option>`).join('');
}

async function saveStudent(id) {
  const payload = {
    student_id: (el('sID')||{}).value?.trim(),
    first_name: el('sFirst').value.trim(), last_name: el('sLast').value.trim(),
    email: el('sEmail').value.trim(), phone: el('sPhone').value.trim(),
    date_of_birth: el('sDOB').value||null, gender: el('sGender').value,
    joining_date: el('sJoin').value||null, address: el('sAddr').value.trim(),
    course_id: el('sCourse').value||null, batch_id: el('sBatch').value||null,
    guardian_name: el('sGuard').value.trim(), guardian_phone: el('sGuardPh').value.trim(),
    total_fee: el('sTotalFee').value||null,
    installment_amount: el('sInstAmt').value||null,
    installment_freq: el('sInstFreq').value||null,
    next_due_date: el('sDueDate').value||null,
    password: (el('sPass')||{}).value,
    status: 'active'
  };
  if (!payload.first_name||!payload.last_name||!payload.email) { toast('Name and email required','warning'); return; }
  if (!id && (!payload.student_id || !payload.password)) { toast('Student ID and password required','warning'); return; }
  const url = id ? `/api/students/${id}` : '/api/students/';
  const { ok, data } = await api(url, {
    method: id ? 'PUT' : 'POST',
    headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)
  });
  if (ok) {
    closeModal();
    if (!id) {
      // After creation, remember the new student's DB id for photo upload
      const newStudentId = data.student?.id;
      showModal(`
        ${modalHeader('Student Created')}
        <div class="modal-body">
          <div class="alert alert-success">Student account created successfully!</div>
          <div class="card" style="background:var(--gray-50);margin-bottom:16px;">
            <div class="detail-item"><div class="label">Student Name</div><div class="value">${payload.first_name} ${payload.last_name}</div></div>
            <div class="detail-item" style="margin-top:10px;"><div class="label">Login — Username (Student ID)</div>
              <div class="value"><strong>${payload.student_id}</strong></div></div>
            <div class="detail-item" style="margin-top:10px;"><div class="label">Login — Password</div>
              <div class="value"><strong>${payload.password}</strong></div></div>
          </div>
          ${newStudentId ? `
          <div class="form-section-title">Add Profile Photo (optional)</div>
          <div style="display:flex;align-items:center;gap:16px;margin-top:8px;">
            <img id="newPhotoPreview"
              src="https://ui-avatars.com/api/?name=${encodeURIComponent(payload.first_name+' '+payload.last_name)}&background=1e3a5f&color=f59e0b&size=64"
              style="width:64px;height:64px;border-radius:50%;object-fit:cover;border:2px solid var(--gray-200);flex-shrink:0;">
            <div style="flex:1;">
              <input class="form-control" type="file" id="newSPhoto" accept=".jpg,.jpeg,.png"
                onchange="(function(i){if(!i.files[0])return;const r=new FileReader();r.onload=e=>document.getElementById('newPhotoPreview').src=e.target.result;r.readAsDataURL(i.files[0]);})(this)">
              <div class="form-hint">JPG or PNG — optional</div>
            </div>
          </div>` : ''}
          <p class="form-hint" style="margin-top:12px;">Share credentials with the student.</p>
        </div>
        <div class="modal-footer">
          ${newStudentId ? `<button class="btn btn-secondary" onclick="uploadNewStudentPhoto(${newStudentId})">Upload Photo &amp; Done</button>` : ''}
          <button class="btn btn-primary" onclick="closeModal();loadStudents()">Done</button>
        </div>`, 'modal-sm');
    } else { toast('Student updated'); loadStudents(); }
  } else toast(data.error||'Failed','danger');
}

async function showEditStudentModal(id) {
  const [sr, cr, br] = await Promise.all([api(`/api/students/${id}`), api('/api/courses/'), api('/api/batches/')]);
  if (!sr.ok) { toast('Failed to load student','danger'); return; }
  const s = sr.data.student;
  const courses = cr.data.courses||[];
  const batches = br.data.batches||[];
  window._allBatches = batches;
  showModal(`
    ${modalHeader('Edit Student')}
    <div class="modal-body">
      <div class="form-section-title">Student Information</div>
      <div class="form-group"><label>Student ID</label>
        <input class="form-control" value="${s.student_id}" disabled></div>
      <div class="form-row">
        <div class="form-group"><label>First Name *</label>
          <input class="form-control" id="sFirst" value="${s.first_name}"></div>
        <div class="form-group"><label>Last Name *</label>
          <input class="form-control" id="sLast" value="${s.last_name}"></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>Email *</label>
          <input class="form-control" type="email" id="sEmail" value="${s.email||''}"></div>
        <div class="form-group"><label>Phone</label>
          <input class="form-control" id="sPhone" value="${s.phone||''}"></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>Date of Birth</label>
          <input class="form-control" type="date" id="sDOB" value="${s.date_of_birth||''}"></div>
        <div class="form-group"><label>Gender</label>
          <select class="form-control" id="sGender">
            <option value="">Select</option>
            ${['Male','Female','Other'].map(g=>`<option ${s.gender===g?'selected':''}>${g}</option>`).join('')}
          </select></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>Course</label>
          <select class="form-control" id="sCourse" onchange="filterBatchesByCourse(this.value)">
            <option value="">Select</option>
            ${courses.map(c=>`<option value="${c.id}" ${s.course_id==c.id?'selected':''}>${c.name}</option>`).join('')}
          </select></div>
        <div class="form-group"><label>Batch</label>
          <select class="form-control" id="sBatch">
            <option value="">Select</option>
            ${batches.map(b=>`<option value="${b.id}" ${s.batch_id==b.id?'selected':''}>${b.name}</option>`).join('')}
          </select></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>Joining Date</label>
          <input class="form-control" type="date" id="sJoin" value="${s.joining_date||''}"></div>
        <div class="form-group"><label>Status</label>
          <select class="form-control" id="sStatusEdit">
            ${['active','completed','on_hold','dropped'].map(st=>`<option value="${st}" ${(s.status||'active')===st?'selected':''}>${st.replace('_',' ')}</option>`).join('')}
          </select></div>
      </div>
      <div class="form-group"><label>Address</label>
        <textarea class="form-control" id="sAddr" rows="2">${s.address||''}</textarea></div>
      <div class="form-row">
        <div class="form-group"><label>Guardian Name</label>
          <input class="form-control" id="sGuard" value="${s.guardian_name||''}"></div>
        <div class="form-group"><label>Guardian Phone</label>
          <input class="form-control" id="sGuardPh" value="${s.guardian_phone||''}"></div>
      </div>
      <div class="form-section-title" style="margin-top:8px;">Profile Photo</div>
      <div style="display:flex;align-items:center;gap:16px;margin-bottom:4px;">
        <img id="editPhotoPreview"
          src="${s.profile_image ? `/api/profile-image/${s.profile_image}` : `https://ui-avatars.com/api/?name=${encodeURIComponent(s.first_name+' '+s.last_name)}&background=1e3a5f&color=f59e0b&size=80`}"
          style="width:72px;height:72px;border-radius:50%;object-fit:cover;border:2px solid var(--gray-200);flex-shrink:0;">
        <div>
          <input class="form-control" type="file" id="sPhoto" accept=".jpg,.jpeg,.png"
            onchange="previewStudentPhoto(this)">
          <div class="form-hint">JPG or PNG — max 5 MB. Leave blank to keep existing photo.</div>
        </div>
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="saveStudentEdit(${id})">Update Student</button>
    </div>`, 'modal-xl');
}

function previewStudentPhoto(input) {
  if (!input.files || !input.files[0]) return;
  const reader = new FileReader();
  reader.onload = e => {
    const img = document.getElementById('editPhotoPreview');
    if (img) img.src = e.target.result;
  };
  reader.readAsDataURL(input.files[0]);
}

async function uploadNewStudentPhoto(studentId) {
  const photoInput = el('newSPhoto');
  if (photoInput && photoInput.files && photoInput.files[0]) {
    const fd = new FormData();
    fd.append('file', photoInput.files[0]);
    const { ok, data } = await api(`/api/students/${studentId}/profile-image`, {
      method: 'POST', body: fd
    });
    if (!ok) { toast('Photo upload failed: ' + (data.error||''), 'warning'); }
    else { toast('Photo uploaded!'); }
  }
  closeModal();
  loadStudents();
}

async function saveStudentEdit(id) {
  const payload = {
    first_name: el('sFirst').value.trim(), last_name: el('sLast').value.trim(),
    email: el('sEmail').value.trim(), phone: el('sPhone').value.trim(),
    date_of_birth: el('sDOB').value||null, gender: el('sGender').value,
    joining_date: el('sJoin').value||null, address: el('sAddr').value.trim(),
    course_id: el('sCourse').value||null, batch_id: el('sBatch').value||null,
    guardian_name: el('sGuard').value.trim(), guardian_phone: el('sGuardPh').value.trim(),
    status: el('sStatusEdit').value, is_active: el('sStatusEdit').value !== 'dropped'
  };
  const { ok, data } = await api(`/api/students/${id}`, {
    method:'PUT', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)
  });
  if (!ok) { toast(data.error||'Failed','danger'); return; }

  // Upload photo if one was chosen
  const photoInput = el('sPhoto');
  if (photoInput && photoInput.files && photoInput.files[0]) {
    const fd = new FormData();
    fd.append('file', photoInput.files[0]);
    const { ok: pOk, data: pData } = await api(`/api/students/${id}/profile-image`, {
      method: 'POST', body: fd
    });
    if (!pOk) { toast('Info updated but photo upload failed: ' + (pData.error||''), 'warning'); loadStudents(); return; }
  }

  closeModal();
  toast('Student updated');
  loadStudents();
}

async function viewStudentProfile(id) {
  const [sr, fr] = await Promise.all([api(`/api/students/${id}`), api(`/api/fees/student/${id}/summary`)]);
  if (!sr.ok) { toast('Failed to load','danger'); return; }
  const s  = sr.data.student;
  const fe = fr.ok ? fr.data : { total_fee:0, total_paid:0, remaining:0, payments:[] };
  const pct= fe.total_fee > 0 ? Math.min(100, Math.round(fe.total_paid/fe.total_fee*100)) : 0;

  // Use actual photo if available, else fallback to initials avatar
  const photoSrc = s.profile_image
    ? `/api/profile-image/${s.profile_image}`
    : `https://ui-avatars.com/api/?name=${encodeURIComponent(s.full_name)}&background=1e3a5f&color=f59e0b&size=80`;
  showModal(`
    ${modalHeader('Student Profile')}
    <div class="modal-body">
      <div class="student-profile-header" style="margin-bottom:16px;">
        <img class="student-profile-avatar" src="${photoSrc}"
          onerror="this.src='https://ui-avatars.com/api/?name=${encodeURIComponent(s.full_name)}&background=1e3a5f&color=f59e0b&size=80'"
          alt="${s.full_name}">
        <div class="student-profile-info">
          <h3>${s.full_name}</h3>
          <p>${badge(s.student_id,'purple')} &nbsp; ${statusBadge(s.status||'active')}</p>
        </div>
      </div>
      <div class="tabs">
        <button class="tab-btn active" onclick="switchProfileTab(this,'spInfo')">Info</button>
        <button class="tab-btn" onclick="switchProfileTab(this,'spFees')">Fees</button>
      </div>
      <div id="spInfo">
        <div class="detail-grid">
          <div class="detail-item"><div class="label">Email</div><div class="value">${s.email||'—'}</div></div>
          <div class="detail-item"><div class="label">Phone</div><div class="value">${s.phone||'—'}</div></div>
          <div class="detail-item"><div class="label">Course</div><div class="value">${s.course||'—'}</div></div>
          <div class="detail-item"><div class="label">Batch</div><div class="value">${s.batch||'—'}</div></div>
          <div class="detail-item"><div class="label">Joining Date</div><div class="value">${fmtDate(s.joining_date)}</div></div>
          <div class="detail-item"><div class="label">Gender</div><div class="value">${s.gender||'—'}</div></div>
          <div class="detail-item"><div class="label">Guardian</div><div class="value">${s.guardian_name||'—'}</div></div>
          <div class="detail-item"><div class="label">Guardian Phone</div><div class="value">${s.guardian_phone||'—'}</div></div>
        </div>
        ${s.address ? `<div class="detail-item" style="margin-top:12px;"><div class="label">Address</div><div class="value">${s.address}</div></div>` : ''}
      </div>
      <div id="spFees" style="display:none;">
        <div class="fee-summary-bar">
          <div class="fee-bar-item"><div class="fb-label">Total Fee</div><div class="fb-value">${fmtMoney(fe.total_fee)}</div></div>
          <div class="fee-bar-item paid"><div class="fb-label">Paid</div><div class="fb-value">${fmtMoney(fe.total_paid)}</div></div>
          <div class="fee-bar-item due"><div class="fb-label">Remaining</div><div class="fb-value">${fmtMoney(fe.remaining)}</div></div>
        </div>
        <div style="margin-bottom:16px;">
          <div class="progress-bar-wrap"><div class="progress-bar-fill" style="width:${pct}%"></div></div>
          <div class="text-small text-muted" style="margin-top:4px;">${pct}% paid</div>
        </div>
        ${fe.payments.length === 0 ? emptyState('No payments recorded') : `
        <div class="table-wrap"><table>
          <thead><tr><th>Receipt</th><th>Amount</th><th>Date</th><th>Mode</th><th></th></tr></thead>
          <tbody>${fe.payments.map(p=>`<tr>
            <td>${p.receipt_number}</td>
            <td style="color:var(--success);font-weight:600;">${fmtMoney(p.amount)}</td>
            <td>${fmtDate(p.payment_date)}</td>
            <td>${badge(p.payment_mode||'—','info')}</td>
            <td><button class="btn btn-xs btn-secondary" onclick="window.open('/api/fees/payments/${p.id}/receipt','_blank')">${I.receipt}</button></td>
          </tr>`).join('')}</tbody>
        </table></div>`}
      </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="closeModal()">Close</button>
      <button class="btn btn-primary" onclick="closeModal();showEditStudentModal(${id})">${I.edit} Edit</button>
    </div>`, 'modal-lg');
}

function switchProfileTab(btn, tabId) {
  btn.closest('.tabs').querySelectorAll('.tab-btn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById('spInfo').style.display = 'none';
  document.getElementById('spFees').style.display = 'none';
  document.getElementById(tabId).style.display = 'block';
}

async function deleteStudent(id) {
  confirmDialog('Permanently delete this student and their account?', async () => {
    const { ok, data } = await api(`/api/students/${id}`, { method:'DELETE' });
    if (ok) { toast('Student deleted'); loadStudents(); }
    else toast(data.error||'Failed','danger');
  });
}

// ─── ATTENDANCE ───────────────────────────────────────────────────────────────
async function loadAttendance() {
  const { data: bd } = await api('/api/batches/?status=active');
  const batches = bd.batches||[];
  html('pageContent', `
    <div class="page-header"><h2>Attendance</h2></div>
    <div class="card" style="margin-bottom:16px;">
      <div class="search-bar">
        <select class="form-control" id="attBatch" style="max-width:280px;">
          <option value="">Select Batch</option>
          ${batches.map(b=>`<option value="${b.id}">${b.name} (${b.course_name||'—'})</option>`).join('')}
        </select>
        <input class="form-control" type="date" id="attDate" value="${new Date().toISOString().split('T')[0]}" style="max-width:180px;">
        <button class="btn btn-primary" onclick="loadAttendanceGrid()">Load</button>
      </div>
    </div>
    <div id="attGrid"></div>`);
}

async function loadAttendanceGrid() {
  const batchId = el('attBatch').value;
  const date    = el('attDate').value;
  if (!batchId) { toast('Please select a batch','warning'); return; }
  html('attGrid', spinner());
  const { ok, data } = await api(`/api/attendance/batch/${batchId}/date/${date}`);
  if (!ok) { html('attGrid', `<div class="alert alert-error">Failed to load</div>`); return; }
  const students = data.students||[];
  if (!students.length) { html('attGrid', `<div class="card">${emptyState('No students in this batch')}</div>`); return; }
  html('attGrid', `
    <div class="card">
      <div class="card-header">
        <h3>${data.batch.name} — ${fmtDate(date)}</h3>
        <button class="btn btn-primary" onclick="saveAttendance(${batchId},'${date}')">${I.attendance} Save Attendance</button>
      </div>
      <div class="table-wrap">
        <table><thead><tr><th>Student ID</th><th>Name</th><th>Status</th><th>Remarks</th></tr></thead>
        <tbody>
          ${students.map((s,i) => {
            const st = s.status||'present';
            return `<tr>
              <td>${s.student_number}</td>
              <td><strong>${s.student_name}</strong></td>
              <td>
                <select class="att-select ${st}" id="att_${s.student_id}"
                  data-sid="${s.student_id}" onchange="this.className='att-select '+this.value">
                  <option value="present" ${st==='present'?'selected':''}>Present</option>
                  <option value="absent"  ${st==='absent' ?'selected':''}>Absent</option>
                  <option value="late"    ${st==='late'   ?'selected':''}>Late</option>
                  <option value="excused" ${st==='excused'?'selected':''}>Excused</option>
                </select>
              </td>
              <td><input class="form-control" id="rem_${s.student_id}" placeholder="Optional" value="${s.remarks||''}" style="max-width:200px;"></td>
            </tr>`;
          }).join('')}
        </tbody>
        </table>
      </div>
    </div>`);
}

async function saveAttendance(batchId, date) {
  const records = [];
  document.querySelectorAll('.att-select').forEach(sel => {
    records.push({
      student_id: parseInt(sel.dataset.sid),
      status:     sel.value,
      remarks:    (el(`rem_${sel.dataset.sid}`)||{}).value||''
    });
  });
  const { ok, data } = await api('/api/attendance/mark', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ batch_id: batchId, date, records })
  });
  if (ok) toast(data.message);
  else toast(data.error||'Failed','danger');
}

// ─── FEES ─────────────────────────────────────────────────────────────────────
async function loadFees() {
  const { ok, data } = await api('/api/fees/payments');
  if (!ok) { html('pageContent', `<div class="alert alert-error">Failed</div>`); return; }
  html('pageContent', `
    <div class="page-header"><h2>Fee Management</h2>
      <div class="page-actions">
        <button class="btn btn-primary" onclick="showRecordPaymentModal()">${I.plus} Record Payment</button>
      </div>
    </div>
    <div class="card">
      <div class="table-wrap">
        <table>
          <thead><tr><th>Receipt</th><th>Student</th><th>Amount</th><th>Date</th><th>Mode</th><th>Actions</th></tr></thead>
          <tbody>
            ${!data.payments.length ? `<tr><td colspan="6">${emptyState('No payments recorded')}</td></tr>` :
              data.payments.map(p=>`<tr>
                <td>${badge(p.receipt_number,'purple')}</td>
                <td><strong>${p.student_name}</strong><br><span class="text-muted text-small">${p.student_number}</span></td>
                <td style="font-weight:700;color:var(--success);">${fmtMoney(p.amount)}</td>
                <td>${fmtDate(p.payment_date)}</td>
                <td>${badge(p.payment_mode||'—','info')}</td>
                <td style="white-space:nowrap;">
                  <button class="btn btn-xs btn-secondary" onclick="window.open('/api/fees/payments/${p.id}/receipt','_blank')">${I.receipt} Receipt</button>
                  <button class="btn btn-xs btn-danger" onclick="deletePayment(${p.id})">${I.trash}</button>
                </td>
              </tr>`).join('')}
          </tbody>
        </table>
      </div>
    </div>`);
}

async function showRecordPaymentModal() {
  const { data } = await api('/api/students/');
  const students = (data.students||[]).filter(s=>s.is_active);
  showModal(`
    ${modalHeader('Record Fee Payment')}
    <div class="modal-body">
      <div class="form-group"><label>Student *</label>
        <select class="form-control" id="fpStudent" onchange="loadStudentFeeInfo(this.value)">
          <option value="">Select Student</option>
          ${students.map(s=>`<option value="${s.id}">${s.first_name} ${s.last_name} — ${s.student_id}</option>`).join('')}
        </select></div>
      <div id="feeInfoBox"></div>
      <div class="form-row">
        <div class="form-group"><label>Amount (Rs.) *</label>
          <input class="form-control" type="number" id="fpAmount" min="1" placeholder="Enter amount"></div>
        <div class="form-group"><label>Payment Date *</label>
          <input class="form-control" type="date" id="fpDate" value="${new Date().toISOString().split('T')[0]}"></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>Payment Mode *</label>
          <select class="form-control" id="fpMode">
            <option value="cash">Cash</option>
            <option value="upi">UPI</option>
            <option value="bank_transfer">Bank Transfer</option>
            <option value="cheque">Cheque</option>
            <option value="other">Other</option>
          </select></div>
        <div class="form-group"><label>Transaction / Ref ID</label>
          <input class="form-control" id="fpRef" placeholder="Optional"></div>
      </div>
      <div class="form-group"><label>Remarks</label>
        <textarea class="form-control" id="fpRemarks" rows="2"></textarea></div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="submitPayment()">Record Payment</button>
    </div>`, 'modal-md');
}

async function loadStudentFeeInfo(studentId) {
  if (!studentId) { html('feeInfoBox',''); return; }
  const { ok, data } = await api(`/api/fees/student/${studentId}/summary`);
  if (!ok) { html('feeInfoBox',''); return; }
  html('feeInfoBox', `
    <div class="fee-summary-bar" style="margin-bottom:12px;">
      <div class="fee-bar-item"><div class="fb-label">Total Fee</div><div class="fb-value" style="font-size:14px;">${fmtMoney(data.total_fee)}</div></div>
      <div class="fee-bar-item paid"><div class="fb-label">Paid</div><div class="fb-value" style="font-size:14px;">${fmtMoney(data.total_paid)}</div></div>
      <div class="fee-bar-item due"><div class="fb-label">Remaining</div><div class="fb-value" style="font-size:14px;">${fmtMoney(data.remaining)}</div></div>
    </div>`);
  // Pre-fill installment amount if set
  if (data.fee_account?.installment_amount) {
    el('fpAmount').value = data.fee_account.installment_amount;
  }
}

async function submitPayment() {
  const payload = {
    student_id:    el('fpStudent').value,
    amount:        el('fpAmount').value,
    payment_date:  el('fpDate').value,
    payment_mode:  el('fpMode').value,
    transaction_id: el('fpRef').value.trim(),
    remarks:       el('fpRemarks').value.trim()
  };
  if (!payload.student_id || !payload.amount || !payload.payment_mode) {
    toast('Fill all required fields','warning'); return;
  }
  const { ok, data } = await api('/api/fees/payments', {
    method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)
  });
  if (ok) { closeModal(); toast(`Payment recorded! Receipt: ${data.payment.receipt_number}`); loadFees(); }
  else toast(data.error||'Failed','danger');
}

async function deletePayment(id) {
  confirmDialog('Delete this payment record? This cannot be undone.', async () => {
    const { ok, data } = await api(`/api/fees/payments/${id}`, { method:'DELETE' });
    if (ok) { toast('Payment deleted'); loadFees(); }
    else toast(data.error||'Failed','danger');
  });
}

// ─── NOTES ────────────────────────────────────────────────────────────────────
async function loadNotes(query='') {
  const { ok, data } = await api(`/api/notes/?query=${encodeURIComponent(query)}`);
  if (!ok) { html('pageContent', `<div class="alert alert-error">Failed</div>`); return; }
  const isAdmin = G.user.role !== 'student';
  html('pageContent', `
    <div class="page-header"><h2>Study Notes</h2>
      ${isAdmin ? `<div class="page-actions"><button class="btn btn-primary" onclick="showUploadNoteModal()">${I.plus} Upload Note</button></div>` : ''}
    </div>
    <div class="card">
      <div class="search-bar">
        <input class="form-control" id="noteSearch" placeholder="Search notes…"
          oninput="loadNotes(this.value)" value="${query}" style="max-width:300px;">
      </div>
      <div class="table-wrap">
        <table>
          <thead><tr>
            <th>Title</th><th>Course</th><th>Category</th><th>Type</th>
            <th>Uploaded</th><th>Views</th><th>Access</th><th>Actions</th>
          </tr></thead>
          <tbody>
            ${!data.notes.length ? `<tr><td colspan="8">${emptyState('No notes uploaded yet')}</td></tr>` :
              data.notes.map(n => renderNoteRow(n, isAdmin)).join('')}
          </tbody>
        </table>
      </div>
    </div>`);
}

function renderNoteRow(n, isAdmin) {
  // Cache note data so the viewer can retrieve it without inline JSON
  window._noteCache[n.id] = n;

  const accessBadge = n.is_downloadable
    ? badge('View + Download', 'success')
    : badge('View Only', 'warning');

  const viewBtn = `<button class="btn btn-xs btn-secondary"
    onclick="cacheAndOpenNote(${n.id})"
    title="Open note in viewer">${I.eye} Open</button>`;

  // Download button ONLY rendered when download is permitted
  // Never shown for view-only to students
  const dlBtn = (isAdmin || n.is_downloadable)
    ? `<button class="btn btn-xs btn-primary"
         onclick="window.open('/api/notes/${n.id}/download','_blank')"
         title="Download file">${I.download}</button>`
    : '';

  const adminBtns = isAdmin ? `
    <button class="btn btn-xs btn-secondary" onclick="showEditNoteModal(${n.id})">${I.edit}</button>
    <button class="btn btn-xs btn-danger"   onclick="deleteNote(${n.id})">${I.trash}</button>` : '';

  return `<tr>
    <td>
      <strong>${n.title}</strong>
      ${n.description ? `<br><span class="text-muted text-small">${n.description.substring(0,55)}&hellip;</span>` : ''}
    </td>
    <td>${n.course_name || badge('All', 'gray')}</td>
    <td>${badge(n.category || 'General', 'info')}</td>
    <td>${(n.file_type || '?').toUpperCase()}</td>
    <td>${fmtDate(n.uploaded_at)}</td>
    <td>${n.views}</td>
    <td>${accessBadge}</td>
    <td style="white-space:nowrap;display:flex;gap:4px;flex-wrap:wrap;">
      ${viewBtn}${dlBtn}${adminBtns}
    </td>
  </tr>`;
}

async function showUploadNoteModal() {
  const { data: cd } = await api('/api/courses/');
  const courses = cd.courses||[];
  showModal(`
    ${modalHeader('Upload Study Note')}
    <div class="modal-body">
      <div class="form-group"><label>Title *</label>
        <input class="form-control" id="nTitle" placeholder="Note title"></div>
      <div class="form-group"><label>Description</label>
        <textarea class="form-control" id="nDesc" rows="2" placeholder="Optional description"></textarea></div>
      <div class="form-row">
        <div class="form-group"><label>Course (leave blank for all)</label>
          <select class="form-control" id="nCourse">
            <option value="">All Courses</option>
            ${courses.map(c=>`<option value="${c.id}">${c.name}</option>`).join('')}
          </select></div>
        <div class="form-group"><label>Category</label>
          <select class="form-control" id="nCat">
            ${['General','Lecture Notes','Assignments','Study Material','Reference','Lab Work'].map(c=>`<option>${c}</option>`).join('')}
          </select></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>Visibility</label>
          <select class="form-control" id="nVis">
            <option value="all">All Users</option>
            <option value="students">Students Only</option>
            <option value="admin">Admin Only</option>
          </select></div>
        <div class="form-group">
          <label style="margin-bottom:20px;">&nbsp;</label>
          <label style="display:flex;align-items:center;gap:8px;cursor:pointer;">
            <input type="checkbox" id="nDL"> Allow students to download
          </label>
          <div class="form-hint">Default is <strong>View Only</strong>. Check to allow download.</div>
        </div>
      </div>
      <div class="form-group"><label>Tags (comma separated)</label>
        <input class="form-control" id="nTags" placeholder="python, basics, week1"></div>
      <div class="form-group"><label>File *</label>
        <input class="form-control" type="file" id="nFile" accept=".pdf,.mp4,.webm,.mov,.ppt,.pptx">
        <div class="form-hint">PDF, Video (MP4/WEBM/MOV), Presentation (PPT/PPTX) — Max 500 MB</div>      </div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="submitUploadNote()">Upload</button>
    </div>`, 'modal-md');
}

async function submitUploadNote() {
  const file = el('nFile').files[0];
  if (!el('nTitle').value.trim()) { toast('Title is required','warning'); return; }
  if (!file) { toast('Please select a file','warning'); return; }
  const fd = new FormData();
  fd.append('title', el('nTitle').value.trim());
  fd.append('description', el('nDesc').value.trim());
  fd.append('course_id', el('nCourse').value);
  fd.append('category', el('nCat').value);
  fd.append('visibility', el('nVis').value);
  fd.append('is_downloadable', el('nDL').checked);
  fd.append('tags', el('nTags').value.trim());
  fd.append('file', file);
  const { ok, data } = await api('/api/notes/upload', { method:'POST', body: fd });
  if (ok) { closeModal(); toast('Note uploaded'); loadNotes(); }
  else toast(data.error||'Upload failed','danger');
}

async function showEditNoteModal(id) {
  const [nr, cr] = await Promise.all([api(`/api/notes/${id}`), api('/api/courses/')]);
  if (!nr.ok) { toast('Failed to load','danger'); return; }
  const n = nr.data.note;
  const courses = cr.data.courses||[];
  showModal(`
    ${modalHeader('Edit Note')}
    <div class="modal-body">
      <div class="form-group"><label>Title *</label>
        <input class="form-control" id="nTitle" value="${n.title}"></div>
      <div class="form-group"><label>Description</label>
        <textarea class="form-control" id="nDesc" rows="2">${n.description||''}</textarea></div>
      <div class="form-row">
        <div class="form-group"><label>Course</label>
          <select class="form-control" id="nCourse">
            <option value="">All Courses</option>
            ${courses.map(c=>`<option value="${c.id}" ${n.course_id==c.id?'selected':''}>${c.name}</option>`).join('')}
          </select></div>
        <div class="form-group"><label>Category</label>
          <select class="form-control" id="nCat">
            ${['General','Lecture Notes','Assignments','Study Material','Reference','Lab Work'].map(c=>`<option ${n.category===c?'selected':''}>${c}</option>`).join('')}
          </select></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>Visibility</label>
          <select class="form-control" id="nVis">
            <option value="all" ${n.visibility==='all'?'selected':''}>All Users</option>
            <option value="students" ${n.visibility==='students'?'selected':''}>Students Only</option>
            <option value="admin" ${n.visibility==='admin'?'selected':''}>Admin Only</option>
          </select></div>
        <div class="form-group">
          <label style="margin-bottom:20px;">&nbsp;</label>
          <label style="display:flex;align-items:center;gap:8px;cursor:pointer;">
            <input type="checkbox" id="nDL" ${n.is_downloadable?'checked':''}> Allow students to download
          </label>
        </div>
      </div>
      <div class="form-group"><label>Tags</label>
        <input class="form-control" id="nTags" value="${n.tags||''}"></div>
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary" onclick="closeModal()">Cancel</button>
      <button class="btn btn-primary" onclick="submitEditNote(${id})">Save Changes</button>
    </div>`, 'modal-md');
}

async function submitEditNote(id) {
  const payload = {
    title: el('nTitle').value.trim(), description: el('nDesc').value.trim(),
    course_id: el('nCourse').value||null, category: el('nCat').value,
    visibility: el('nVis').value, is_downloadable: el('nDL').checked,
    tags: el('nTags').value.trim()
  };
  const { ok, data } = await api(`/api/notes/${id}`, {
    method:'PUT', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)
  });
  if (ok) { closeModal(); toast('Note updated'); loadNotes(); }
  else toast(data.error||'Failed','danger');
}

async function deleteNote(id) {
  confirmDialog('Delete this note and its file?', async () => {
    const { ok, data } = await api(`/api/notes/${id}`, { method:'DELETE' });
    if (ok) { toast('Note deleted'); loadNotes(); }
    else toast(data.error||'Failed','danger');
  });
}

// ─── REPORTS ──────────────────────────────────────────────────────────────────
function loadReports() {
  html('pageContent', `
    <div class="page-header"><h2>Reports &amp; Exports</h2></div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px;">
      ${[
        { title:'Student Report', desc:'Export all student records as CSV', url:'/api/reports/export/students', color:'blue' },
        { title:'Attendance Report', desc:'Export attendance records by date range', url:'/api/reports/export/attendance', color:'green' },
        { title:'Fee Collection Report', desc:'Export fee payment records', url:'/api/reports/export/fees', color:'amber' },
        { title:'Notes Report', desc:'Export study notes listing', url:'/api/reports/export/notes', color:'purple' },
      ].map(r=>`
        <div class="card">
          <div class="stat-icon-box ${r.color}" style="margin-bottom:12px;">${I.export}</div>
          <h4 style="font-size:14px;font-weight:700;margin-bottom:6px;">${r.title}</h4>
          <p style="font-size:13px;color:var(--gray-500);margin-bottom:16px;">${r.desc}</p>
          <button class="btn btn-secondary btn-sm" onclick="window.open('${r.url}','_blank')">${I.download} Export CSV</button>
        </div>`).join('')}
    </div>`);
}

// ─── ACTIVITY ─────────────────────────────────────────────────────────────────
async function loadActivity() {
  const { ok, data } = await api('/api/dashboard/activity?per_page=100');
  if (!ok) { html('pageContent', `<div class="alert alert-error">Failed</div>`); return; }
  html('pageContent', `
    <div class="page-header"><h2>Activity Log</h2></div>
    <div class="card">
      <div class="table-wrap">
        <table>
          <thead><tr><th>User</th><th>Action</th><th>Details</th><th>Status</th><th>Time</th></tr></thead>
          <tbody>
            ${!data.activities.length ? `<tr><td colspan="5">${emptyState('No activity yet')}</td></tr>` :
              data.activities.map(a=>`<tr>
                <td>${a.user_name||a.user}</td>
                <td>${badge(a.action,'info')}</td>
                <td style="max-width:300px;white-space:normal;">${a.details||'—'}</td>
                <td>${statusBadge(a.status==='SUCCESS'?'active':'dropped')}</td>
                <td class="text-muted text-small">${new Date(a.timestamp).toLocaleString('en-IN')}</td>
              </tr>`).join('')}
          </tbody>
        </table>
      </div>
    </div>`);
}

// ─── SETTINGS ─────────────────────────────────────────────────────────────────
async function loadSettings() {
  const { ok, data } = await api('/api/settings/');
  const s = ok ? data.settings : {};
  html('pageContent', `
    <div class="page-header"><h2>Settings</h2></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
      <div class="card">
        <div class="card-header"><h3>Institute Profile</h3></div>
        <div class="form-group"><label>Institute Name</label>
          <input class="form-control" id="sInst" value="${s.institute_name||'Oxford LMS'}"></div>
        <div class="form-group"><label>Address</label>
          <textarea class="form-control" id="sAddr" rows="3">${s.institute_address||''}</textarea></div>
        <div class="form-group"><label>Phone</label>
          <input class="form-control" id="sPh" value="${s.institute_phone||''}"></div>
        <div class="form-group"><label>Email</label>
          <input class="form-control" id="sEm" value="${s.institute_email||''}"></div>
        <div class="form-group"><label>Website</label>
          <input class="form-control" id="sWeb" value="${s.institute_website||''}"></div>
        <button class="btn btn-primary" onclick="saveSettings()">Save Changes</button>
      </div>
      <div class="card">
        <div class="card-header"><h3>Receipt Settings</h3></div>
        <div class="form-group"><label>Receipt Number Prefix</label>
          <input class="form-control" id="sPrefix" value="${s.receipt_prefix||'OXLMS'}">
          <div class="form-hint">e.g. OXLMS/2026/0001</div></div>
        <div class="form-group"><label>Authorized Signatory</label>
          <input class="form-control" id="sSig" value="${s.authorized_signatory||'Administrator'}"></div>
        <div class="form-group"><label>Currency Symbol</label>
          <input class="form-control" id="sCur" value="${s.currency_symbol||'Rs.'}"></div>
        <div class="form-group"><label>Receipt Footer Text</label>
          <textarea class="form-control" id="sFooter" rows="2">${s.receipt_footer||'Thank you for your payment.'}</textarea></div>
        <div class="card" style="background:var(--gray-50);margin-top:16px;">
          <div class="form-section-title">Change Admin Password</div>
          <div class="form-group"><label>Current Password</label>
            <input class="form-control" type="password" id="sPwOld"></div>
          <div class="form-group"><label>New Password</label>
            <input class="form-control" type="password" id="sPwNew" placeholder="Min 6 characters"></div>
          <button class="btn btn-secondary" onclick="changeAdminPassword()">Update Password</button>
        </div>
      </div>
    </div>`);
}

async function saveSettings() {
  const payload = {
    institute_name: el('sInst').value.trim(),
    institute_address: el('sAddr').value.trim(),
    institute_phone: el('sPh').value.trim(),
    institute_email: el('sEm').value.trim(),
    institute_website: el('sWeb').value.trim(),
    receipt_prefix: el('sPrefix').value.trim().toUpperCase(),
    authorized_signatory: el('sSig').value.trim(),
    currency_symbol: el('sCur').value.trim(),
    receipt_footer: el('sFooter').value.trim()
  };
  const { ok, data } = await api('/api/settings/', {
    method:'PUT', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload)
  });
  if (ok) toast('Settings saved');
  else toast(data.error||'Failed','danger');
}

async function changeAdminPassword() {
  const oldPw = el('sPwOld').value;
  const newPw = el('sPwNew').value;
  if (!oldPw || !newPw) { toast('Both fields required','warning'); return; }
  if (newPw.length < 6) { toast('Password must be 6+ characters','warning'); return; }
  const { ok, data } = await api('/api/auth/change-password', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ old_password: oldPw, new_password: newPw })
  });
  if (ok) { toast('Password changed'); el('sPwOld').value=''; el('sPwNew').value=''; }
  else toast(data.error||'Failed','danger');
}

// ─── STUDENT SECTIONS ─────────────────────────────────────────────────────────
async function loadMyCourse() {
  const { ok, data } = await api('/api/dashboard/');
  if (!ok) { html('pageContent','<div class="alert alert-error">Failed</div>'); return; }
  const s = data.student;
  html('pageContent', `
    <div class="page-header"><h2>My Course</h2></div>
    <div class="card">
      <div class="detail-grid">
        <div class="detail-item"><div class="label">Course</div><div class="value">${s.course||'—'}</div></div>
        <div class="detail-item"><div class="label">Batch</div><div class="value">${s.batch||'—'}</div></div>
        <div class="detail-item"><div class="label">Status</div><div class="value">${statusBadge(s.status||'active')}</div></div>
        <div class="detail-item"><div class="label">Joining Date</div><div class="value">${fmtDate(s.joining_date)}</div></div>
      </div>
    </div>`);
}

async function loadMyAttendance() {
  const { ok: dok, data: dd } = await api('/api/dashboard/');
  if (!dok) { html('pageContent','<div class="alert alert-error">Failed</div>'); return; }
  const sid = dd.student.id;
  const { ok, data } = await api(`/api/attendance/student/${sid}`);
  if (!ok) { html('pageContent','<div class="alert alert-error">Failed to load attendance</div>'); return; }
  const st = data.statistics;
  const pct = st.percentage;
  html('pageContent', `
    <div class="page-header"><h2>My Attendance</h2></div>
    <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:16px;">
      ${[['Total Days',st.total_days,'blue'],['Present',st.present,'green'],['Absent',st.absent,'red'],['Percentage',pct+'%',pct>=75?'green':'red']].map(([l,v,c])=>`
        <div class="stat-card"><div class="stat-icon-box ${c}">${I.attendance}</div>
        <div class="stat-body"><div class="stat-value">${v}</div><div class="stat-label">${l}</div></div></div>`).join('')}
    </div>
    <div class="card">
      <div class="table-wrap">
        <table><thead><tr><th>Date</th><th>Status</th><th>Remarks</th></tr></thead>
        <tbody>
          ${!data.attendance.length ? `<tr><td colspan="3">${emptyState('No attendance records')}</td></tr>` :
            data.attendance.map(r=>`<tr>
              <td>${fmtDate(r.date)}</td>
              <td>${statusBadge(r.status)}</td>
              <td>${r.remarks||'—'}</td>
            </tr>`).join('')}
        </tbody>
        </table>
      </div>
    </div>`);
}

async function loadMyFees() {
  const { ok: dok, data: dd } = await api('/api/dashboard/');
  if (!dok) { html('pageContent','<div class="alert alert-error">Failed</div>'); return; }
  const sid = dd.student.id;
  const { ok, data } = await api(`/api/fees/student/${sid}/summary`);
  if (!ok) { html('pageContent','<div class="alert alert-error">Failed to load fees</div>'); return; }
  const pct = data.total_fee > 0 ? Math.min(100, Math.round(data.total_paid/data.total_fee*100)) : 0;
  html('pageContent', `
    <div class="page-header"><h2>My Fees</h2></div>
    <div class="fee-summary-bar" style="margin-bottom:16px;">
      <div class="fee-bar-item"><div class="fb-label">Total Fee</div><div class="fb-value">${fmtMoney(data.total_fee)}</div></div>
      <div class="fee-bar-item paid"><div class="fb-label">Paid</div><div class="fb-value">${fmtMoney(data.total_paid)}</div></div>
      <div class="fee-bar-item due"><div class="fb-label">Remaining</div><div class="fb-value">${fmtMoney(data.remaining)}</div></div>
    </div>
    ${data.fee_account?.next_due_date ? `<div class="alert alert-warning" style="margin-bottom:16px;">${I.alert_tri} Next installment due: <strong>${fmtDate(data.fee_account.next_due_date)}</strong> — ${fmtMoney(data.fee_account.installment_amount)}</div>` : ''}
    <div class="card">
      <div class="card-header"><h3>Payment History</h3></div>
      <div class="table-wrap">
        <table><thead><tr><th>Receipt</th><th>Amount</th><th>Date</th><th>Mode</th><th></th></tr></thead>
        <tbody>
          ${!data.payments.length ? `<tr><td colspan="5">${emptyState('No payments recorded')}</td></tr>` :
            data.payments.map(p=>`<tr>
              <td>${badge(p.receipt_number,'purple')}</td>
              <td style="color:var(--success);font-weight:600;">${fmtMoney(p.amount)}</td>
              <td>${fmtDate(p.payment_date)}</td>
              <td>${badge(p.payment_mode||'—','info')}</td>
              <td><button class="btn btn-xs btn-secondary" onclick="window.open('/api/fees/payments/${p.id}/receipt','_blank')">${I.receipt}</button></td>
            </tr>`).join('')}
        </tbody>
        </table>
      </div>
    </div>`);
}

async function loadMyNotes() {
  const { ok, data } = await api('/api/notes/');
  if (!ok) { html('pageContent','<div class="alert alert-error">Failed</div>'); return; }
  // Cache all notes for the viewer
  (data.notes || []).forEach(n => { window._noteCache[n.id] = n; });
  html('pageContent', `
    <div class="page-header"><h2>Study Notes</h2></div>
    <div class="card">
      <div class="table-wrap">
        <table><thead><tr>
          <th>Title</th><th>Course</th><th>Category</th><th>Date</th><th>Access</th><th>Actions</th>
        </tr></thead>
        <tbody>
          ${!data.notes.length ? `<tr><td colspan="6">${emptyState('No notes available for your course/batch')}</td></tr>` :
            data.notes.map(n => `<tr>
              <td><strong>${n.title}</strong></td>
              <td>${n.course_name || badge('All','gray')}</td>
              <td>${badge(n.category||'General','info')}</td>
              <td>${fmtDate(n.uploaded_at)}</td>
              <td>${n.is_downloadable ? badge('View + Download','success') : badge('View Only','warning')}</td>
              <td style="white-space:nowrap;display:flex;gap:6px;">
                <button class="btn btn-xs btn-secondary"
                  onclick="cacheAndOpenNote(${n.id})">${I.eye} Open</button>
                ${n.is_downloadable ? `<button class="btn btn-xs btn-primary"
                  onclick="window.open('/api/notes/${n.id}/download','_blank')">${I.download}</button>` : ''}
              </td>
            </tr>`).join('')}
        </tbody>
        </table>
      </div>
    </div>`);
}

async function loadFavorites() {
  const { ok, data } = await api('/api/notes/?favorites=true');
  if (!ok) { html('pageContent','<div class="alert alert-error">Failed</div>'); return; }
  (data.notes || []).forEach(n => { window._noteCache[n.id] = n; });
  html('pageContent', `
    <div class="page-header"><h2>Favorites</h2></div>
    <div class="card">
      ${!data.notes.length ? emptyState('No favorites yet') : `
      <div class="table-wrap">
        <table><thead><tr>
          <th>Title</th><th>Category</th><th>Date</th><th>Access</th><th>Actions</th>
        </tr></thead>
        <tbody>
          ${data.notes.map(n=>`<tr>
            <td><strong>${n.title}</strong></td>
            <td>${badge(n.category||'General','info')}</td>
            <td>${fmtDate(n.uploaded_at)}</td>
            <td>${n.is_downloadable ? badge('View + Download','success') : badge('View Only','warning')}</td>
            <td style="white-space:nowrap;display:flex;gap:6px;">
              <button class="btn btn-xs btn-secondary"
                onclick="cacheAndOpenNote(${n.id})">${I.eye} Open</button>
              ${n.is_downloadable ? `<button class="btn btn-xs btn-primary"
                onclick="window.open('/api/notes/${n.id}/download','_blank')">${I.download}</button>` : ''}
            </td>
          </tr>`).join('')}
        </tbody>
        </table>
      </div>`}
    </div>`);
}

async function loadMyProfile() {
  const [authRes, dashRes] = await Promise.all([api('/api/auth/me'), api('/api/dashboard/')]);
  if (!authRes.ok) { html('pageContent','<div class="alert alert-error">Failed</div>'); return; }
  const u = authRes.data.user;
  const s = dashRes.ok && dashRes.data.student ? dashRes.data.student : null;

  const photoSrc = u.profile_image
    ? `/api/profile-image/${u.profile_image}`
    : `https://ui-avatars.com/api/?name=${encodeURIComponent(u.full_name||u.username)}&background=1e3a5f&color=f59e0b&size=80`;

  html('pageContent', `
    <div class="page-header"><h2>My Profile</h2></div>
    <div class="card" style="max-width:540px;">

      <!-- Photo section -->
      <div style="display:flex;align-items:center;gap:20px;padding-bottom:20px;
                  border-bottom:1px solid var(--gray-200);margin-bottom:20px;">
        <div style="position:relative;flex-shrink:0;">
          <img id="myProfilePhoto" src="${photoSrc}"
            onerror="this.src='https://ui-avatars.com/api/?name=${encodeURIComponent(u.full_name||u.username)}&background=1e3a5f&color=f59e0b&size=80'"
            style="width:88px;height:88px;border-radius:50%;object-fit:cover;
                   border:3px solid var(--gray-200);display:block;">
        </div>
        <div style="flex:1;">
          <h3 style="font-size:18px;font-weight:700;margin-bottom:4px;">${u.full_name||u.username}</h3>
          <p style="color:var(--gray-500);font-size:13px;margin-bottom:12px;">
            ${u.username} &nbsp;&bull;&nbsp; ${badge(u.role,'info')}
          </p>
          ${s ? `
          <label class="btn btn-secondary btn-sm" style="cursor:pointer;display:inline-flex;align-items:center;gap:6px;">
            ${I.edit} Change Photo
            <input type="file" accept=".jpg,.jpeg,.png" style="display:none;"
              onchange="uploadMyPhoto(this, ${s.id})">
          </label>` : ''}
        </div>
      </div>

      <!-- Info grid -->
      <div class="detail-grid">
        <div class="detail-item"><div class="label">Student ID</div><div class="value">${u.username}</div></div>
        <div class="detail-item"><div class="label">Email</div><div class="value">${u.email||'—'}</div></div>
        ${s ? `
        <div class="detail-item"><div class="label">Course</div><div class="value">${s.course||'—'}</div></div>
        <div class="detail-item"><div class="label">Batch</div><div class="value">${s.batch||'—'}</div></div>
        <div class="detail-item"><div class="label">Phone</div><div class="value">${s.phone||'—'}</div></div>
        <div class="detail-item"><div class="label">Joining Date</div><div class="value">${fmtDate(s.joining_date)}</div></div>
        <div class="detail-item"><div class="label">Gender</div><div class="value">${s.gender||'—'}</div></div>
        <div class="detail-item"><div class="label">Status</div><div class="value">${statusBadge(s.status||'active')}</div></div>
        ` : ''}
      </div>
    </div>`);
}

async function uploadMyPhoto(input, studentId) {
  if (!input.files || !input.files[0]) return;
  const fd = new FormData();
  fd.append('file', input.files[0]);
  const { ok, data } = await api(`/api/students/${studentId}/profile-image`, {
    method: 'POST', body: fd
  });
  if (ok) {
    // Update the displayed photo immediately and the topbar avatar
    const reader = new FileReader();
    reader.onload = e => {
      const img = document.getElementById('myProfilePhoto');
      if (img) img.src = e.target.result;
      // Refresh topbar and sidebar avatars
      const newSrc = `/api/profile-image/${data.profile_image}`;
      const ta = el('topbarAvatar');  if (ta) ta.src = newSrc;
      const sa = el('sidebarAvatar'); if (sa) sa.src = newSrc;
      if (G.user) G.user.profile_image = data.profile_image;
    };
    reader.readAsDataURL(input.files[0]);
    toast('Profile photo updated!');
  } else {
    toast(data.error || 'Photo upload failed', 'danger');
  }
}

// ─── NOTIFICATIONS / PROFILE ──────────────────────────────────────────────────
function toggleNotifications() { /* simple placeholder — could expand to dropdown */ }

function showProfileModal() {
  const u = G.user;
  const isAdmin = u.role !== 'student';
  showModal(`
    ${modalHeader('My Profile')}
    <div class="modal-body" style="text-align:center;">
      <img src="${el('topbarAvatar').src}" style="width:72px;height:72px;border-radius:50%;border:3px solid var(--gray-200);margin-bottom:12px;">
      <h3 style="font-size:16px;font-weight:700;">${u.full_name||u.username}</h3>
      <p style="color:var(--gray-500);margin-bottom:16px;">${badge(u.role,'info')} &nbsp; ${u.email||''}</p>
      ${isAdmin ? `
      <div style="text-align:left;border-top:1px solid var(--gray-200);padding-top:16px;">
        <div class="form-group"><label>Current Password</label><input class="form-control" type="password" id="pwOld"></div>
        <div class="form-group"><label>New Password</label><input class="form-control" type="password" id="pwNew" placeholder="Min 6 characters"></div>
        <button class="btn btn-secondary w-full" onclick="changeAdminPasswordModal()">Update Password</button>
      </div>` : ''}
    </div>
    <div class="modal-footer">
      <button class="btn btn-danger" onclick="logout()">Logout</button>
      <button class="btn btn-secondary" onclick="closeModal()">Close</button>
    </div>`, 'modal-sm');
}

async function changeAdminPasswordModal() {
  const oldPw = el('pwOld').value;
  const newPw = el('pwNew').value;
  if (!oldPw || !newPw) { toast('Both fields required','warning'); return; }
  if (newPw.length < 6) { toast('Password must be 6+ characters','warning'); return; }
  const { ok, data } = await api('/api/auth/change-password', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({ old_password: oldPw, new_password: newPw })
  });
  if (ok) { closeModal(); toast('Password changed'); }
  else toast(data.error||'Failed','danger');
}

// ─── BOOT ─────────────────────────────────────────────────────────────────────

/**
 * Safe wrapper around openNoteViewer so inline onclick attrs
 * work without complex JSON serialisation issues.
 * Called from renderNoteRow / student note rows.
 */
window._noteCache = {};
function cacheAndOpenNote(noteId) {
  const note = window._noteCache[noteId];
  if (!note) { toast('Note data not available, try refreshing', 'warning'); return; }
  openNoteViewer(note, G.user);
}

window.addEventListener('DOMContentLoaded', init);
