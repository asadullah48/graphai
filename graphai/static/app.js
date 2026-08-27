// GraphAI Interactive Controller & Bilingual Localization

let currentLang = 'en';
let currentRunId = null;

const TRANSLATIONS = {
  en: {
    badgeTitle: "DAG Workflow Engine",
    statusLive: "DAG Engine Active (:8010)",
    heroTitle: "Deterministic DAG Workflow Orchestration with Approvals & Fault Recovery",
    heroSubtitle: "Coordinate multi-agent processes with strict topological dependencies, parallel fan-out evaluation, human-in-the-loop compliance gates, and self-healing exponential retries.",
    metric1Label: "DAG Topological Integrity",
    metric1Sub: "Zero Race Conditions",
    metric2Label: "HITL Checkpoint Latency",
    metric2Sub: "Safe State Suspension",
    metric3Label: "Transient Error Recovery",
    metric3Sub: "Exponential Backoff & Jitter",
    metric4Label: "Parallel Task Speedup",
    metric4Sub: "Concurrent Node Dispatch",
    studioTitle: "DAG Orchestration & Approval Studio",
    studioDesc: "Trigger commercial loan origination workflows, watch parallel evaluation branches, interact with compliance approval gates, and test automated retry recovery.",
    lblPresets: "Select Workflow Scenario:",
    lblApplicant: "Commercial Applicant Entity",
    lblLoanAmount: "Requested Facility ($)",
    lblRiskScore: "Risk Index (0.0 - 1.0)",
    lblSimulateRetry: "Simulate Transient 504 Timeout (Triggers RetryAgent)",
    btnExecuteWorkflow: "⚡ Dispatch DAG Workflow",
    lblApprovalRequired: "⚠️ Compliance Checkpoint Reached",
    lblApprovalDesc: "Workflow paused for dual-custody authorization. Amount exceeds $100k policy ceiling.",
    titleDAGView: "DAG Execution Topology",
    lblAuditTrail: "Workflow Execution Audit Ledger:"
  },
  ar: {
    badgeTitle: "محرك تدفقات DAG المؤسسي",
    statusLive: "محرك التدفقات نشط (:8010)",
    heroTitle: "تنسيق تدفقات العمل الموجهة (DAG) مع الموافقات البشرية والتعافي التلقائي",
    heroSubtitle: "تنسيق مهام الوكلاء الأذكياء عبر علاقات الاعتماد الدقيقة، والتفرع المتوازي، وبوابات الموافقة البشرية، وإعادة المحاولة التلقائية عند الأخطاء.",
    metric1Label: "سلامة المخطط التوجيهي (DAG)",
    metric1Sub: "انعدام تعارضات التنفيذ",
    metric2Label: "سرعة تعليق بوابات الامتثال",
    metric2Sub: "تعليق واستئناف آمن وفوري",
    metric3Label: "التعافي من الأخطاء العابرة",
    metric3Sub: "تراجع أسي مع تشتت عشوائي",
    metric4Label: "تسريع التنفيذ المتوازي",
    metric4Sub: "تنفيذ أسرع بمعدل 2.4 ضعف",
    studioTitle: "استوديو إدارة تدفقات DAG والموافقات",
    studioDesc: "قم بتشغيل طلبات التسهيلات الائتمانية، وراقب فروع التقييم المتوازية، وتفاعل مع بوابات الموافقة البشرية، واختبر إعادة المحاولة الآلية.",
    lblPresets: "اختر سيناريو التدفق:",
    lblApplicant: "الجهة التجارية المتقدمة",
    lblLoanAmount: "مبلغ التسهيل المطلوب ($)",
    lblRiskScore: "مؤشر المخاطر (0.0 - 1.0)",
    lblSimulateRetry: "محاكاة مهلة عابرة 504 (لتفعيل وكيل إعادة المحاولة)",
    btnExecuteWorkflow: "⚡ إطلاق تدفق عمل DAG",
    lblApprovalRequired: "⚠️ تم الوصول إلى نقطة تفتيش الامتثال",
    lblApprovalDesc: "تم تعليق التدفق للحصول على موافقة مسؤول الامتثال لتجاوز سقف 100 ألف دولار.",
    titleDAGView: "مخطط هيكل التنفيذ (DAG)",
    lblAuditTrail: "سجل تدقيق تنفيذ المهام:"
  }
};

const SCENARIOS = [
  {
    name: "🏢 Enterprise Prime Commercial Facility ($250k - Requires HITL Approval)",
    applicant: "Apex Global Holdings Ltd",
    amount: 250000,
    risk: 0.42,
    retry: true
  },
  {
    name: "🚀 Fast-Track Micro Working Capital ($45k - Auto Underwriting)",
    applicant: "SwiftLogistics SMB",
    amount: 45000,
    risk: 0.18,
    retry: false
  },
  {
    name: "⚠️ High-Risk Bridge Facility ($1.5M - Dual Compliance Review)",
    applicant: "Horizon Venture Partners",
    amount: 1500000,
    risk: 0.65,
    retry: true
  }
];

function init() {
  renderPresets();
  loadScenario(0);
}

function toggleLanguage() {
  currentLang = currentLang === 'en' ? 'ar' : 'en';
  document.documentElement.lang = currentLang;
  document.documentElement.dir = currentLang === 'ar' ? 'rtl' : 'ltr';
  document.getElementById('langLabel').innerText = currentLang === 'en' ? 'العربية' : 'English';

  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (TRANSLATIONS[currentLang][key]) {
      el.innerText = TRANSLATIONS[currentLang][key];
    }
  });
}

function renderPresets() {
  const container = document.getElementById('scenarioButtons');
  container.innerHTML = '';
  SCENARIOS.forEach((sc, idx) => {
    const btn = document.createElement('button');
    btn.className = 'preset-btn';
    btn.innerText = sc.name;
    btn.onclick = () => loadScenario(idx);
    container.appendChild(btn);
  });
}

function loadScenario(idx) {
  const sc = SCENARIOS[idx];
  document.getElementById('applicantInput').value = sc.applicant;
  document.getElementById('amountInput').value = sc.amount;
  document.getElementById('riskInput').value = sc.risk;
  document.getElementById('transientToggle').checked = sc.retry;
}

async function runWorkflowTask() {
  const btn = document.getElementById('wfBtn');
  const applicant = document.getElementById('applicantInput').value.trim();
  const amount = parseFloat(document.getElementById('amountInput').value);
  const risk = parseFloat(document.getElementById('riskInput').value);
  const retry = document.getElementById('transientToggle').checked;

  currentRunId = `RUN-${Date.now()}`;
  btn.disabled = true;
  btn.innerText = "Dispatching DAG Nodes...";

  // Reset visualizer
  resetDAGVisuals();

  try {
    const res = await fetch('/api/v1/workflow/execute', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        run_id: currentRunId,
        graph_id: "LOAN_ORIGINATION_DAG",
        payload: {
          applicant_name: applicant,
          loan_amount: amount,
          risk_score: risk,
          simulate_transient_error: retry
        }
      })
    });

    const result = await res.json();
    renderWorkflowResult(result);

  } catch (err) {
    document.getElementById('auditStream').innerText = `Error: ${err.message}`;
  } finally {
    btn.disabled = false;
    btn.innerText = TRANSLATIONS[currentLang].btnExecuteWorkflow;
  }
}

async function submitApproval(action) {
  if (!currentRunId) return;

  try {
    const res = await fetch(`/api/v1/workflow/${currentRunId}/approve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        run_id: currentRunId,
        node_id: "NODE_3",
        action: action,
        approver_id: "COMPLIANCE_VP_01",
        signature_token: "sig_hmac_valid_9981",
        notes: "Authorized by compliance executive officer."
      })
    });

    const result = await res.json();
    document.getElementById('approvalBox').style.display = 'none';
    renderWorkflowResult(result);

  } catch (err) {
    alert(`Approval error: ${err.message}`);
  }
}

function renderWorkflowResult(result) {
  const badge = document.getElementById('wfStatusBadge');
  badge.innerText = result.status;
  if (result.status === 'COMPLETED') {
    badge.className = 'badge badge-success';
  } else if (result.status === 'PAUSED_FOR_APPROVAL') {
    badge.className = 'badge badge-warning';
    document.getElementById('approvalBox').style.display = 'block';
  } else {
    badge.className = 'badge badge-danger';
  }

  // Update DAG Node States
  result.completed_nodes.forEach(nid => {
    const el = document.getElementById(`node_${nid}`);
    const tag = document.getElementById(`status_${nid}`);
    if (el && tag) {
      el.className = 'dag-node completed';
      tag.innerText = 'COMPLETED';
      tag.style.color = '#10b981';
    }
  });

  if (result.waiting_approval_node) {
    const el = document.getElementById(`node_${result.waiting_approval_node}`);
    const tag = document.getElementById(`status_${result.waiting_approval_node}`);
    if (el && tag) {
      el.className = 'dag-node waiting';
      tag.innerText = 'WAITING APPROVAL';
      tag.style.color = '#f59e0b';
    }
  }

  // Render audit trail
  document.getElementById('auditStream').innerText = result.audit_trail.join('\n');
}

function resetDAGVisuals() {
  ['NODE_1', 'NODE_2A', 'NODE_2B', 'NODE_3', 'NODE_4'].forEach(nid => {
    const el = document.getElementById(`node_${nid}`);
    const tag = document.getElementById(`status_${nid}`);
    if (el && tag) {
      el.className = 'dag-node';
      tag.innerText = 'PENDING';
      tag.style.color = '#64748b';
    }
  });
  document.getElementById('approvalBox').style.display = 'none';
}

window.addEventListener('DOMContentLoaded', init);
