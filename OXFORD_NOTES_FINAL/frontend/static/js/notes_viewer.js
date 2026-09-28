/**
 * Oxford LMS — Document/Video Viewer
 *
 * Supported types:
 *   PDF               → PDF.js canvas renderer (no browser toolbar)
 *   MP4 / WEBM / MOV  → HTML5 <video> player (controlslist blocks download)
 *   PPT / PPTX        → Google Docs Viewer (read-only embed)
 *
 * View Only: watermark overlay + anti-copy/print protections (PDF + PPT).
 * View + Download: separate Download button shown only when permitted.
 *
 * Security note: OS-level screenshots cannot be prevented in a web browser.
 * These controls are deterrence, not DRM.
 */

(function () {
  'use strict';

  const VIDEO_TYPES = new Set(['mp4', 'webm', 'mov']);
  const PPT_TYPES   = new Set(['ppt', 'pptx']);
  const PDF_TYPE    = 'pdf';

  // ── PDF.js state ─────────────────────────────────────────────────────────
  let _pdfDoc     = null;
  let _pageNum    = 1;
  let _pageCount  = 0;
  let _scale      = 1.2;
  let _renderTask = null;
  let _handlers   = [];

  function esc(s) {
    if (!s) return '';
    return String(s)
      .replace(/&/g,'&amp;').replace(/</g,'&lt;')
      .replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
  }

  // ─────────────────────────────────────────────────────────────────────────
  // MAIN ENTRY
  // ─────────────────────────────────────────────────────────────────────────
  window.openNoteViewer = function (note, user) {
    const existing = document.getElementById('noteViewerOverlay');
    if (existing) existing.remove();
    _removeHandlers();

    _scale   = 1.2;
    _pageNum = 1;
    _pdfDoc  = null;

    const ft           = (note.file_type || '').toLowerCase();
    const isViewOnly   = !note.is_downloadable;
    const isStudent    = user.role === 'student';
    const showWatermark = isViewOnly && isStudent;
    const canDl        = !isViewOnly || user.role === 'admin';

    const wmName = esc(user.full_name || user.username || '');
    const wmId   = esc(user.username || '');

    // ── Build type-specific body & toolbar ─────────────────────────────
    let bodyHtml    = '';
    let extraToolbar = '';

    if (ft === PDF_TYPE) {
      extraToolbar = `
        <div style="display:flex;align-items:center;gap:6px;
                    padding:0 14px;border-left:1px solid rgba(255,255,255,.1);height:100%;">
          <button class="vtbtn" title="Zoom out"  onclick="pdfZoom(-0.2)">&#8722;</button>
          <span id="zoomLabel" style="font-size:12px;color:rgba(255,255,255,.65);
                                      min-width:40px;text-align:center;">120%</span>
          <button class="vtbtn" title="Zoom in"   onclick="pdfZoom(+0.2)">&#43;</button>
          <div style="width:1px;height:20px;background:rgba(255,255,255,.12);margin:0 4px;"></div>
          <button id="btnPrev" class="vtbtn" title="Previous page" onclick="pdfPrevPage()">&#8592;</button>
          <span   id="pageInfo" style="font-size:12px;color:rgba(255,255,255,.65);
                                       min-width:52px;text-align:center;">— / —</span>
          <button id="btnNext" class="vtbtn" title="Next page" onclick="pdfNextPage()">&#8594;</button>
        </div>`;

      bodyHtml = `
        <div id="pdfScroll" style="
          flex:1;overflow-y:auto;overflow-x:auto;background:#525659;
          display:flex;flex-direction:column;align-items:center;
          padding:20px 16px;box-sizing:border-box;">
          <div id="pdfSpinner" style="
            display:flex;flex-direction:column;align-items:center;
            gap:12px;color:#fff;margin-top:60px;">
            <div style="width:36px;height:36px;border-radius:50%;
                        border:3px solid rgba(255,255,255,.2);border-top-color:#f59e0b;
                        animation:_pvSpin .8s linear infinite;"></div>
            <div style="font-size:13px;opacity:.7;">Loading PDF&hellip;</div>
          </div>
          <canvas id="pdfCanvas" style="display:none;box-shadow:0 4px 24px rgba(0,0,0,.5);background:#fff;"></canvas>
        </div>`;

    } else if (VIDEO_TYPES.has(ft)) {
      // HTML5 video — controlslist prevents the native download button
      const mimeMap = { mp4:'video/mp4', webm:'video/webm', mov:'video/mp4' };
      const mime = mimeMap[ft] || 'video/mp4';
      bodyHtml = `
        <div style="flex:1;background:#000;display:flex;align-items:center;justify-content:center;overflow:hidden;">
          <video id="noteVideo"
            src="/api/notes/${note.id}/view"
            type="${mime}"
            controls
            controlslist="nodownload nofullscreen noremoteplayback"
            disablepictureinpicture
            style="max-width:100%;max-height:100%;display:block;outline:none;"
            oncontextmenu="return false;">
            Your browser does not support HTML5 video.
          </video>
        </div>`;

    } else if (PPT_TYPES.has(ft)) {
      const fileUrl = encodeURIComponent(`${location.origin}/api/notes/${note.id}/view`);
      bodyHtml = `
        <div style="flex:1;position:relative;background:#f0f0f0;">
          <div id="gdocsSpinner" style="
            position:absolute;inset:0;display:flex;flex-direction:column;
            align-items:center;justify-content:center;
            background:#2a2a2a;color:#fff;gap:12px;z-index:5;">
            <div style="width:32px;height:32px;border-radius:50%;
                        border:3px solid rgba(255,255,255,.2);border-top-color:#f59e0b;
                        animation:_pvSpin .8s linear infinite;"></div>
            <div style="font-size:13px;opacity:.8;">Loading presentation&hellip;</div>
            <div style="font-size:11px;opacity:.45;">Powered by Google Docs Viewer</div>
          </div>
          <iframe
            src="https://docs.google.com/viewer?url=${fileUrl}&embedded=true"
            style="width:100%;height:100%;border:none;display:block;"
            onload="var s=document.getElementById('gdocsSpinner');if(s)s.remove();"
            title="${esc(note.title)}">
          </iframe>
        </div>`;

    } else {
      bodyHtml = `
        <div style="flex:1;display:flex;flex-direction:column;align-items:center;
                    justify-content:center;color:#fff;gap:16px;text-align:center;padding:40px;background:#2a2a2a;">
          <div style="font-size:48px;opacity:.3;">&#x1F4C4;</div>
          <div style="font-size:15px;font-weight:600;">
            Cannot preview .${esc(note.file_type||'?')} files in the browser</div>
          <div style="font-size:13px;opacity:.6;">This file format cannot be displayed inline.</div>
          ${canDl ? `
            <button onclick="downloadNoteFromViewer(${note.id})" style="
              margin-top:8px;padding:10px 24px;background:#2563eb;color:#fff;
              border:none;border-radius:8px;font-size:14px;font-weight:600;cursor:pointer;">
              Download to view</button>` :
            `<div style="font-size:12px;opacity:.45;margin-top:4px;">
              This note is View Only — contact your instructor.</div>`}
        </div>`;
    }

    // ── Watermark (PDF + PPT only — not on video) ───────────────────────
    const showWm = showWatermark && !VIDEO_TYPES.has(ft);
    const watermarkHtml = showWm ? `
      <div style="
        position:absolute;top:46px;left:0;right:0;bottom:0;
        pointer-events:none;overflow:hidden;
        display:grid;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(5,1fr);
        z-index:50;">
        ${Array(15).fill(`
          <div style="display:flex;align-items:center;justify-content:center;
            transform:rotate(-32deg);opacity:.055;
            font-size:10px;font-weight:900;color:#000;
            white-space:nowrap;pointer-events:none;user-select:none;
            text-align:center;line-height:1.7;">
            OXFORD LMS<br>${wmName}<br>${wmId}</div>
        `).join('')}
      </div>` : '';

    // ── Assemble overlay ────────────────────────────────────────────────
    const overlay = document.createElement('div');
    overlay.id    = 'noteViewerOverlay';
    overlay.style.cssText = `
      position:fixed;inset:0;z-index:9000;
      background:rgba(10,20,40,.88);
      display:flex;flex-direction:column;
      font-family:'Inter',-apple-system,sans-serif;`;

    overlay.innerHTML = `
      <style>
        .vtbtn {
          min-width:28px;height:28px;background:rgba(255,255,255,.1);
          border:none;color:#fff;border-radius:5px;padding:0 6px;
          font-size:15px;line-height:1;cursor:pointer;
          display:inline-flex;align-items:center;justify-content:center;
          transition:background .15s;
        }
        .vtbtn:hover    { background:rgba(255,255,255,.22); }
        .vtbtn:active   { background:rgba(255,255,255,.32); }
        .vtbtn:disabled { opacity:.35;cursor:default; }
        #pdfScroll::-webkit-scrollbar       { width:8px;height:8px; }
        #pdfScroll::-webkit-scrollbar-track { background:#333; }
        #pdfScroll::-webkit-scrollbar-thumb { background:#666;border-radius:4px; }
        #pdfScroll::-webkit-scrollbar-thumb:hover { background:#888; }
        @keyframes _pvSpin { to { transform:rotate(360deg); } }
      </style>

      <!-- Header bar -->
      <div style="display:flex;align-items:center;height:46px;flex-shrink:0;
                  background:#0f2340;border-bottom:1px solid rgba(255,255,255,.08);">

        <!-- Logo + title -->
        <div style="display:flex;align-items:center;gap:10px;padding:0 16px;flex:1;min-width:0;">
          <img src="/static/assets/oxford_logo.jpg" alt="Oxford Logo" style="width:26px;height:26px;border-radius:5px;flex-shrink:0;object-fit:cover;">
          <div style="min-width:0;">
            <div style="font-size:13px;font-weight:700;color:#fff;
                        overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">
              ${esc(note.title)}</div>
            <div style="font-size:10px;color:rgba(255,255,255,.4);margin-top:1px;">
              ${_typeLabel(ft)} &mdash;
              ${isViewOnly
                ? 'VIEW ONLY &mdash; Downloading not permitted'
                : 'View &amp; Download'}</div>
          </div>
        </div>

        <!-- Type-specific controls (PDF zoom/page nav) -->
        ${extraToolbar}

        <!-- Download + Close -->
        <div style="display:flex;align-items:center;gap:8px;padding:0 14px;flex-shrink:0;">
          ${canDl ? `
            <button onclick="downloadNoteFromViewer(${note.id})" style="
              padding:5px 14px;background:#2563eb;color:#fff;border:none;
              border-radius:5px;font-size:12px;font-weight:600;cursor:pointer;">
              Download</button>` : ''}
          <button class="vtbtn" onclick="closeNoteViewer()"
                  style="font-size:18px;width:30px;height:30px;" title="Close">&times;</button>
        </div>
      </div>

      <!-- Body -->
      <div id="viewerBody" style="flex:1;position:relative;overflow:hidden;
                                   display:flex;flex-direction:column;background:#2a2a2a;">
        ${bodyHtml}
        ${watermarkHtml}
      </div>`;

    document.body.appendChild(overlay);

    if (isViewOnly && !VIDEO_TYPES.has(ft)) _applyProtections(overlay, ft);

    if (ft === PDF_TYPE) _loadPdfJs(() => _initPdf(note.id));
  };

  // ── Type label ────────────────────────────────────────────────────────────
  function _typeLabel(ft) {
    if (ft === 'pdf')  return 'PDF';
    if (VIDEO_TYPES.has(ft)) return 'Video';
    if (PPT_TYPES.has(ft))   return 'Presentation';
    return ft.toUpperCase();
  }

  // ── PDF.js loader ─────────────────────────────────────────────────────────
  function _loadPdfJs(cb) {
    if (window.pdfjsLib) { cb(); return; }
    const s   = document.createElement('script');
    s.src     = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js';
    s.onload  = () => {
      window.pdfjsLib.GlobalWorkerOptions.workerSrc =
        'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
      cb();
    };
    s.onerror = () => _pdfError('Failed to load PDF renderer. Check your connection.');
    document.head.appendChild(s);
  }

  // ── PDF init ──────────────────────────────────────────────────────────────
  async function _initPdf(noteId) {
    try {
      const res = await fetch(`/api/notes/${noteId}/view`, { credentials:'include' });
      if (!res.ok) { _pdfError(`Server error ${res.status} loading PDF.`); return; }
      const buf = await res.arrayBuffer();

      const loadTask = window.pdfjsLib.getDocument({ data: buf });
      _pdfDoc    = await loadTask.promise;
      _pageCount = _pdfDoc.numPages;
      _pageNum   = 1;

      const spinner = document.getElementById('pdfSpinner');
      const canvas  = document.getElementById('pdfCanvas');
      if (spinner) spinner.style.display = 'none';
      if (canvas)  canvas.style.display  = 'block';

      _updatePdfUI();
      await _renderPage(_pageNum);
    } catch (err) {
      console.error('PDF load error:', err);
      _pdfError('Could not load PDF: ' + (err.message || String(err)));
    }
  }

  // ── PDF render ────────────────────────────────────────────────────────────
  async function _renderPage(num) {
    if (!_pdfDoc) return;
    const canvas = document.getElementById('pdfCanvas');
    const scroll = document.getElementById('pdfScroll');
    if (!canvas || !scroll) return;

    if (_renderTask) { _renderTask.cancel(); _renderTask = null; }

    const page       = await _pdfDoc.getPage(num);
    const containerW = scroll.clientWidth - 48;
    const vp0        = page.getViewport({ scale:1 });
    const autoScale  = containerW / vp0.width;
    const viewport   = page.getViewport({ scale: autoScale * _scale });

    canvas.width  = viewport.width;
    canvas.height = viewport.height;

    _renderTask = page.render({ canvasContext: canvas.getContext('2d'), viewport });
    try {
      await _renderTask.promise;
      _renderTask = null;
      scroll.scrollTop = 0;
    } catch (e) {
      if (e?.name !== 'RenderingCancelledException') console.error('Render err:', e);
    }
  }

  function _updatePdfUI() {
    const pi   = document.getElementById('pageInfo');
    const zl   = document.getElementById('zoomLabel');
    const prev = document.getElementById('btnPrev');
    const next = document.getElementById('btnNext');
    if (pi)   pi.textContent = `${_pageNum} / ${_pageCount}`;
    if (zl)   zl.textContent = Math.round(_scale * 100) + '%';
    if (prev) prev.disabled  = _pageNum <= 1;
    if (next) next.disabled  = _pageNum >= _pageCount;
  }

  function _pdfError(msg) {
    const spinner = document.getElementById('pdfSpinner');
    if (spinner) spinner.innerHTML = `
      <div style="color:#f87171;font-size:14px;text-align:center;padding:20px;max-width:360px;">
        <div style="font-size:32px;margin-bottom:12px;">&#x26A0;</div>${esc(msg)}</div>`;
  }

  // ── Public PDF controls ────────────────────────────────────────────────────
  window.pdfZoom = async function (delta) {
    _scale = Math.max(0.4, Math.min(3.5, _scale + delta));
    _updatePdfUI();
    await _renderPage(_pageNum);
  };

  window.pdfPrevPage = async function () {
    if (!_pdfDoc || _pageNum <= 1) return;
    _pageNum--; _updatePdfUI(); await _renderPage(_pageNum);
  };

  window.pdfNextPage = async function () {
    if (!_pdfDoc || _pageNum >= _pageCount) return;
    _pageNum++; _updatePdfUI(); await _renderPage(_pageNum);
  };

  // ── Close / download ────────────────────────────────────────────────────────
  window.closeNoteViewer = function () {
    if (_renderTask) { _renderTask.cancel(); _renderTask = null; }
    _pdfDoc = null;

    // Pause video if playing to avoid background audio
    const vid = document.getElementById('noteVideo');
    if (vid) { vid.pause(); vid.src = ''; }

    _removeHandlers();
    const ov = document.getElementById('noteViewerOverlay');
    if (ov) ov.remove();
  };

  window.downloadNoteFromViewer = function (noteId) {
    window.open(`/api/notes/${noteId}/download`, '_blank');
  };

  // ── View-only protections (PDF + PPT, not video) ────────────────────────────
  function _applyProtections(overlay, ft) {
    const rc = e => e.preventDefault();
    overlay.addEventListener('contextmenu', rc);
    _handlers.push({ el:overlay, type:'contextmenu', fn:rc });

    if (ft === PDF_TYPE) {
      const canvas = document.getElementById('pdfCanvas');
      if (canvas) {
        canvas.addEventListener('contextmenu', rc);
        _handlers.push({ el:canvas, type:'contextmenu', fn:rc });
      }
    }

    const BLOCKED = new Set(['c','p','s','a','u']);
    const kd = e => {
      if ((e.ctrlKey || e.metaKey) && BLOCKED.has(e.key.toLowerCase())) {
        e.preventDefault(); e.stopPropagation();
      }
    };
    document.addEventListener('keydown', kd, true);
    _handlers.push({ el:document, type:'keydown', fn:kd, capture:true });

    const ss = e => e.preventDefault();
    overlay.addEventListener('selectstart', ss);
    _handlers.push({ el:overlay, type:'selectstart', fn:ss });
  }

  function _removeHandlers() {
    _handlers.forEach(({ el, type, fn, capture }) => {
      el.removeEventListener(type, fn, capture || false);
    });
    _handlers = [];
  }

  // ── Keyboard shortcuts ──────────────────────────────────────────────────────
  document.addEventListener('keydown', e => {
    if (!document.getElementById('noteViewerOverlay')) return;
    if (e.key === 'Escape')                              closeNoteViewer();
    if (e.key === 'ArrowRight' || e.key === 'PageDown') pdfNextPage();
    if (e.key === 'ArrowLeft'  || e.key === 'PageUp')   pdfPrevPage();
    if (e.key === '+' || e.key === '=')                  pdfZoom(+0.2);
    if (e.key === '-')                                   pdfZoom(-0.2);
  });

})();
