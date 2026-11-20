const BANKS = [
  { code: "", label: "-- Chưa chọn ngân hàng --", keywords: "" },
  { code: "MOMO", label: "Ví MoMo (971025)", keywords: "momo vi momo psp 971025 ví momo" },
  { code: "VCB", label: "Vietcombank (VCB)", keywords: "vcb vietcombank ngoai thuong" },
  { code: "TCB", label: "Techcombank (TCB)", keywords: "tcb techcombank ky thuong" },
  { code: "MB", label: "MB Bank (MB)", keywords: "mb mbbank quan doi" },
  { code: "ACB", label: "ACB", keywords: "acb a chau" },
  { code: "BIDV", label: "BIDV", keywords: "bidv dau tu phat trien" },
  { code: "ICB", label: "VietinBank (ICB)", keywords: "icb vietinbank cong thuong" },
  { code: "VPB", label: "VPBank (VPB)", keywords: "vpb vpbank thinh vuong" },
  { code: "TPB", label: "TPBank (TPB)", keywords: "tpb tpbank tien phong" },
  { code: "STB", label: "Sacombank (STB)", keywords: "stb sacombank sai gon thuong tin" },
  { code: "VIB", label: "VIB", keywords: "vib quoc te" },
  { code: "HDB", label: "HDBank (HDB)", keywords: "hdb hdbank phat trien tphcm" },
  { code: "OCB", label: "OCB", keywords: "ocb phuong dong" },
  { code: "SHB", label: "SHB", keywords: "shb sai gon ha noi" },
  { code: "MSB", label: "MSB", keywords: "msb hang hai" },
  { code: "VBA", label: "Agribank (VBA)", keywords: "vba agribank nong nghiep" },
  { code: "CAKE", label: "CAKE by VPBank", keywords: "cake by vpbank ngan hang so" },
  { code: "TIMO", label: "Timo by BVBank", keywords: "timo by bvbank ban viet" },
  { code: "ZALOPAY", label: "Ví ZaloPay (971101)", keywords: "zalopay zalo pay vi dien tu 971101" },
  { code: "VTLMONEY", label: "Viettel Money (971005)", keywords: "viettel money vtl viettelpay 971005" },
  { code: "LPB", label: "LPBank (Lộc Phát)", keywords: "lpb lienvietpostbank loc phat" },
  { code: "SEAB", label: "SeABank", keywords: "seab seabank dong nam a" },
  { code: "NAB", label: "Nam A Bank", keywords: "nab nam a bank" },
  { code: "EXB", label: "Eximbank", keywords: "exb eximbank xuat nhap khau" },
];

const ICONS = {
  shuttle: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" class="svg-icon"><path d="M9 18c0 2 1.34 3.5 3 3.5s3-1.5 3-3.5v-1H9v1z" fill="currentColor" fill-opacity="0.22"/><line x1="9" y1="17" x2="15" y2="17" stroke-width="2"/><path d="M9 17L4 4.5"/><path d="M10.2 17L7.8 4.2"/><path d="M12 17V3.8"/><path d="M13.8 17l2.4-12.8"/><path d="M15 17l5-12.5"/><path d="M7.2 13.5c1.4.8 3.2 1.2 4.8 1.2s3.4-.4 4.8-1.2" stroke-width="1.6"/><path d="M5.5 9c1.9 1.1 4.2 1.7 6.5 1.7s4.6-.6 6.5-1.7" stroke-width="1.6"/><path d="M4 4.5c2.4.9 5.1 1.4 8 1.4s5.6-.5 8-1.4" stroke-width="1.8"/><path d="M4 4.5c1.2 4.5 3.2 9 5 12.5"/><path d="M20 4.5c-1.2 4.5-3.2 9-5 12.5"/></svg>`,
  court: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svg-icon"><rect width="20" height="14" x="2" y="5" rx="2"/><line x1="12" x2="12" y1="5" y2="19"/><line x1="2" x2="22" y1="12" y2="12"/><circle cx="12" cy="12" r="2.5"/></svg>`,
  parking: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svg-icon"><rect width="18" height="18" x="3" y="3" rx="4"/><path d="M9 17V7h4a3 3 0 0 1 0 6H9"/></svg>`,
  snack: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svg-icon"><circle cx="9" cy="7" r="2"/><path d="M7.2 7.9 3 11v9c0 .6.4 1 1 1h16c.6 0 1-.4 1-1v-9c0-2-3-6-7-8l-3.6 2.6"/><path d="M16 13H3"/><path d="M16 17H3"/></svg>`,
  drink: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svg-icon"><path d="M17 8h1a4 4 0 1 1 0 8h-1"/><path d="M3 8h14v9a4 4 0 0 1-4 4H7a4 4 0 0 1-4-4Z"/><line x1="6" x2="6" y1="2" y2="4"/><line x1="10" x2="10" y1="2" y2="4"/><line x1="14" x2="14" y1="2" y2="4"/></svg>`,
  other: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svg-icon"><path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1-2-1Z"/><path d="M14 8H8"/><path d="M16 12H8"/><path d="M13 16H8"/></svg>`,
  linked: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" class="svg-icon svg-linked"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>`,
  couple: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" class="svg-icon svg-linked"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/></svg>`,
  bank: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svg-icon"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>`,
  qr: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svg-icon"><rect width="5" height="5" x="3" y="3" rx="1"/><rect width="5" height="5" x="16" y="3" rx="1"/><rect width="5" height="5" x="3" y="16" rx="1"/><path d="M21 16h-3a2 2 0 0 0-2 2v3"/><path d="M21 21v.01"/><path d="M12 7v3a2 2 0 0 1-2 2H7"/><path d="M3 12h.01"/><path d="M12 3h.01"/><path d="M12 16v.01"/><path d="M16 12h1"/><path d="M21 12v.01"/><path d="M12 21v-1"/></svg>`,
  copy: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svg-icon"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>`,
  check: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="svg-icon"><polyline points="20 6 9 17 4 12"/></svg>`,
  arrowRight: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svg-icon"><line x1="5" x2="19" y1="12" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>`,
  edit: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svg-icon"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg>`,
  trash: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="svg-icon"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" x2="10" y1="11" y2="17"/><line x1="14" x2="14" y1="11" y2="17"/></svg>`,
  plus: `<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" class="svg-icon"><line x1="12" x2="12" y1="5" y2="19"/><line x1="5" x2="19" y1="12" y2="12"/></svg>`,
};

const AVATAR_PALETTES = [
  { bg: "linear-gradient(135deg, #10b981 0%, #059669 100%)", color: "#ffffff", shadow: "rgba(16, 185, 129, 0.3)" },
  { bg: "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)", color: "#ffffff", shadow: "rgba(59, 130, 246, 0.3)" },
  { bg: "linear-gradient(135deg, #8b5cf6 0%, #6d28d9 100%)", color: "#ffffff", shadow: "rgba(139, 92, 246, 0.3)" },
  { bg: "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)", color: "#ffffff", shadow: "rgba(245, 158, 11, 0.3)" },
  { bg: "linear-gradient(135deg, #ec4899 0%, #be185d 100%)", color: "#ffffff", shadow: "rgba(236, 72, 153, 0.3)" },
  { bg: "linear-gradient(135deg, #06b6d4 0%, #0e7490 100%)", color: "#ffffff", shadow: "rgba(6, 182, 212, 0.3)" },
  { bg: "linear-gradient(135deg, #6366f1 0%, #4338ca 100%)", color: "#ffffff", shadow: "rgba(99, 102, 241, 0.3)" },
  { bg: "linear-gradient(135deg, #14b8a6 0%, #0f766e 100%)", color: "#ffffff", shadow: "rgba(20, 184, 166, 0.3)" },
  { bg: "linear-gradient(135deg, #f97316 0%, #c2410c 100%)", color: "#ffffff", shadow: "rgba(249, 115, 22, 0.3)" },
  { bg: "linear-gradient(135deg, #a855f7 0%, #7e22ce 100%)", color: "#ffffff", shadow: "rgba(168, 85, 247, 0.3)" },
  { bg: "linear-gradient(135deg, #0ea5e9 0%, #0369a1 100%)", color: "#ffffff", shadow: "rgba(14, 165, 233, 0.3)" },
  { bg: "linear-gradient(135deg, #84cc16 0%, #4d7c0f 100%)", color: "#ffffff", shadow: "rgba(132, 204, 22, 0.3)" },
];

function getAvatarStyle(name, id = null) {
  let idx = 0;
  if (id !== null && id !== undefined && Number.isFinite(Number(id)) && Number(id) > 0) {
    idx = Math.abs(Number(id)) % AVATAR_PALETTES.length;
  } else {
    let hash = 2166136261;
    const str = String(name || "A");
    for (let i = 0; i < str.length; i++) {
      hash ^= str.charCodeAt(i);
      hash = Math.imul(hash, 16777619);
    }
    idx = (hash >>> 0) % AVATAR_PALETTES.length;
  }
  const p = AVATAR_PALETTES[idx];
  return `background: ${p.bg}; color: ${p.color}; box-shadow: 0 2px 6px ${p.shadow}; border: 1.5px solid rgba(255, 255, 255, 0.7);`;
}

const CAT_META = {
  court: { label: "Tiền sân", iconSvg: ICONS.court, colorClass: "cat-court", defaultSplit: "equal_split" },
  shuttle: { label: "Tiền cầu", iconSvg: ICONS.shuttle, colorClass: "cat-shuttle", defaultSplit: "equal_split" },
  parking: { label: "Gửi xe", iconSvg: ICONS.parking, colorClass: "cat-parking", defaultSplit: "parking" },
  snack: { label: "Bánh / Ăn nhẹ", iconSvg: ICONS.snack, colorClass: "cat-snack", defaultSplit: "itemized" },
  drink: { label: "Nước uống", iconSvg: ICONS.drink, colorClass: "cat-drink", defaultSplit: "itemized" },
  other: { label: "Khoản khác", iconSvg: ICONS.other, colorClass: "cat-other", defaultSplit: "equal_split" },
};

function getInitials(name) {
  if (!name) return "??";
  const parts = name.trim().split(/\s+/);
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
}

const state = {
  members: [],
  hiddenMembers: [],
  sessions: [],
  current: null, // full session payload
  qrTarget: null,
  expenseDraft: {
    equalIds: new Set(),
    parkingIds: new Set(),
    items: [],
  },
  sessionParticipantIds: new Set(),
  sessionCouplePairs: new Map(), // memberId -> payerId
};

// ---------- Helpers ----------

function vnd(n) {
  const num = Number(n) || 0;
  return num.toLocaleString("vi-VN") + "đ";
}

function formatSigned(n) {
  const num = Number(n) || 0;
  return (num > 0 ? "+" : "") + vnd(num);
}

function readMoneyInput(id, fallback) {
  const raw = document.getElementById(id).value;
  if (String(raw).trim() === "") return fallback;
  const num = Number(raw);
  if (!Number.isFinite(num) || num < 0) return fallback;
  return Math.round(num);
}

function moneyOrFallback(value, fallback) {
  if (value === null || value === undefined || value === "") return fallback;
  const num = Number(value);
  return Number.isFinite(num) ? num : fallback;
}

function netOriginHtml(r) {
  const merged = Boolean(r.paid_by_name) || (r.paid_for_names && r.paid_for_names.length);
  if (!merged) return "";
  const rawText = formatSigned(r.raw_net);
  if (r.paid_by_name) {
    return `<div class="net-origin">Gốc ${rawText} · đã gộp sang ${escapeHtml(r.paid_by_name)}</div>`;
  }
  return `<div class="net-origin">Gốc ${rawText} · gồm phần của ${escapeHtml(r.paid_for_names.join(", "))}</div>`;
}

function escapeHtml(str) {
  return String(str ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function removeVietnameseTones(str) {
  return String(str || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/đ/g, "d")
    .replace(/Đ/g, "D")
    .replace(/[^a-zA-Z0-9\s-]/g, "")
    .trim();
}

function toVietnameseUpperNoTones(str) {
  return String(str || "")
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .replace(/đ/g, "D")
    .replace(/Đ/g, "D")
    .replace(/[^a-zA-Z0-9\s]/g, "")
    .toUpperCase();
}

function showToast(msg) {
  const el = document.getElementById("toast");
  el.textContent = msg;
  el.classList.remove("hidden");
  clearTimeout(showToast._t);
  showToast._t = setTimeout(() => el.classList.add("hidden"), 2600);
}

async function api(url, options = {}) {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    let msg = "Có lỗi xảy ra";
    try {
      const err = await res.json();
      msg = err.detail || msg;
    } catch (_) {}
    throw new Error(msg);
  }
  return res.json();
}

function openModal(id) {
  document.getElementById(id).classList.remove("hidden");
}

function closeModal(id) {
  document.getElementById(id).classList.add("hidden");
}

function switchTab(tabName) {
  document.querySelectorAll(".nav-tab").forEach((b) => {
    b.classList.toggle("active", b.dataset.tab === tabName);
  });
  document.querySelectorAll(".tab-panel").forEach((p) => {
    p.classList.toggle("active", p.id === `tab-${tabName}`);
  });
}

function closeAllCustomSelects() {
  document.querySelectorAll(".custom-select-menu").forEach((m) => m.classList.add("hidden"));
  document.querySelectorAll(".custom-select-trigger").forEach((t) => {
    t.classList.remove("active");
    t.setAttribute("aria-expanded", "false");
  });
}

function setupCustomSelectEvents() {
  const bankTrigger = document.getElementById("custom-select-bank-trigger");
  const bankMenu = document.getElementById("custom-select-bank-menu");
  const bankSearch = document.getElementById("bank-search-input");

  if (bankTrigger && bankMenu) {
    bankTrigger.addEventListener("click", (e) => {
      e.stopPropagation();
      const isClosed = bankMenu.classList.contains("hidden");
      closeAllCustomSelects();
      if (isClosed) {
        bankMenu.classList.remove("hidden");
        bankTrigger.classList.add("active");
        bankTrigger.setAttribute("aria-expanded", "true");
        if (bankSearch) {
          bankSearch.value = "";
          renderCustomBankOptions("");
          setTimeout(() => bankSearch.focus(), 60);
        }
      }
    });

    if (bankSearch) {
      bankSearch.addEventListener("input", (e) => {
        renderCustomBankOptions(e.target.value);
      });
      bankSearch.addEventListener("click", (e) => e.stopPropagation());
    }
  }

  const payerTrigger = document.getElementById("custom-select-payer-trigger");
  const payerMenu = document.getElementById("custom-select-payer-menu");

  if (payerTrigger && payerMenu) {
    payerTrigger.addEventListener("click", (e) => {
      e.stopPropagation();
      const isClosed = payerMenu.classList.contains("hidden");
      closeAllCustomSelects();
      if (isClosed) {
        payerMenu.classList.remove("hidden");
        payerTrigger.classList.add("active");
        payerTrigger.setAttribute("aria-expanded", "true");
      }
    });
  }

  document.addEventListener("click", (e) => {
    if (!e.target.closest(".custom-select")) {
      closeAllCustomSelects();
    }
  });
}

// ---------- Data Loading ----------

async function initApp() {
  populateBankSelect();
  setupCustomSelectEvents();
  bindEvents();
  initScoreboard();
  await loadMembers();
  await loadSessions();

  const urlParams = new URLSearchParams(window.location.search);
  const requestedId = Number(urlParams.get("session"));
  if (requestedId && state.sessions.some((s) => s.id === requestedId)) {
    await openSession(requestedId);
  } else if (state.sessions.length > 0) {
    await openSession(state.sessions[0].id);
  } else {
    renderCurrentSession();
  }
}

async function loadMembers() {
  const all = await api("/api/members?include_inactive=true");
  state.members = all.filter((m) => Number(m.is_active) === 1);
  state.hiddenMembers = all.filter((m) => Number(m.is_active) !== 1);
  renderMembers();
}

async function loadSessions() {
  state.sessions = await api("/api/sessions");
  renderHistory();
}

async function openSession(sessionId) {
  state.current = await api(`/api/sessions/${sessionId}`);
  const url = new URL(window.location.href);
  url.searchParams.set("session", sessionId);
  window.history.replaceState({}, "", url);
  renderCurrentSession();
  switchTab("session");
}

// ---------- Rendering: Current Session ----------

function renderCurrentSession() {
  const emptyEl = document.getElementById("session-empty");
  const wsEl = document.getElementById("session-workspace");

  if (!state.current) {
    emptyEl.classList.remove("hidden");
    wsEl.classList.add("hidden");
    return;
  }

  emptyEl.classList.add("hidden");
  wsEl.classList.remove("hidden");

  const { session, participants, expenses, summary, settlements } = state.current;

  document.getElementById("sess-title").textContent = session.title;
  document.getElementById("sess-date-badge").textContent = session.played_at;
  document.getElementById("sess-notes").textContent = session.notes || "";
  const templateBadge = document.getElementById("sess-template-badge");
  if (templateBadge) templateBadge.classList.toggle("hidden", Number(session.is_template) !== 1);
  const templateBtn = document.getElementById("btn-toggle-template");
  if (templateBtn) {
    templateBtn.textContent = Number(session.is_template) === 1 ? "Bỏ mẫu mặc định" : "Đặt làm mẫu";
  }

  const statusBadge = document.getElementById("sess-status-badge");
  if (session.status === "settled") {
    statusBadge.innerHTML = `<span class="badge-dot badge-dot-settled"></span> Đã hoàn tất`;
    statusBadge.className = "badge badge-settled";
  } else {
    statusBadge.innerHTML = `<span class="badge-dot badge-dot-open"></span> Đang thu tiền`;
    statusBadge.className = "badge badge-open";
  }

  document.getElementById("kpi-total-spent").textContent = vnd(summary.total_spent);
  document.getElementById("kpi-participants").textContent = `${participants.length} người`;
  const paidCount = settlements.filter((s) => s.is_paid).length;
  document.getElementById("kpi-transfers").textContent = `${paidCount} / ${settlements.length} đã trả`;

  const progressFill = document.getElementById("kpi-progress-fill");
  if (progressFill) {
    const pct = settlements.length > 0 ? Math.round((paidCount / settlements.length) * 100) : 0;
    progressFill.style.width = `${pct}%`;
  }

  const warnEl = document.getElementById("session-warnings");
  if (summary.warnings && summary.warnings.length > 0) {
    warnEl.innerHTML = summary.warnings.map((w) => `⚠️ ${escapeHtml(w)}`).join("<br/>");
    warnEl.classList.remove("hidden");
  } else {
    warnEl.classList.add("hidden");
  }

  renderExpensesList(expenses, participants);
  renderSettlementsList(settlements);
  renderBreakdownTable(summary.member_summaries);
  renderBreakdownCards(summary.member_summaries);
}

function renderExpensesList(expenses, participants) {
  const container = document.getElementById("expenses-list");
  if (!expenses.length) {
    container.innerHTML = `
      <div class="empty-hint-card">
        <div class="empty-hint-icon">${ICONS.shuttle}</div>
        <p>Chưa có khoản chi nào trong buổi này.</p>
        <small class="muted">Bấm các nút bên trên để nhập nhanh Tiền sân, Tiền cầu, Gửi xe 5k, Bánh hoặc Nước.</small>
      </div>`;
    return;
  }

  const nameById = Object.fromEntries(participants.map((p) => [p.id, p.name]));

  container.innerHTML = expenses
    .map((exp) => {
      const meta = CAT_META[exp.category] || CAT_META.other;
      let detailHtml = "";
      let payerText = exp.payer_name ? `Người ứng: <strong class="text-primary">${escapeHtml(exp.payer_name)}</strong>` : "Chưa chọn người ứng";

      if (exp.split_type === "equal_split") {
        const names = exp.participant_ids.map((id) => nameById[id]).filter(Boolean);
        const allIn = names.length === participants.length;
        const peelNote =
          Number(exp.parking_deducted) > 0
            ? `<div class="expense-meta">Hóa đơn ${vnd(exp.invoice_total)} · đã tách ${vnd(exp.parking_deducted)} gửi xe. Số trên thẻ là phần sân còn lại.</div>`
            : "";
        detailHtml = `<div class="expense-meta">${payerText} · <span class="tag-pill">Chia đều ${names.length} người ${
          allIn ? "(cả nhóm)" : `(${escapeHtml(names.join(", "))})`
        }</span></div>${peelNote}`;
      } else if (exp.split_type === "parking") {
        const names = exp.participant_ids.map((id) => nameById[id]).filter(Boolean);
        let modeText = payerText;
        if (exp.parking_mode === "included_in_court") {
          if (Number(exp.parking_unmatched)) {
            modeText = "<span class='tag-pill tag-pill-blue'>Chưa có hóa đơn sân. Khoản này đang ghi nợ từng người và chưa có người nhận.</span>";
          } else if (Number(exp.parking_unfunded) > 0) {
            modeText = `<span class='tag-pill tag-pill-blue'>Đã tách ${vnd(exp.computed_total)} từ hóa đơn sân. ${vnd(exp.parking_unfunded)} vượt hóa đơn nên không ghi nợ.</span>`;
          } else {
            modeText = "<span class='tag-pill tag-pill-blue'>Đã tách từ hóa đơn sân. Cộng với phần sân còn lại thì bằng hóa đơn.</span>";
          }
        }
        detailHtml = `<div class="expense-meta">${modeText} · ${vnd(exp.unit_fee)}/xe × ${names.length} người (${escapeHtml(
          names.join(", ") || "chưa chọn"
        )})</div>`;
      } else if (exp.split_type === "itemized") {
        const rows = (exp.items || [])
          .map((it) => {
            const names = it.participant_ids.map((id) => nameById[id]).filter(Boolean);
            const sub = it.pricing_mode === "per_person" ? it.amount * names.length : it.amount;
            const modeLabel =
              it.pricing_mode === "per_person"
                ? `${vnd(it.amount)}/người × ${names.length}`
                : `Chia đều ${vnd(it.amount)}`;
            return `<li><strong>${escapeHtml(it.item_name || "Món")}</strong>: ${modeLabel} = <strong>${vnd(sub)}</strong> <span class="muted small">(${escapeHtml(
              names.join(", ") || "chưa chọn"
            )})</span></li>`;
          })
          .join("");
        detailHtml = `<div class="expense-meta">${payerText}</div><ul class="expense-subitems">${rows}</ul>`;
      }

      return `
        <div class="expense-card">
          <div class="expense-main">
            <div class="expense-top">
              <div class="expense-icon-badge ${meta.colorClass}">${meta.iconSvg}</div>
              <div>
                <span class="expense-name">${escapeHtml(exp.title)}</span>
                ${detailHtml}
              </div>
            </div>
          </div>
          <div class="expense-right">
            <span class="expense-amount">${vnd(exp.computed_total)}</span>
            <div class="action-row">
              <button class="btn btn-secondary btn-xs btn-icon-action" onclick="openEditExpense(${exp.id})" title="Sửa">${ICONS.edit} <span>Sửa</span></button>
              <button class="btn btn-danger btn-xs btn-icon-action" onclick="deleteExpense(${exp.id})" title="Xóa">${ICONS.trash} <span>Xóa</span></button>
            </div>
          </div>
        </div>
      `;
    })
    .join("");
}

function renderSettlementsList(settlements) {
  const container = document.getElementById("settlements-list");
  const summaries = state.current?.summary?.member_summaries || [];
  const leftover = summaries.filter((m) => Number(m.net));
  if (!settlements.length) {
    if (leftover.length) {
      const rows = leftover
        .map(
          (m) =>
            `<li><span>${escapeHtml(m.name)}</span><strong class="${m.net > 0 ? "net-pos" : "net-neg"}">${formatSigned(m.net)}</strong></li>`
        )
        .join("");
      container.innerHTML = `
        <div class="empty-hint-card">
          <div class="empty-hint-icon">${ICONS.other}</div>
          <p>Còn số dư chưa có lệnh chuyển</p>
          <ul class="leftover-list">${rows}</ul>
          <small class="muted">Sổ chưa cân, nên chưa có người nhận cho khoản nợ này.</small>
        </div>`;
    } else {
      container.innerHTML = `
        <div class="empty-hint-card">
          <div class="empty-hint-icon">${ICONS.check}</div>
          <p>Mọi người đã cân bằng thu chi (0đ).</p>
          <small class="muted">Không còn khoản chuyển tiền nào cần thực hiện.</small>
        </div>`;
    }
    return;
  }

  container.innerHTML = settlements
    .map((s) => {
      const hasBank = Boolean(s.to_bank_id && s.to_account_no);
      const fromInit = getInitials(s.from_name);
      const toInit = getInitials(s.to_name);

      return `
        <div class="settlement-card ${s.is_paid ? "is-paid" : ""}">
          <div class="settlement-left">
            <div class="settlement-avatars">
              <div class="avatar-circle" style="${getAvatarStyle(s.from_name, s.from_member_id)}" title="${escapeHtml(s.from_name)}">${fromInit}</div>
              <div class="avatar-arrow-icon">${ICONS.arrowRight}</div>
              <div class="avatar-circle" style="${getAvatarStyle(s.to_name, s.to_member_id)}" title="${escapeHtml(s.to_name)}">${toInit}</div>
            </div>
            <div class="settlement-details">
              <div class="settlement-names">
                <span class="name-from">${escapeHtml(s.from_name)}</span>
                <span class="arrow-text">chuyển cho</span>
                <span class="name-to">${escapeHtml(s.to_name)}</span>
              </div>
              <div class="settlement-subinfo">
                ${
                  s.is_paid && s.paid_at
                    ? `<span class="paid-stamp">${ICONS.check} Đã thanh toán lúc ${escapeHtml(s.paid_at)}</span>`
                    : hasBank
                    ? `<span class="bank-pill"><span class="bank-badge">${escapeHtml(s.to_bank_id)}</span> ${escapeHtml(s.to_account_no)}</span>`
                    : `<span class="muted small text-amber">Chưa có STK ngân hàng của ${escapeHtml(s.to_name)}</span>`
                }
              </div>
            </div>
          </div>
          <div class="settlement-right">
            <div class="settlement-amount">${vnd(s.amount)}</div>
            <div class="settlement-actions">
              <button class="btn btn-secondary btn-sm btn-qr-action" onclick="openQrModal(${s.id})">
                ${ICONS.qr} <span>Mã QR</span>
              </button>
              <label class="paid-switch-label">
                <input type="checkbox" ${s.is_paid ? "checked" : ""} onchange="toggleSettlementPaid(${s.id}, this.checked)" />
                <span class="paid-custom-check ${s.is_paid ? "checked" : ""}">
                  ${s.is_paid ? ICONS.check : ""}
                </span>
                <span class="paid-label-text">${s.is_paid ? "Đã trả" : "Chưa trả"}</span>
              </label>
            </div>
          </div>
        </div>
      `;
    })
    .join("");
}

function renderBreakdownTable(rows) {
  const tbody = document.getElementById("breakdown-tbody");
  tbody.innerHTML = rows
    .map((r) => {
      const b = r.breakdown;
      const netCls = r.net > 0 ? "net-pos" : r.net < 0 ? "net-neg" : "";
      const netPrefix = r.net > 0 ? "+" : "";
      let coupleBadge = "";
      if (r.couple_cycle) {
        coupleBadge = `<button type="button" class="couple-pill-btn cycle-pill" onclick="openCoupleLinkModal(${r.member_id})" title="Ghép đang bị vòng">${ICONS.linked} Ghép vòng, tự trả</button>`;
      } else if (r.paid_by_name) {
        coupleBadge = `<button type="button" class="couple-pill-btn" onclick="openCoupleLinkModal(${r.member_id})" title="Bấm để chỉnh sửa">${ICONS.linked} ${escapeHtml(r.paid_by_name)} trả</button>`;
      } else if (r.paid_for_names && r.paid_for_names.length) {
        coupleBadge = `<button type="button" class="couple-pill-btn payer-pill" onclick="openCoupleLinkModal(${r.member_id})" title="Bấm để chỉnh sửa">${ICONS.linked} Trả thay (${r.paid_for_names.length})</button>`;
      } else {
        coupleBadge = `<button type="button" class="btn btn-ghost btn-xs text-muted" onclick="openCoupleLinkModal(${r.member_id})">${ICONS.linked} Ghép</button>`;
      }
      return `
        <tr>
          <td>
            <div class="member-td-flex">
              <span class="avatar-sm" style="${getAvatarStyle(r.name, r.member_id)}">${getInitials(r.name)}</span>
              <strong>${escapeHtml(r.name)}</strong>
            </div>
          </td>
          <td class="num">${vnd(b.court)}</td>
          <td class="num">${vnd(b.shuttle)}</td>
          <td class="num">${vnd(b.parking)}</td>
          <td class="num">${vnd(b.snack)}</td>
          <td class="num">${vnd(b.drink + b.other)}</td>
          <td class="num"><strong>${vnd(r.consumed)}</strong></td>
          <td class="num">${vnd(r.paid)}</td>
          <td class="num ${netCls}"><strong>${netPrefix}${vnd(r.net)}</strong>${netOriginHtml(r)}</td>
          <td>${coupleBadge}</td>
        </tr>
      `;
    })
    .join("");
}

function renderBreakdownCards(rows) {
  const container = document.getElementById("breakdown-cards");
  if (!container) return;
  container.innerHTML = rows
    .map((r) => {
      const b = r.breakdown;
      const netCls = r.net > 0 ? "net-pos" : r.net < 0 ? "net-neg" : "";
      const netPrefix = r.net > 0 ? "+" : "";
      let coupleBanner = "";
      if (r.couple_cycle) {
        coupleBanner = `<div class="mb-couple-banner note-cycle">${ICONS.linked} Ghép đang bị vòng, nên người này tự giữ số dư.</div>`;
      } else if (r.paid_by_name) {
        coupleBanner = `<div class="mb-couple-banner note-couple">${ICONS.linked} <strong>${escapeHtml(r.paid_by_name)}</strong> sẽ đại diện thanh toán chung cho phần này (đã gộp)</div>`;
      } else if (r.paid_for_names && r.paid_for_names.length) {
        coupleBanner = `<div class="mb-couple-banner note-payer">${ICONS.linked} Nhận trả thay cho: <strong>${escapeHtml(r.paid_for_names.join(", "))}</strong></div>`;
      }
      return `
        <div class="mb-card">
          <div class="mb-card-head">
            <div class="mb-card-title">
              <span class="avatar-sm" style="${getAvatarStyle(r.name, r.member_id)}">${getInitials(r.name)}</span>
              <strong>${escapeHtml(r.name)}</strong>
              <button type="button" class="couple-pill-btn ${r.couple_cycle ? "cycle-pill" : r.paid_for_names?.length ? "payer-pill" : ""}" onclick="openCoupleLinkModal(${r.member_id})">
                ${r.couple_cycle ? `${ICONS.linked} Ghép vòng, tự trả` : r.paid_by_name ? `${ICONS.linked} ${escapeHtml(r.paid_by_name)} trả` : r.paid_for_names?.length ? `${ICONS.linked} Trả thay (${r.paid_for_names.length})` : `${ICONS.linked} Trả kèm`}
              </button>
            </div>
            <div class="mb-net-amount ${netCls}">
              ${netPrefix}${vnd(r.net)}
            </div>
          </div>
          ${coupleBanner}
          <div class="mb-chips-row">
            ${b.court ? `<span class="mb-chip chip-court">${ICONS.court} Sân: ${vnd(b.court)}</span>` : ""}
            ${b.shuttle ? `<span class="mb-chip chip-shuttle">${ICONS.shuttle} Cầu: ${vnd(b.shuttle)}</span>` : ""}
            ${b.parking ? `<span class="mb-chip chip-parking">${ICONS.parking} Xe: ${vnd(b.parking)}</span>` : ""}
            ${b.snack ? `<span class="mb-chip chip-snack">${ICONS.snack} Bánh: ${vnd(b.snack)}</span>` : ""}
            ${(b.drink + b.other) ? `<span class="mb-chip chip-drink">${ICONS.drink} Nước: ${vnd(b.drink + b.other)}</span>` : ""}
          </div>
          <div class="mb-card-foot">
            <div class="mb-foot-item">
              <span class="muted small">Thực tiêu:</span>
              <strong>${vnd(r.consumed)}</strong>
            </div>
            <div class="mb-foot-item">
              <span class="muted small">Đã ứng chi:</span>
              <strong>${vnd(r.paid)}</strong>
            </div>
            <div class="mb-foot-item">
              <span class="muted small">Cân đối:</span>
              <strong class="${netCls}">${netPrefix}${vnd(r.net)}</strong>
              ${netOriginHtml(r)}
            </div>
          </div>
        </div>
      `;
    })
    .join("");
}

window.openCoupleLinkModal = function (memberId) {
  if (!state.current) return;
  const member = state.current.participants.find((p) => p.id === memberId);
  if (!member) return;
  document.getElementById("couple-link-member-id").value = memberId;
  document.getElementById("couple-link-desc").textContent = `Thiết lập người trả chung tiền cho "${member.name}" trong buổi này:`;
  const select = document.getElementById("select-couple-payer");
  const currentPayerId = member.payer_member_id;
  select.innerHTML = `
    <option value="">-- Tự thanh toán riêng (Không ghép cặp) --</option>
    ${state.current.participants
      .filter((p) => p.id !== memberId)
      .map((p) => `<option value="${p.id}" ${currentPayerId === p.id ? "selected" : ""}>🔗 ${escapeHtml(p.name)} trả chung</option>`)
      .join("")}
  `;
  openModal("modal-couple-link");
};

// ---------- Rendering: History & Members ----------

function renderHistory() {
  const container = document.getElementById("history-list");
  if (!state.sessions.length) {
    container.innerHTML = `<p class="muted small">Chưa có lịch sử buổi đánh nào.</p>`;
    return;
  }
  container.innerHTML = state.sessions
    .map((s) => {
      const done = s.status === "settled";
      return `
        <div class="history-card" onclick="openSession(${s.id})">
          <div>
            <div class="badge-row">
              <span class="badge ${done ? "badge-settled" : "badge-open"}">${
        done ? "Hoàn tất" : `${s.paid_transfers}/${s.total_transfers} đã trả`
      }</span>
              <span class="badge badge-neutral">${escapeHtml(s.played_at)}</span>
              <span class="badge badge-neutral">${s.participant_count} người</span>
              ${Number(s.is_template) === 1 ? `<span class="badge badge-template">Mẫu mặc định</span>` : ""}
            </div>
            <strong style="display:block; margin-top:6px; font-size:15px;">${escapeHtml(s.title)}</strong>
          </div>
          <div class="history-actions" onclick="event.stopPropagation()">
            <strong style="align-self:center; margin-right:6px; color:var(--primary-dark);">${vnd(s.total_spent)}</strong>
            <button class="btn btn-secondary btn-xs" onclick="cloneSessionFrom(${s.id})">Giống buổi này</button>
            <button class="btn btn-secondary btn-xs" onclick="toggleSessionTemplate(${s.id}, ${Number(s.is_template) === 1 ? "false" : "true"})">${Number(s.is_template) === 1 ? "Bỏ mẫu" : "Đặt làm mẫu"}</button>
            <button class="btn btn-danger btn-sm" onclick="deleteSession(${s.id})">Xóa</button>
          </div>
        </div>
      `;
    })
    .join("");
}

function memberCardHtml(m, hidden) {
  const bankStr = m.bank_id && m.account_no
    ? `${m.bank_id} · ${m.account_no}${m.account_name ? ` (${m.account_name})` : ""}`
    : "Chưa cập nhật tài khoản ngân hàng";
  const initials = getInitials(m.name);
  const actions = hidden
    ? `<button class="btn btn-primary btn-sm" onclick="restoreMember(${m.id})">Hiện lại</button>`
    : `<button class="btn btn-secondary btn-sm btn-icon-action" onclick="openEditMember(${m.id})">${ICONS.edit} <span>Sửa</span></button>
       <button class="btn btn-danger btn-sm btn-icon-action" onclick="deleteMember(${m.id})">${ICONS.trash} <span>Ẩn</span></button>`;
  return `
    <div class="member-card ${hidden ? "is-hidden-member" : ""}">
      <div class="member-card-main">
        <div class="avatar-circle avatar-member" style="${getAvatarStyle(m.name, m.id)}">${initials}</div>
        <div class="member-card-text">
          <div class="member-title-row">
            <strong>${escapeHtml(m.name)}</strong>
            ${hidden ? `<span class="badge badge-neutral">Đã ẩn</span>` : m.is_regular ? `<span class="badge badge-settled">Cố định</span>` : `<span class="badge badge-neutral">Vãng lai</span>`}
            ${m.default_payer_name ? `<span class="badge badge-linked">${ICONS.linked} Trả kèm cùng ${escapeHtml(m.default_payer_name)}</span>` : ""}
          </div>
          <div class="member-bank-info">${ICONS.bank} <span>${escapeHtml(bankStr)}</span></div>
        </div>
      </div>
      <div class="action-row">${actions}</div>
    </div>
  `;
}

function renderMembers() {
  const container = document.getElementById("members-list");
  const hidden = state.hiddenMembers || [];
  if (!state.members.length && !hidden.length) {
    container.innerHTML = `
      <div class="empty-hint-card">
        <div class="empty-hint-icon">${ICONS.shuttle}</div>
        <p>Chưa có thành viên cố định nào.</p>
        <small class="muted">Thêm danh sách thành viên cố định của nhóm để tạo buổi đánh cực nhanh.</small>
      </div>`;
    return;
  }
  const activeHtml = state.members.length
    ? state.members.map((m) => memberCardHtml(m, false)).join("")
    : `<p class="muted small">Không còn thành viên đang hiện.</p>`;
  const hiddenHtml = hidden.length
    ? `<div class="hidden-members-block">
         <h3>Đã ẩn</h3>
         <p class="muted small">Những người này không hiện khi tạo buổi mới. Bấm Hiện lại để dùng tiếp. Buổi đánh cũ vẫn giữ tên họ.</p>
         ${hidden.map((m) => memberCardHtml(m, true)).join("")}
       </div>`
    : "";
  container.innerHTML = activeHtml + hiddenHtml;
}

function populateBankSelect() {
  renderCustomBankOptions();
}

window.setCustomBankValue = function (code) {
  const hidden = document.getElementById("input-member-bank");
  if (hidden) hidden.value = code || "";
  const b = BANKS.find((x) => x.code === code);
  const badge = document.getElementById("bank-badge-preview");
  const label = document.getElementById("bank-label-preview");
  const accInput = document.getElementById("input-member-accno");
  if (badge && label) {
    if (b && b.code) {
      badge.textContent = b.code;
      badge.className = "bank-trigger-badge active" + (b.code === "MOMO" ? " badge-momo" : "");
      label.textContent = b.label;
    } else {
      badge.textContent = "🏦";
      badge.className = "bank-trigger-badge";
      label.textContent = "-- Chưa chọn ngân hàng --";
    }
  }
  if (accInput) {
    if (code === "MOMO") {
      accInput.placeholder = "VD: PSP2600711000000104 hoặc SĐT MoMo";
    } else if (code === "ZALOPAY" || code === "VTLMONEY") {
      accInput.placeholder = "VD: Số điện thoại ví hoặc số tài khoản";
    } else {
      accInput.placeholder = "VD: 190368686868";
    }
  }
  closeAllCustomSelects();
};

function renderCustomBankOptions(filterText = "") {
  const container = document.getElementById("custom-select-bank-options");
  if (!container) return;
  const currentVal = document.getElementById("input-member-bank")?.value || "";
  const query = filterText.toLowerCase().trim();

  const filtered = BANKS.filter((b) => {
    if (!query) return true;
    const matchCode = b.code && b.code.toLowerCase().includes(query);
    const matchLabel = b.label && b.label.toLowerCase().includes(query);
    const matchKeywords = b.keywords && b.keywords.toLowerCase().includes(query);
    return matchCode || matchLabel || matchKeywords;
  });

  if (filtered.length === 0) {
    container.innerHTML = `<div class="custom-select-empty">Không tìm thấy ngân hàng "${escapeHtml(filterText)}"</div>`;
    return;
  }

  container.innerHTML = filtered
    .map((b) => {
      const isSelected = b.code === currentVal;
      const isMoMo = b.code === "MOMO";
      return `
        <div class="custom-select-option ${isSelected ? "selected" : ""}" onclick="setCustomBankValue('${b.code}')">
          <div class="option-left">
            <span class="bank-option-badge ${isMoMo ? "badge-momo" : ""}">${b.code || "✕"}</span>
            <span class="option-name">${escapeHtml(b.label)}</span>
          </div>
          ${isSelected ? `<span class="option-check">${ICONS.check}</span>` : ""}
        </div>
      `;
    })
    .join("");
}

// ---------- Session Modal ----------

function todaySessionTitle() {
  const now = new Date();
  const local = new Date(now.getTime() - now.getTimezoneOffset() * 60000);
  const today = local.toISOString().slice(0, 10);
  return { today, title: `Cầu lông ${today.split("-").reverse().join("/")}` };
}

function applyBlankSessionDefaults() {
  document.getElementById("input-session-parking").value = 5000;
  document.getElementById("input-session-notes").value = "";
  state.sessionParticipantIds = new Set(state.members.filter((m) => m.is_regular).map((m) => m.id));
  state.sessionCouplePairs = new Map();
  state.members.forEach((m) => {
    if (m.default_payer_id && state.sessionParticipantIds.has(m.id) && state.sessionParticipantIds.has(m.default_payer_id)) {
      state.sessionCouplePairs.set(m.id, m.default_payer_id);
    }
  });
}

function applyTemplateSource(full) {
  const activeIds = new Set(state.members.map((m) => m.id));
  state.sessionParticipantIds = new Set(full.participants.map((p) => p.id).filter((id) => activeIds.has(id)));
  state.sessionCouplePairs = new Map();
  full.participants.forEach((p) => {
    if (
      p.payer_member_id &&
      p.payer_member_id !== p.id &&
      state.sessionParticipantIds.has(p.id) &&
      state.sessionParticipantIds.has(p.payer_member_id)
    ) {
      state.sessionCouplePairs.set(p.id, p.payer_member_id);
    }
  });
  document.getElementById("input-session-parking").value = moneyOrFallback(full.session.parking_fee, 5000);
  document.getElementById("input-session-notes").value = full.session.notes || "";
}

function showTemplateChoice(full) {
  const box = document.getElementById("session-template-box");
  const checkbox = document.getElementById("input-use-template");
  if (!full) {
    box.classList.add("hidden");
    checkbox.checked = false;
    document.getElementById("session-template-id").value = "";
    state.templateSource = null;
    return;
  }
  state.templateSource = full;
  box.classList.remove("hidden");
  document.getElementById("session-template-id").value = full.session.id;
  checkbox.checked = true;
  const count = full.expenses.length;
  document.getElementById("template-box-label").textContent = `Chép form từ “${full.session.title}”`;
  document.getElementById("template-box-help").textContent =
    `Giữ người chơi, ghép cặp và ${count} khoản chi kèm số tiền hiện tại. Bỏ tick người không đi hôm nay. Sau khi tạo, chỉ sửa số tiền nào đổi hoặc thêm khoản mới.`;
}

async function openNewSessionModal(sourceSessionId) {
  document.getElementById("modal-session-title").textContent = "Tạo buổi đánh mới";
  document.getElementById("session-edit-id").value = "";
  const { today, title } = todaySessionTitle();
  document.getElementById("input-session-date").value = today;
  document.getElementById("input-session-title").value = title;

  let source = null;
  try {
    if (sourceSessionId) {
      source = await api(`/api/sessions/${sourceSessionId}`);
    } else {
      const marked = state.sessions.find((s) => Number(s.is_template) === 1);
      if (marked) source = await api(`/api/sessions/${marked.id}`);
    }
  } catch (err) {
    showToast(err.message);
    source = null;
  }

  showTemplateChoice(source);
  if (source) applyTemplateSource(source);
  else applyBlankSessionDefaults();

  renderSessionParticipantChips();
  renderSessionCouplePairs();
  openModal("modal-session");
}

window.cloneSessionFrom = function (sessionId) {
  openNewSessionModal(sessionId);
};

window.toggleSessionTemplate = async function (sessionId, makeTemplate) {
  try {
    await api(`/api/sessions/${sessionId}/template`, {
      method: "PUT",
      body: JSON.stringify({ is_template: Boolean(makeTemplate) }),
    });
    await loadSessions();
    if (state.current) {
      const fresh = state.sessions.find((s) => s.id === state.current.session.id);
      if (fresh) state.current.session.is_template = fresh.is_template;
      renderCurrentSession();
    }
    showToast(makeTemplate ? "Đã đặt buổi này làm mẫu mặc định." : "Đã bỏ mẫu mặc định.");
  } catch (err) {
    showToast(err.message);
  }
};

function openEditSessionModal() {
  if (!state.current) return;
  const { session, participants } = state.current;
  document.getElementById("modal-session-title").textContent = "Sửa thông tin buổi đánh";
  document.getElementById("session-edit-id").value = session.id;
  document.getElementById("session-template-box").classList.add("hidden");
  document.getElementById("input-use-template").checked = false;
  document.getElementById("session-template-id").value = "";
  document.getElementById("input-session-title").value = session.title;
  document.getElementById("input-session-date").value = session.played_at;
  document.getElementById("input-session-parking").value = session.parking_fee;
  document.getElementById("input-session-notes").value = session.notes || "";

  state.sessionParticipantIds = new Set(participants.map((p) => p.id));
  state.sessionCouplePairs = new Map();
  participants.forEach((p) => {
    if (p.payer_member_id && p.payer_member_id !== p.id) {
      state.sessionCouplePairs.set(p.id, p.payer_member_id);
    }
  });

  renderSessionParticipantChips();
  renderSessionCouplePairs();
  openModal("modal-session");
}

function renderSessionParticipantChips() {
  const wrap = document.getElementById("session-participants-chips");
  if (!state.members.length) {
    wrap.innerHTML = `<span class="muted small">Chưa có thành viên nào. Hãy thêm nhanh tên thành viên ở ô bên dưới!</span>`;
    return;
  }
  wrap.innerHTML = state.members
    .map((m) => {
      const sel = state.sessionParticipantIds.has(m.id);
      return `<button type="button" class="chip ${sel ? "selected" : ""}" onclick="toggleSessionParticipant(${m.id})">${escapeHtml(
        m.name
      )}</button>`;
    })
    .join("");
}

window.toggleSessionParticipant = function (id) {
  if (state.sessionParticipantIds.has(id)) {
    state.sessionParticipantIds.delete(id);
    state.sessionCouplePairs.delete(id);
    for (const [mid, pid] of state.sessionCouplePairs.entries()) {
      if (pid === id) state.sessionCouplePairs.delete(mid);
    }
  } else {
    state.sessionParticipantIds.add(id);
    const m = state.members.find((x) => x.id === id);
    if (m && m.default_payer_id && state.sessionParticipantIds.has(m.default_payer_id)) {
      state.sessionCouplePairs.set(id, m.default_payer_id);
    }
  }
  renderSessionParticipantChips();
  renderSessionCouplePairs();
};

function renderSessionCouplePairs() {
  const wrap = document.getElementById("session-couple-pairs-list");
  if (!wrap) return;
  const pairs = Array.from(state.sessionCouplePairs.entries());
  if (!pairs.length) {
    wrap.innerHTML = `<span class="muted small">Chưa ghép ai. Bấm <strong>+ Thêm ghép cặp</strong> nếu có người trả chung tiền (bạn bè, cặp đôi, đi chung xe).</span>`;
    return;
  }
  wrap.innerHTML = pairs
    .map(([memberId, payerId]) => {
      const mName = state.members.find((m) => m.id === memberId)?.name || `TV #${memberId}`;
      const pName = state.members.find((m) => m.id === payerId)?.name || `TV #${payerId}`;
      return `
        <div class="couple-pair-item">
          <div class="couple-pair-names">
            <span class="couple-tag">${ICONS.linked} ${escapeHtml(mName)}</span>
            <span class="muted small">được</span>
            <span class="couple-tag-payer">${escapeHtml(pName)}</span>
            <span class="muted small">trả chung</span>
          </div>
          <button type="button" class="btn btn-ghost btn-xs text-danger" onclick="removeSessionCouplePair(${memberId})">✕ Bỏ</button>
        </div>
      `;
    })
    .join("");
}

window.removeSessionCouplePair = function (memberId) {
  state.sessionCouplePairs.delete(memberId);
  renderSessionCouplePairs();
};

function showAddCouplePairRow() {
  const wrap = document.getElementById("session-couple-pairs-list");
  if (!wrap) return;
  const selected = state.members.filter((m) => state.sessionParticipantIds.has(m.id));
  if (selected.length < 2) {
    showToast("Cần ít nhất 2 thành viên tham gia để ghép cặp.");
    return;
  }
  if (document.getElementById("couple-select-member")) return;

  const availableMembers = selected.filter((m) => !state.sessionCouplePairs.has(m.id));
  if (!availableMembers.length) {
    showToast("Tất cả thành viên tham gia đã được ghép cặp.");
    return;
  }

  const row = document.createElement("div");
  row.className = "couple-pair-edit-row";
  row.innerHTML = `
    <select id="couple-select-member" class="form-select-sm">
      <option value="">-- Người được trả thay --</option>
      ${availableMembers.map((m) => `<option value="${m.id}">${escapeHtml(m.name)}</option>`).join("")}
    </select>
    <span class="muted small">được</span>
    <select id="couple-select-payer" class="form-select-sm">
      <option value="">-- Người trả chung --</option>
      ${selected.map((m) => `<option value="${m.id}">${escapeHtml(m.name)}</option>`).join("")}
    </select>
    <button type="button" class="btn btn-primary btn-xs" id="btn-confirm-couple-pair">✓ Ghép</button>
    <button type="button" class="btn btn-secondary btn-xs" id="btn-cancel-couple-pair">✕</button>
  `;
  wrap.appendChild(row);

  row.querySelector("#btn-confirm-couple-pair").onclick = () => {
    const mId = Number(row.querySelector("#couple-select-member").value);
    const pId = Number(row.querySelector("#couple-select-payer").value);
    if (!mId || !pId) {
      showToast("Vui lòng chọn cả 2 người trong cặp.");
      return;
    }
    if (mId === pId) {
      showToast("Người trả chung phải khác người được trả.");
      return;
    }
    state.sessionCouplePairs.set(mId, pId);
    renderSessionCouplePairs();
  };

  row.querySelector("#btn-cancel-couple-pair").onclick = () => {
    renderSessionCouplePairs();
  };
}

async function submitSessionForm(e) {
  e.preventDefault();
  const editId = document.getElementById("session-edit-id").value;
  const payload = {
    title: document.getElementById("input-session-title").value.trim(),
    played_at: document.getElementById("input-session-date").value,
    parking_fee: readMoneyInput("input-session-parking", 5000),
    notes: document.getElementById("input-session-notes").value.trim(),
    participant_ids: Array.from(state.sessionParticipantIds),
    participant_payers: Object.fromEntries(state.sessionCouplePairs),
  };
  if (!editId) {
    const useTemplate = document.getElementById("input-use-template").checked;
    const templateId = Number(document.getElementById("session-template-id").value);
    payload.template_session_id = useTemplate && templateId ? templateId : null;
  }
  if (payload.participant_ids.length === 0) {
    showToast("Hãy chọn ít nhất 1 thành viên tham gia buổi đánh.");
    return;
  }
  try {
    const res = editId
      ? await api(`/api/sessions/${editId}`, { method: "PUT", body: JSON.stringify(payload) })
      : await api("/api/sessions", { method: "POST", body: JSON.stringify(payload) });
    state.current = res;
    closeModal("modal-session");
    await loadSessions();
    renderCurrentSession();
    switchTab("session");
    const copied = !editId && payload.template_session_id;
    showToast(editId ? "Đã cập nhật buổi đánh." : copied ? "Đã tạo buổi mới từ mẫu. Sửa số tiền nào đổi, hoặc thêm khoản mới." : "Đã tạo buổi đánh mới.");
  } catch (err) {
    showToast(err.message);
  }
}

window.deleteSession = async function (id) {
  if (!confirm("Bạn chắc chắn muốn xóa buổi đánh này?")) return;
  try {
    await api(`/api/sessions/${id}`, { method: "DELETE" });
    if (state.current && state.current.session.id === id) {
      state.current = null;
    }
    await loadSessions();
    if (!state.current && state.sessions.length > 0) {
      await openSession(state.sessions[0].id);
    } else {
      renderCurrentSession();
    }
    showToast("Đã xóa buổi đánh.");
  } catch (err) {
    showToast(err.message);
  }
};

// ---------- Expense Modal ----------

function populatePayerSelect(selectedId = null) {
  const sel = document.getElementById("input-expense-payer");
  const participants = state.current ? state.current.participants : [];
  sel.innerHTML = participants
    .map(
      (p) =>
        `<option value="${p.id}" ${Number(selectedId) === p.id ? "selected" : ""}>${escapeHtml(p.name)}</option>`
    )
    .join("");
}

function openQuickExpense(category) {
  if (!state.current) return;
  const meta = CAT_META[category] || CAT_META.other;
  const participants = state.current.participants;
  const allIds = participants.map((p) => p.id);

  document.getElementById("modal-expense-title").innerHTML = `${meta.iconSvg} <span>Thêm ${escapeHtml(meta.label)}</span>`;
  document.getElementById("expense-edit-id").value = "";
  document.getElementById("expense-category").value = category;
  document.getElementById("expense-split-type").value = meta.defaultSplit;
  document.getElementById("input-expense-title").value = meta.label;
  populatePayerSelect(participants[0]?.id);

  configureExpenseModalBlocks(meta.defaultSplit);

  if (meta.defaultSplit === "equal_split") {
    document.getElementById("input-expense-total").value = "";
    state.expenseDraft.equalIds = new Set(allIds);
    renderEqualChips();
  } else if (meta.defaultSplit === "parking") {
    document.querySelector('input[name="parking_mode"][value="separate_payer"]').checked = true;
    document.getElementById("input-parking-unit").value = moneyOrFallback(state.current.session.parking_fee, 5000);
    state.expenseDraft.parkingIds = new Set(allIds);
    updateParkingModeVisibility();
    renderParkingChips();
  } else if (meta.defaultSplit === "itemized") {
    state.expenseDraft.items = [
      {
        item_name: category === "snack" ? "Bánh loại 1" : "Cà phê / Nước",
        amount: "",
        pricing_mode: "per_person",
        participant_ids: new Set(),
      },
    ];
    renderItemizedRows();
  }

  openModal("modal-expense");
}

window.openEditExpense = function (expenseId) {
  if (!state.current) return;
  const exp = state.current.expenses.find((e) => e.id === expenseId);
  if (!exp) return;

  const meta = CAT_META[exp.category] || CAT_META.other;
  document.getElementById("modal-expense-title").innerHTML = `${meta.iconSvg} <span>Sửa ${escapeHtml(exp.title)}</span>`;
  document.getElementById("expense-edit-id").value = exp.id;
  document.getElementById("expense-category").value = exp.category;
  document.getElementById("expense-split-type").value = exp.split_type;
  document.getElementById("input-expense-title").value = exp.title;
  populatePayerSelect(exp.payer_id);

  configureExpenseModalBlocks(exp.split_type);

  if (exp.split_type === "equal_split") {
    document.getElementById("input-expense-total").value = exp.total_amount;
    state.expenseDraft.equalIds = new Set(exp.participant_ids);
    renderEqualChips();
  } else if (exp.split_type === "parking") {
    const mode = exp.parking_mode || "separate_payer";
    document.querySelector(`input[name="parking_mode"][value="${mode}"]`).checked = true;
    document.getElementById("input-parking-unit").value = moneyOrFallback(exp.unit_fee, 5000);
    state.expenseDraft.parkingIds = new Set(exp.participant_ids);
    updateParkingModeVisibility();
    renderParkingChips();
  } else if (exp.split_type === "itemized") {
    state.expenseDraft.items = (exp.items || []).map((it) => ({
      item_name: it.item_name,
      amount: it.amount,
      pricing_mode: it.pricing_mode || "per_person",
      participant_ids: new Set(it.participant_ids),
    }));
    if (state.expenseDraft.items.length === 0) {
      state.expenseDraft.items.push({
        item_name: "",
        amount: "",
        pricing_mode: "per_person",
        participant_ids: new Set(),
      });
    }
    renderItemizedRows();
  }

  openModal("modal-expense");
};

function configureExpenseModalBlocks(splitType) {
  document.getElementById("block-equal-split").classList.toggle("hidden", splitType !== "equal_split");
  document.getElementById("block-parking").classList.toggle("hidden", splitType !== "parking");
  document.getElementById("block-itemized").classList.toggle("hidden", splitType !== "itemized");
  document.getElementById("group-expense-payer").classList.remove("hidden");
}

function updateParkingModeVisibility() {
  const mode = document.querySelector('input[name="parking_mode"]:checked')?.value;
  document
    .getElementById("group-expense-payer")
    .classList.toggle("hidden", mode === "included_in_court");
  updateParkingPreview();
}

function updateParkingPreview() {
  const raw = document.getElementById("input-parking-unit").value;
  const unit = String(raw).trim() === "" ? 5000 : Math.max(0, Math.round(Number(raw)) || 0);
  const count = state.expenseDraft.parkingIds.size;
  const mode = document.querySelector('input[name="parking_mode"]:checked')?.value;
  const total = unit * count;
  const el = document.getElementById("parking-preview");
  el.textContent =
    mode === "included_in_court"
      ? `Tổng tách từ hóa đơn sân: ${vnd(unit)} × ${count} người = ${vnd(total)}`
      : `Tổng người trả hộ đã ứng: ${vnd(unit)} × ${count} người = ${vnd(total)}`;
}

function renderEqualChips() {
  const wrap = document.getElementById("equal-participants-chips");
  const participants = state.current?.participants || [];
  wrap.innerHTML = participants
    .map((p) => {
      const sel = state.expenseDraft.equalIds.has(p.id);
      return `<button type="button" class="chip ${sel ? "selected" : ""}" onclick="toggleEqualChip(${p.id})">${escapeHtml(
        p.name
      )}</button>`;
    })
    .join("");
}

window.toggleEqualChip = function (id) {
  if (state.expenseDraft.equalIds.has(id)) state.expenseDraft.equalIds.delete(id);
  else state.expenseDraft.equalIds.add(id);
  renderEqualChips();
};

function renderParkingChips() {
  const wrap = document.getElementById("parking-participants-chips");
  const participants = state.current?.participants || [];
  wrap.innerHTML = participants
    .map((p) => {
      const sel = state.expenseDraft.parkingIds.has(p.id);
      return `<button type="button" class="chip ${sel ? "selected" : ""}" onclick="toggleParkingChip(${p.id})">${escapeHtml(
        p.name
      )}</button>`;
    })
    .join("");
  updateParkingPreview();
}

window.toggleParkingChip = function (id) {
  if (state.expenseDraft.parkingIds.has(id)) state.expenseDraft.parkingIds.delete(id);
  else state.expenseDraft.parkingIds.add(id);
  renderParkingChips();
};

function renderItemizedRows() {
  const wrap = document.getElementById("itemized-rows");
  const participants = state.current?.participants || [];
  let grandTotal = 0;

  wrap.innerHTML = state.expenseDraft.items
    .map((item, idx) => {
      const amt = Number(item.amount) || 0;
      const cnt = item.participant_ids.size;
      const sub = cnt === 0 ? 0 : item.pricing_mode === "per_person" ? amt * cnt : amt;
      grandTotal += sub;

      const chipsHtml = participants
        .map((p) => {
          const sel = item.participant_ids.has(p.id);
          return `<button type="button" class="chip ${sel ? "selected" : ""}" onclick="toggleItemChip(${idx}, ${p.id})">${escapeHtml(
            p.name
          )}</button>`;
        })
        .join("");

      const calcText =
        cnt === 0
          ? "Chưa chọn người"
          : item.pricing_mode === "per_person"
          ? `${vnd(amt)}/người × ${cnt} người = ${vnd(sub)}`
          : `Chia đều ${vnd(amt)} / ${cnt} người ≈ ${vnd(Math.round(amt / cnt))}/người`;

      return `
        <div class="item-row-card">
          <div class="item-row-top">
            <input type="text" value="${escapeHtml(item.item_name)}" placeholder="Tên món (VD: Bánh mì, Bạc xỉu)" oninput="updateItemField(${idx}, 'item_name', this.value)" />
            <input type="number" min="0" step="1000" value="${item.amount}" placeholder="Giá (VNĐ)" oninput="updateItemField(${idx}, 'amount', this.value)" />
            <button type="button" class="btn btn-danger btn-sm" onclick="removeItemRow(${idx})" title="Xóa dòng">&times;</button>
          </div>
          <div class="mode-toggle">
            <button type="button" class="mode-btn ${item.pricing_mode === "per_person" ? "active" : ""}" onclick="setItemMode(${idx}, 'per_person')">Đơn giá / người</button>
            <button type="button" class="mode-btn ${item.pricing_mode === "split_total" ? "active" : ""}" onclick="setItemMode(${idx}, 'split_total')">Chia đều tổng</button>
          </div>
          <div class="chip-container">${chipsHtml}</div>
          <div class="item-row-foot">
            <span>${calcText}</span>
            <strong>${vnd(sub)}</strong>
          </div>
        </div>
      `;
    })
    .join("");

  document.getElementById("itemized-grand-total").textContent = vnd(grandTotal);
}

window.updateItemField = function (idx, field, val) {
  state.expenseDraft.items[idx][field] = field === "amount" ? (val === "" ? "" : Number(val)) : val;
  if (field === "amount") {
    // Recompute totals smoothly without losing input focus
    let grandTotal = 0;
    const cards = document.querySelectorAll(".item-row-card");
    state.expenseDraft.items.forEach((item, i) => {
      const amt = Number(item.amount) || 0;
      const cnt = item.participant_ids.size;
      const sub = cnt === 0 ? 0 : item.pricing_mode === "per_person" ? amt * cnt : amt;
      grandTotal += sub;
      const foot = cards[i]?.querySelector(".item-row-foot");
      if (foot) {
        foot.children[0].textContent =
          cnt === 0
            ? "Chưa chọn người"
            : item.pricing_mode === "per_person"
            ? `${vnd(amt)}/người × ${cnt} người = ${vnd(sub)}`
            : `Chia đều ${vnd(amt)} / ${cnt} người ≈ ${vnd(Math.round(amt / cnt))}/người`;
        foot.children[1].textContent = vnd(sub);
      }
    });
    document.getElementById("itemized-grand-total").textContent = vnd(grandTotal);
  }
};

window.setItemMode = function (idx, mode) {
  state.expenseDraft.items[idx].pricing_mode = mode;
  renderItemizedRows();
};

window.toggleItemChip = function (idx, memberId) {
  const set = state.expenseDraft.items[idx].participant_ids;
  if (set.has(memberId)) set.delete(memberId);
  else set.add(memberId);
  renderItemizedRows();
};

window.removeItemRow = function (idx) {
  if (state.expenseDraft.items.length === 1) {
    state.expenseDraft.items[0] = {
      item_name: "",
      amount: "",
      pricing_mode: "per_person",
      participant_ids: new Set(),
    };
  } else {
    state.expenseDraft.items.splice(idx, 1);
  }
  renderItemizedRows();
};

async function submitExpenseForm(e) {
  e.preventDefault();
  if (!state.current) return;

  const editId = document.getElementById("expense-edit-id").value;
  const category = document.getElementById("expense-category").value;
  const splitType = document.getElementById("expense-split-type").value;
  const title = document.getElementById("input-expense-title").value.trim();
  const payerVal = document.getElementById("input-expense-payer").value;
  let payerId = payerVal ? Number(payerVal) : null;

  const payload = {
    category,
    title,
    split_type: splitType,
    payer_id: payerId,
    total_amount: 0,
    parking_mode: null,
    unit_fee: 5000,
    participant_ids: [],
    items: [],
  };

  if (splitType === "equal_split") {
    payload.total_amount = Number(document.getElementById("input-expense-total").value) || 0;
    payload.participant_ids = Array.from(state.expenseDraft.equalIds);
    if (payload.participant_ids.length === 0) {
      showToast("Hãy chọn ít nhất 1 người chia khoản này.");
      return;
    }
  } else if (splitType === "parking") {
    const mode = document.querySelector('input[name="parking_mode"]:checked')?.value || "separate_payer";
    payload.parking_mode = mode;
    payload.unit_fee = readMoneyInput("input-parking-unit", 5000);
    payload.participant_ids = Array.from(state.expenseDraft.parkingIds);
    if (mode === "included_in_court") {
      payload.payer_id = null;
    }
  } else if (splitType === "itemized") {
    payload.items = state.expenseDraft.items
      .filter((it) => Number(it.amount) > 0 && it.participant_ids.size > 0)
      .map((it) => ({
        item_name: it.item_name.trim() || "Món",
        amount: Number(it.amount),
        pricing_mode: it.pricing_mode,
        participant_ids: Array.from(it.participant_ids),
      }));
    if (payload.items.length === 0) {
      showToast("Hãy nhập giá và tích chọn người cho ít nhất 1 dòng món.");
      return;
    }
  }

  try {
    const sessionId = state.current.session.id;
    state.current = editId
      ? await api(`/api/expenses/${editId}`, { method: "PUT", body: JSON.stringify(payload) })
      : await api(`/api/sessions/${sessionId}/expenses`, { method: "POST", body: JSON.stringify(payload) });
    closeModal("modal-expense");
    renderCurrentSession();
    await loadSessions();
    showToast(editId ? "Đã cập nhật khoản chi." : "Đã thêm khoản chi.");
  } catch (err) {
    showToast(err.message);
  }
}

window.deleteExpense = async function (expenseId) {
  if (!confirm("Xóa khoản chi này?")) return;
  try {
    state.current = await api(`/api/expenses/${expenseId}`, { method: "DELETE" });
    renderCurrentSession();
    await loadSessions();
    showToast("Đã xóa khoản chi.");
  } catch (err) {
    showToast(err.message);
  }
};

// ---------- Settlements, VietQR SVG & Copy Zalo ----------

window.toggleSettlementPaid = async function (settlementId, isPaid) {
  try {
    state.current = await api(`/api/settlements/${settlementId}`, {
      method: "PATCH",
      body: JSON.stringify({ is_paid: isPaid }),
    });
    renderCurrentSession();
    await loadSessions();
    showToast(isPaid ? "Đã đánh dấu hoàn tất chuyển khoản." : "Đã bỏ đánh dấu chuyển khoản.");
  } catch (err) {
    showToast(err.message);
  }
};

window.openQrModal = function (settlementId) {
  if (!state.current) return;
  const s = state.current.settlements.find((x) => x.id === settlementId);
  if (!s) return;
  state.qrTarget = s;

  const sessDate = state.current.session.played_at.split("-").reverse().slice(0, 2).join("/");
  const addInfo = removeVietnameseTones(`Cau long ${sessDate} ${s.from_name} chuyen ${s.to_name}`).slice(0, 50);

  document.getElementById("qr-subtitle").textContent = `${s.from_name} chuyển cho ${s.to_name}`;

  const wrap = document.getElementById("qr-image-wrap");
  if (s.to_bank_id && s.to_account_no) {
    const params = new URLSearchParams({
      amount: String(s.amount),
      addInfo,
      accountName: s.to_account_name || removeVietnameseTones(s.to_name).toUpperCase(),
    });
    const qrUrl = `https://img.vietqr.io/image/${encodeURIComponent(s.to_bank_id)}-${encodeURIComponent(
      s.to_account_no
    )}-compact2.svg?${params.toString()}`;
    wrap.innerHTML = `<img src="${qrUrl}" alt="Mã VietQR chuyển khoản" />`;
  } else {
    wrap.innerHTML = `<p class="muted small" style="padding:18px 8px;">Thành viên <strong>${escapeHtml(
      s.to_name
    )}</strong> chưa cập nhật ngân hàng & số tài khoản. Vào tab <strong>Thành viên</strong> để bổ sung và tự động hiện mã VietQR.</p>`;
  }

  document.getElementById("qr-details").innerHTML = `
    <div><span>Ngân hàng:</span><strong>${escapeHtml(s.to_bank_id || "Chưa có")}</strong></div>
    <div><span>Số tài khoản:</span><strong>${escapeHtml(s.to_account_no || "Chưa có")}</strong></div>
    <div><span>Chủ tài khoản:</span><strong>${escapeHtml(s.to_account_name || s.to_name)}</strong></div>
    <div><span>Số tiền:</span><strong style="color:var(--primary-dark);">${vnd(s.amount)}</strong></div>
    <div><span>Nội dung:</span><strong>${escapeHtml(addInfo)}</strong></div>
  `;

  const btnPaid = document.getElementById("btn-qr-mark-paid");
  btnPaid.textContent = s.is_paid ? "✓ Đã chuyển khoản" : "✓ Đánh dấu đã chuyển";
  btnPaid.disabled = Boolean(s.is_paid);

  openModal("modal-qr");
};

function copyZaloSummary() {
  if (!state.current) return;
  const { session, summary, settlements } = state.current;
  const c = summary.category_totals;

  const lines = [
    `🏸 SMASHPAY · TỔNG KẾT ${session.title.toUpperCase()} (${session.played_at})`,
    `💰 Tổng chi: ${vnd(summary.total_spent)}`,
  ];

  const catParts = [];
  if (c.court) catParts.push(`Sân ${vnd(c.court)}`);
  if (c.shuttle) catParts.push(`Cầu ${vnd(c.shuttle)}`);
  if (c.parking) catParts.push(`Gửi xe ${vnd(c.parking)}`);
  if (c.snack) catParts.push(`Bánh ${vnd(c.snack)}`);
  if (c.drink) catParts.push(`Nước ${vnd(c.drink)}`);
  if (c.other) catParts.push(`Khác ${vnd(c.other)}`);
  if (catParts.length) lines.push(`📌 Chi tiết: ${catParts.join(" · ")}`);

  // Couple / joint payment notes
  const coupleNotes = [];
  summary.member_summaries.forEach((m) => {
    if (m.paid_by_name) {
      coupleNotes.push(`• ${m.name}: ${vnd(m.consumed)} (🔗 ${m.paid_by_name} trả chung)`);
    }
  });
  if (coupleNotes.length) {
    lines.push("", "🔗 THANH TOÁN CHUNG / TRẢ KÈM:");
    lines.push(...coupleNotes);
  }

  lines.push("", "💸 CHUYỂN KHOẢN TỐI ƯU:");
  const leftover = summary.member_summaries.filter((m) => Number(m.net));
  if (!settlements.length && leftover.length) {
    lines.push("• Còn số dư chưa có lệnh chuyển:");
    leftover.forEach((m) => lines.push(`  - ${m.name}: ${formatSigned(m.net)}`));
  } else if (!settlements.length) {
    lines.push("• Mọi người đã cân bằng 0đ.");
  } else {
    settlements.forEach((s) => {
      const tick = s.is_paid ? "✅" : "⏳";
      const bank = s.to_bank_id && s.to_account_no ? ` (${s.to_bank_id} ${s.to_account_no})` : "";
      lines.push(`${tick} ${s.from_name} → ${s.to_name}: ${vnd(s.amount)}${bank}`);
    });
  }

  lines.push("", `🔗 Xem chi tiết & quét mã VietQR: ${window.location.href}`);

  const text = lines.join("\n");
  if (navigator.clipboard?.writeText) {
    navigator.clipboard.writeText(text).then(() => showToast("Đã copy tin nhắn tổng kết gửi Zalo!"));
  } else {
    prompt("Copy tin nhắn bên dưới:", text);
  }
}

// ---------- Members Modal ----------

let isMemberAccNameManual = false;

function populateDefaultPayerSelect(currentMemberId, selectedPayerId) {
  const hidden = document.getElementById("input-member-default-payer");
  if (hidden) hidden.value = selectedPayerId ? String(selectedPayerId) : "";
  renderCustomPayerOptions(currentMemberId, selectedPayerId);
}

window.setCustomPayerValue = function (payerId, payerName = "") {
  const hidden = document.getElementById("input-member-default-payer");
  if (hidden) hidden.value = payerId ? String(payerId) : "";
  const badge = document.getElementById("payer-badge-preview");
  const label = document.getElementById("payer-label-preview");

  if (badge && label) {
    if (payerId && payerName) {
      badge.innerHTML = ICONS.linked;
      badge.className = "payer-trigger-badge active";
      label.textContent = `🔗 ${payerName} trả chung`;
    } else {
      badge.innerHTML = "•";
      badge.className = "payer-trigger-badge";
      label.textContent = "Tự thanh toán riêng (Không ghép)";
    }
  }
  closeAllCustomSelects();
};

function renderCustomPayerOptions(currentMemberId, selectedPayerId) {
  const container = document.getElementById("custom-select-payer-options");
  if (!container) return;

  const available = state.members.filter((m) => m.id !== currentMemberId);
  const selectedNum = selectedPayerId ? Number(selectedPayerId) : null;

  let html = `
    <div class="custom-select-option ${!selectedNum ? "selected" : ""}" onclick="setCustomPayerValue('', '')">
      <div class="option-left">
        <span class="payer-option-avatar none-avatar">•</span>
        <span class="option-name">Tự thanh toán riêng (Không ghép)</span>
      </div>
      ${!selectedNum ? `<span class="option-check">${ICONS.check}</span>` : ""}
    </div>
  `;

  html += available
    .map((m) => {
      const isSelected = selectedNum === m.id;
      return `
        <div class="custom-select-option ${isSelected ? "selected" : ""}" onclick="setCustomPayerValue(${m.id}, '${escapeHtml(m.name)}')">
          <div class="option-left">
            <span class="payer-option-avatar" style="${getAvatarStyle(m.name, m.id)}">${getInitials(m.name)}</span>
            <span class="option-name"><strong>${escapeHtml(m.name)}</strong> trả chung</span>
          </div>
          ${isSelected ? `<span class="option-check">${ICONS.check}</span>` : ""}
        </div>
      `;
    })
    .join("");

  container.innerHTML = html;

  if (selectedNum) {
    const m = state.members.find((x) => x.id === selectedNum);
    setCustomPayerValue(selectedNum, m ? m.name : `TV #${selectedNum}`);
  } else {
    setCustomPayerValue("", "");
  }
}

function openAddMemberModal() {
  document.getElementById("modal-member-title").textContent = "Thêm thành viên mới";
  document.getElementById("member-edit-id").value = "";
  document.getElementById("input-member-name").value = "";
  setCustomBankValue("");
  document.getElementById("input-member-accno").value = "";
  document.getElementById("input-member-accname").value = "";
  document.getElementById("input-member-regular").checked = true;
  isMemberAccNameManual = false;
  populateDefaultPayerSelect(0, null);
  openModal("modal-member");
}

window.openEditMember = function (memberId) {
  const m = state.members.find((x) => x.id === memberId);
  if (!m) return;
  document.getElementById("modal-member-title").textContent = "Sửa thông tin thành viên";
  document.getElementById("member-edit-id").value = m.id;
  document.getElementById("input-member-name").value = m.name;
  setCustomBankValue(m.bank_id || "");
  document.getElementById("input-member-accno").value = m.account_no || "";
  document.getElementById("input-member-accname").value = toVietnameseUpperNoTones(m.account_name || "");
  document.getElementById("input-member-regular").checked = Boolean(m.is_regular);
  isMemberAccNameManual = Boolean(m.account_name);
  populateDefaultPayerSelect(m.id, m.default_payer_id);
  openModal("modal-member");
};

async function submitMemberForm(e) {
  e.preventDefault();
  const editId = document.getElementById("member-edit-id").value;
  const defPayerVal = document.getElementById("input-member-default-payer")?.value;
  const payload = {
    name: document.getElementById("input-member-name").value.trim(),
    bank_id: document.getElementById("input-member-bank").value,
    account_no: document.getElementById("input-member-accno").value.trim(),
    account_name: toVietnameseUpperNoTones(document.getElementById("input-member-accname").value).trim(),
    is_regular: document.getElementById("input-member-regular").checked,
    default_payer_id: defPayerVal ? Number(defPayerVal) : null,
  };
  try {
    if (editId) {
      await api(`/api/members/${editId}`, { method: "PUT", body: JSON.stringify(payload) });
    } else {
      await api("/api/members", { method: "POST", body: JSON.stringify(payload) });
    }
    closeModal("modal-member");
    await loadMembers();
    if (state.current) {
      await openSession(state.current.session.id);
    }
    showToast(editId ? "Đã cập nhật thành viên." : "Đã thêm thành viên.");
  } catch (err) {
    showToast(err.message);
  }
}

window.deleteMember = async function (memberId) {
  if (!confirm("Ẩn thành viên này khỏi danh sách? Họ nằm ở mục Đã ẩn và có thể hiện lại. Buổi đánh cũ vẫn giữ nguyên.")) return;
  try {
    await api(`/api/members/${memberId}`, { method: "DELETE" });
    await loadMembers();
    showToast("Đã ẩn thành viên.");
  } catch (err) {
    showToast(err.message);
  }
};

window.restoreMember = async function (memberId) {
  try {
    await api(`/api/members/${memberId}/restore`, { method: "POST", body: "{}" });
    await loadMembers();
    showToast("Đã hiện lại thành viên.");
  } catch (err) {
    showToast(err.message);
  }
};

// ---------- Event Binding ----------

function bindEvents() {
  document.querySelectorAll(".nav-tab").forEach((btn) => {
    btn.addEventListener("click", () => switchTab(btn.dataset.tab));
  });

  document.querySelectorAll("[data-close-modal]").forEach((btn) => {
    btn.addEventListener("click", () => closeModal(btn.dataset.closeModal));
  });

  document.querySelectorAll(".modal-backdrop").forEach((bd) => {
    bd.addEventListener("click", (e) => {
      if (e.target === bd) bd.classList.add("hidden");
    });
  });

  document.getElementById("btn-empty-new-session").addEventListener("click", () => openNewSessionModal());
  document.getElementById("btn-new-session-top").addEventListener("click", () => openNewSessionModal());
  document.getElementById("btn-history-new-session").addEventListener("click", () => openNewSessionModal());
  document.getElementById("btn-clone-session").addEventListener("click", () => {
    if (state.current) openNewSessionModal(state.current.session.id);
  });
  document.getElementById("btn-toggle-template").addEventListener("click", () => {
    if (!state.current) return;
    const on = Number(state.current.session.is_template) === 1;
    toggleSessionTemplate(state.current.session.id, !on);
  });
  document.getElementById("btn-edit-session").addEventListener("click", openEditSessionModal);
  document.getElementById("input-use-template").addEventListener("change", (e) => {
    if (e.target.checked && state.templateSource) applyTemplateSource(state.templateSource);
    else if (!e.target.checked) applyBlankSessionDefaults();
    renderSessionParticipantChips();
    renderSessionCouplePairs();
  });
  document.getElementById("btn-goto-members").addEventListener("click", () => switchTab("members"));
  document.getElementById("btn-add-member").addEventListener("click", openAddMemberModal);
  document.getElementById("btn-copy-zalo").addEventListener("click", copyZaloSummary);

  const btnAddCouple = document.getElementById("btn-add-session-couple");
  if (btnAddCouple) {
    btnAddCouple.addEventListener("click", showAddCouplePairRow);
  }

  const formCoupleLink = document.getElementById("form-couple-link");
  if (formCoupleLink) {
    formCoupleLink.addEventListener("submit", async (e) => {
      e.preventDefault();
      const mId = Number(document.getElementById("couple-link-member-id").value);
      const payerVal = document.getElementById("select-couple-payer").value;
      const payerId = payerVal ? Number(payerVal) : null;
      try {
        state.current = await api(`/api/sessions/${state.current.session.id}/participants/${mId}/payer`, {
          method: "PUT",
          body: JSON.stringify({ payer_member_id: payerId }),
        });
        closeModal("modal-couple-link");
        renderCurrentSession();
        showToast("Đã cập nhật ghép cặp trả chung.");
      } catch (err) {
        showToast(err.message);
      }
    });
  }

  document.querySelectorAll("[data-quick-cat]").forEach((btn) => {
    btn.addEventListener("click", () => openQuickExpense(btn.dataset.quickCat));
  });

  document.getElementById("btn-session-select-all").addEventListener("click", () => {
    state.members.forEach((m) => state.sessionParticipantIds.add(m.id));
    renderSessionParticipantChips();
    renderSessionCouplePairs();
  });

  document.getElementById("btn-add-quick-guest").addEventListener("click", async () => {
    const input = document.getElementById("input-quick-guest");
    const name = input.value.trim();
    if (!name) return;
    try {
      const m = await api("/api/members", {
        method: "POST",
        body: JSON.stringify({ name, is_regular: false }),
      });
      input.value = "";
      await loadMembers();
      state.sessionParticipantIds.add(m.id);
      renderSessionParticipantChips();
      renderSessionCouplePairs();
      showToast(`Đã thêm ${m.name}`);
    } catch (err) {
      showToast(err.message);
    }
  });

  document.getElementById("btn-equal-all").addEventListener("click", () => {
    (state.current?.participants || []).forEach((p) => state.expenseDraft.equalIds.add(p.id));
    renderEqualChips();
  });
  document.getElementById("btn-equal-none").addEventListener("click", () => {
    state.expenseDraft.equalIds.clear();
    renderEqualChips();
  });

  document.getElementById("btn-parking-all").addEventListener("click", () => {
    (state.current?.participants || []).forEach((p) => state.expenseDraft.parkingIds.add(p.id));
    renderParkingChips();
  });
  document.getElementById("btn-parking-none").addEventListener("click", () => {
    state.expenseDraft.parkingIds.clear();
    renderParkingChips();
  });

  document.querySelectorAll('input[name="parking_mode"]').forEach((r) => {
    r.addEventListener("change", updateParkingModeVisibility);
  });
  document.getElementById("input-parking-unit").addEventListener("input", updateParkingPreview);

  document.getElementById("btn-add-item-row").addEventListener("click", () => {
    state.expenseDraft.items.push({
      item_name: "",
      amount: "",
      pricing_mode: "per_person",
      participant_ids: new Set(),
    });
    renderItemizedRows();
  });

  document.getElementById("form-session").addEventListener("submit", submitSessionForm);
  document.getElementById("form-expense").addEventListener("submit", submitExpenseForm);
  document.getElementById("form-member").addEventListener("submit", submitMemberForm);

  const inputMemberName = document.getElementById("input-member-name");
  const inputMemberAccName = document.getElementById("input-member-accname");

  if (inputMemberName && inputMemberAccName) {
    inputMemberName.addEventListener("input", () => {
      if (!isMemberAccNameManual) {
        inputMemberAccName.value = toVietnameseUpperNoTones(inputMemberName.value);
      }
    });

    inputMemberAccName.addEventListener("input", () => {
      if (inputMemberAccName.value.trim() === "") {
        isMemberAccNameManual = false;
      } else {
        isMemberAccNameManual = true;
      }
      inputMemberAccName.value = toVietnameseUpperNoTones(inputMemberAccName.value);
    });
  }

  document.getElementById("btn-copy-stk").addEventListener("click", () => {
    const stk = state.qrTarget?.to_account_no;
    if (!stk) {
      showToast("Chưa có số tài khoản để copy.");
      return;
    }
    navigator.clipboard?.writeText(stk).then(() => showToast(`Đã copy STK: ${stk}`));
  });

  document.getElementById("btn-qr-mark-paid").addEventListener("click", async () => {
    if (!state.qrTarget) return;
    await toggleSettlementPaid(state.qrTarget.id, true);
    closeModal("modal-qr");
  });
}

// =========================================
// SCOREBOARD LOGIC (BẢNG ĐIỂM THI ĐẤU CẦU LÔNG)
// =========================================

const scoreState = {
  teamA: { name: "Đội A", score: 0, sets: 0 },
  teamB: { name: "Đội B", score: 0, sets: 0 },
  currentSet: 1,
  targetSets: 3, // Bo3
  maxPoints: 21,
  serving: "A", // 'A' or 'B'
  history: [],
  isSwapped: false,
  isFullscreen: false,
};

function initScoreboard() {
  const sideA = document.getElementById("sb-side-a");
  const sideB = document.getElementById("sb-side-b");
  const btnUndo = document.getElementById("btn-sb-undo");
  const btnSwap = document.getElementById("btn-sb-swap");
  const btnNewSet = document.getElementById("btn-sb-new-set");
  const btnReset = document.getElementById("btn-sb-reset");
  const btnFullscreen = document.getElementById("btn-sb-fullscreen");
  const btnSettings = document.getElementById("btn-sb-settings");
  const formSettings = document.getElementById("form-scoreboard-settings");

  if (!sideA || !sideB) return;

  sideA.addEventListener("click", () => addScore("A"));
  sideB.addEventListener("click", () => addScore("B"));

  if (btnUndo) btnUndo.addEventListener("click", undoScore);
  if (btnSwap) btnSwap.addEventListener("click", swapSides);
  if (btnNewSet) btnNewSet.addEventListener("click", () => {
    if (confirm("Bắt đầu ván đấu mới? (Điểm số hiện tại sẽ về 0-0, số ván thắng được giữ nguyên)")) {
      resetSet();
    }
  });
  if (btnReset) btnReset.addEventListener("click", () => {
    if (confirm("Tạo lại trận đấu mới từ đầu? (Tất cả điểm số và ván thắng sẽ về 0-0)")) {
      resetMatch();
    }
  });
  if (btnFullscreen) btnFullscreen.addEventListener("click", toggleScoreboardFullscreen);
  if (btnSettings) btnSettings.addEventListener("click", openScoreboardSettings);
  if (formSettings) formSettings.addEventListener("submit", submitScoreboardSettings);

  // First serve radio toggle styles in settings modal
  document.querySelectorAll('input[name="first_serve"]').forEach((r) => {
    r.addEventListener("change", (e) => {
      document.getElementById("label-first-serve-a")?.classList.toggle("active", e.target.value === "A");
      document.getElementById("label-first-serve-b")?.classList.toggle("active", e.target.value === "B");
    });
  });

  renderScoreboard();
}

function renderScoreboard() {
  const scoreAEl = document.getElementById("sb-score-a");
  const scoreBEl = document.getElementById("sb-score-b");
  const nameAEl = document.getElementById("sb-team-a-name");
  const nameBEl = document.getElementById("sb-team-b-name");
  const setsAEl = document.getElementById("sb-sets-a");
  const setsBEl = document.getElementById("sb-sets-b");
  const setsRatioEl = document.getElementById("sb-sets-ratio");
  const setBadgeEl = document.getElementById("sb-set-badge");
  const sideAEl = document.getElementById("sb-side-a");
  const sideBEl = document.getElementById("sb-side-b");
  const serveBadgeA = document.getElementById("sb-serve-badge-a");
  const serveBadgeB = document.getElementById("sb-serve-badge-b");
  const courtTextEl = document.getElementById("sb-service-court-text");
  const pointBannerEl = document.getElementById("sb-point-banner");

  if (!scoreAEl || !scoreBEl) return;

  scoreAEl.textContent = String(scoreState.teamA.score);
  scoreBEl.textContent = String(scoreState.teamB.score);
  if (nameAEl) nameAEl.textContent = scoreState.teamA.name;
  if (nameBEl) nameBEl.textContent = scoreState.teamB.name;
  if (setsAEl) setsAEl.innerHTML = `Ván thắng: <strong>${scoreState.teamA.sets}</strong>`;
  if (setsBEl) setsBEl.innerHTML = `Ván thắng: <strong>${scoreState.teamB.sets}</strong>`;
  if (setsRatioEl) setsRatioEl.textContent = `${scoreState.teamA.sets} - ${scoreState.teamB.sets}`;
  if (setBadgeEl) setBadgeEl.textContent = `Ván ${scoreState.currentSet}`;

  // Serving side styling
  const isAServing = scoreState.serving === "A";
  if (sideAEl) sideAEl.classList.toggle("is-serving", isAServing);
  if (sideBEl) sideBEl.classList.toggle("is-serving", !isAServing);
  if (serveBadgeA) serveBadgeA.classList.toggle("hidden", !isAServing);
  if (serveBadgeB) serveBadgeB.classList.toggle("hidden", isAServing);

  // BWF Service court: even = right court, odd = left court
  const currentServeScore = isAServing ? scoreState.teamA.score : scoreState.teamB.score;
  const isRightCourt = currentServeScore % 2 === 0;
  if (courtTextEl) {
    courtTextEl.textContent = isRightCourt ? "Ô phải (Chẵn)" : "Ô trái (Lẻ)";
  }

  // Game Point / Match Point check
  const neededSetsToWin = Math.ceil(scoreState.targetSets / 2);
  const aCanWinMatch = scoreState.teamA.sets === neededSetsToWin - 1;
  const bCanWinMatch = scoreState.teamB.sets === neededSetsToWin - 1;

  const aIsGamePoint = isPointPotentialWin(scoreState.teamA.score, scoreState.teamB.score, scoreState.maxPoints);
  const bIsGamePoint = isPointPotentialWin(scoreState.teamB.score, scoreState.teamA.score, scoreState.maxPoints);

  if (pointBannerEl) {
    if (aIsGamePoint && aCanWinMatch) {
      pointBannerEl.textContent = `MATCH POINT - ${scoreState.teamA.name.toUpperCase()}`;
      pointBannerEl.classList.remove("hidden");
    } else if (bIsGamePoint && bCanWinMatch) {
      pointBannerEl.textContent = `MATCH POINT - ${scoreState.teamB.name.toUpperCase()}`;
      pointBannerEl.classList.remove("hidden");
    } else if (aIsGamePoint) {
      pointBannerEl.textContent = `SET POINT - ${scoreState.teamA.name.toUpperCase()}`;
      pointBannerEl.classList.remove("hidden");
    } else if (bIsGamePoint) {
      pointBannerEl.textContent = `SET POINT - ${scoreState.teamB.name.toUpperCase()}`;
      pointBannerEl.classList.remove("hidden");
    } else {
      pointBannerEl.classList.add("hidden");
    }
  }
}

function isPointPotentialWin(leaderScore, followerScore, maxPoints) {
  if (leaderScore >= maxPoints - 1 && leaderScore > followerScore) {
    if (leaderScore >= 20 && followerScore >= 20) {
      return leaderScore - followerScore === 1 || leaderScore === 29;
    }
    return true;
  }
  return false;
}

function addScore(side) {
  // Push state to history for undo
  scoreState.history.push({
    teamA: { ...scoreState.teamA },
    teamB: { ...scoreState.teamB },
    currentSet: scoreState.currentSet,
    serving: scoreState.serving,
  });

  if (side === "A") {
    scoreState.teamA.score++;
    scoreState.serving = "A";
  } else {
    scoreState.teamB.score++;
    scoreState.serving = "B";
  }

  if (navigator.vibrate) {
    navigator.vibrate(30);
  }

  // Check Set Win
  checkSetWinner();
  renderScoreboard();
}

function checkSetWinner() {
  const sA = scoreState.teamA.score;
  const sB = scoreState.teamB.score;
  const max = scoreState.maxPoints;
  let winner = null;

  // Win condition: reach maxPoints and lead by >= 2, or reach hard cap 30
  if ((sA >= max && sA - sB >= 2) || sA >= 30) {
    winner = "A";
  } else if ((sB >= max && sB - sA >= 2) || sB >= 30) {
    winner = "B";
  }

  if (winner) {
    const winningName = winner === "A" ? scoreState.teamA.name : scoreState.teamB.name;
    const finalScore = `${sA} - ${sB}`;
    if (winner === "A") scoreState.teamA.sets++;
    else scoreState.teamB.sets++;

    const neededSetsToWin = Math.ceil(scoreState.targetSets / 2);
    const matchWinner =
      scoreState.teamA.sets >= neededSetsToWin
        ? scoreState.teamA.name
        : scoreState.teamB.sets >= neededSetsToWin
        ? scoreState.teamB.name
        : null;

    if (matchWinner) {
      setTimeout(() => {
        alert(`🏆 CHÚC MỪNG!\n\n${matchWinner} đã THẮNG CHUNG CUỘC với tỷ số ván ${scoreState.teamA.sets} - ${scoreState.teamB.sets}!`);
      }, 100);
    } else {
      setTimeout(() => {
        if (confirm(`🎉 ${winningName} thắng Ván ${scoreState.currentSet} (${finalScore})!\n\nBắt đầu Ván ${scoreState.currentSet + 1} và đổi sân?`)) {
          swapSides();
          scoreState.currentSet++;
          scoreState.teamA.score = 0;
          scoreState.teamB.score = 0;
          scoreState.serving = winner; // winning team serves first in next game
          renderScoreboard();
        }
      }, 100);
    }
  }
}

function undoScore() {
  if (scoreState.history.length === 0) {
    showToast("Chưa có điểm nào để hoàn tác.");
    return;
  }
  const prev = scoreState.history.pop();
  scoreState.teamA = prev.teamA;
  scoreState.teamB = prev.teamB;
  scoreState.currentSet = prev.currentSet;
  scoreState.serving = prev.serving;
  renderScoreboard();
  showToast("Đã hoàn tác 1 điểm.");
}

function swapSides() {
  scoreState.isSwapped = !scoreState.isSwapped;
  const board = document.getElementById("sb-board-grid");
  const sideA = document.getElementById("sb-side-a");
  const sideB = document.getElementById("sb-side-b");
  if (board && sideA && sideB) {
    if (scoreState.isSwapped) {
      sideA.style.order = "3";
      sideB.style.order = "1";
    } else {
      sideA.style.order = "1";
      sideB.style.order = "3";
    }
  }
  showToast("Đã đổi sân thi đấu ⇄");
}

function resetSet() {
  scoreState.history.push({
    teamA: { ...scoreState.teamA },
    teamB: { ...scoreState.teamB },
    currentSet: scoreState.currentSet,
    serving: scoreState.serving,
  });
  scoreState.teamA.score = 0;
  scoreState.teamB.score = 0;
  renderScoreboard();
  showToast("Đã thiết lập lại ván đấu (0 - 0).");
}

function resetMatch() {
  scoreState.teamA.score = 0;
  scoreState.teamA.sets = 0;
  scoreState.teamB.score = 0;
  scoreState.teamB.sets = 0;
  scoreState.currentSet = 1;
  scoreState.history = [];
  scoreState.serving = "A";
  renderScoreboard();
  showToast("Đã tạo trận đấu mới (0 - 0).");
}

function toggleScoreboardFullscreen() {
  const arena = document.getElementById("scoreboard-arena");
  const label = document.getElementById("sb-fullscreen-label");
  if (!arena) return;

  scoreState.isFullscreen = !scoreState.isFullscreen;
  arena.classList.toggle("scoreboard-fullscreen", scoreState.isFullscreen);

  if (label) {
    label.textContent = scoreState.isFullscreen ? "Thu nhỏ ✕" : "Toàn màn hình ngang";
  }

  // Request native fullscreen API if available
  if (scoreState.isFullscreen) {
    if (document.documentElement.requestFullscreen) {
      document.documentElement.requestFullscreen().catch(() => {});
    }
  } else {
    if (document.exitFullscreen && document.fullscreenElement) {
      document.exitFullscreen().catch(() => {});
    }
  }
}

function openScoreboardSettings() {
  const inputA = document.getElementById("input-sb-team-a");
  const inputB = document.getElementById("input-sb-team-b");
  const selectPts = document.getElementById("select-sb-points");
  const selectSets = document.getElementById("select-sb-sets");

  if (inputA) inputA.value = scoreState.teamA.name;
  if (inputB) inputB.value = scoreState.teamB.name;
  if (selectPts) selectPts.value = String(scoreState.maxPoints);
  if (selectSets) selectSets.value = String(scoreState.targetSets);

  openModal("modal-scoreboard-settings");
}

function submitScoreboardSettings(e) {
  e.preventDefault();
  const inputA = document.getElementById("input-sb-team-a");
  const inputB = document.getElementById("input-sb-team-b");
  const selectPts = document.getElementById("select-sb-points");
  const selectSets = document.getElementById("select-sb-sets");
  const firstServe = document.querySelector('input[name="first_serve"]:checked')?.value || "A";

  if (inputA && inputA.value.trim()) scoreState.teamA.name = inputA.value.trim();
  if (inputB && inputB.value.trim()) scoreState.teamB.name = inputB.value.trim();
  if (selectPts) scoreState.maxPoints = Number(selectPts.value) || 21;
  if (selectSets) scoreState.targetSets = Number(selectSets.value) || 3;
  scoreState.serving = firstServe;

  closeModal("modal-scoreboard-settings");
  renderScoreboard();
  showToast("Đã cập nhật cài đặt trận đấu!");
}

document.addEventListener("DOMContentLoaded", initApp);
