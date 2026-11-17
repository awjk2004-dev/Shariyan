const API = window.SHARIYAN_API_BASE_URL || (
  location.hostname === '127.0.0.1' || location.hostname === 'localhost'
    ? 'http://127.0.0.1:8000/api'                  // التطوير المحلي
    : 'https://shariyan-81fl.onrender.com/api'     // الإنتاج (Render)
);
const token = () => localStorage.getItem('shريان_token');
function escapeHTML(value) { return String(value ?? '').replace(/[&<>"']/g, character => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[character])); }
function safeAppLink(value) { try { const url = new URL(String(value || ''), location.href); return ['http:', 'https:'].includes(url.protocol) && url.origin === location.origin ? `${url.pathname}${url.search}${url.hash}` : 'index.html'; } catch (_) { return 'index.html'; } }
const headers = () => token() ? {Authorization: `Bearer ${token()}`, 'Content-Type': 'application/json'} : {'Content-Type': 'application/json'};
async function api(path, options = {}) { const response = await fetch(API + path, {...options, headers: {...headers(), ...(options.headers || {})}}); const data = await response.json().catch(() => ({})); if (!response.ok) throw new Error(data.detail || 'حدث خطأ غير متوقع'); return data; }
function showMessage(text, error = false) { const box = document.querySelector('[data-message]'); if (box) { box.textContent = text; box.className = `notice${error ? ' error' : ''}`; } }
function requireAuth() { if (!token()) location.href = 'login.html'; }
async function renderNav() { const nav = document.querySelector('[data-nav]'); if (nav && token()) { nav.querySelectorAll('a[href="login.html"]').forEach(link => link.remove()); nav.querySelectorAll('a[href="register.html"]').forEach(link => link.remove()); nav.innerHTML += '<a href="notifications.html">الإشعارات</a><a href="#" data-logout>خروج</a>'; try { const user = await api('/auth/me'); if (user.is_admin) nav.innerHTML += '<a href="dashboard.html">لوحة التحكم</a><a href="admin.html">إدارة البيانات</a>'; } catch (_) {} } document.querySelector('[data-logout]')?.addEventListener('click', () => { localStorage.removeItem('shريان_token'); location.href='index.html'; }); }
function addHomeLink() { document.querySelectorAll('.nav').forEach(nav => { if (!nav.querySelector('a[href="index.html"]')) { const link = document.createElement('a'); link.href = 'index.html'; link.textContent = 'الرئيسية'; nav.prepend(link); } if (!nav.querySelector('a[href="about.html"]')) { const link = document.createElement('a'); link.href = 'about.html'; link.textContent = 'عن المنصة'; nav.append(link); } }); }
const brandStyles = document.createElement('link');
brandStyles.rel = 'stylesheet';
brandStyles.href = 'css/brand-system.css?v=brand-20261117-v2';
document.head.append(brandStyles);
document.addEventListener('DOMContentLoaded', () => { renderNav(); addHomeLink(); });
