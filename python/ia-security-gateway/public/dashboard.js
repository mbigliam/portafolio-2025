/**
 * IA Security Gateway - Dashboard JavaScript
 * Real backend integration - NO MOCK DATA
 * API Base: http://localhost:8000/api
 */

const API_BASE = 'http://localhost:8000/api';

// ============================================================
// UTILITIES & HELPERS
// ============================================================

function showLoading(elementId) {
    const element = document.getElementById(elementId);
    if (element) element.innerHTML = '<div class="loading active">⏳ Cargando...</div>';
}

function displayResult(elementId, content, status = 'info') {
    const element = document.getElementById(elementId);
    if (element) {
        element.innerHTML = content;
        element.className = `result-box ${status}`;
    }
}

function displayJSON(elementId, data, status = 'success') {
    const content = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
    displayResult(elementId, content, status);
}

function handleAPIError(error, elementId) {
    console.error('API Error:', error);
    displayResult(elementId, `❌ Error: ${error.message}`, 'error');
}

// ============================================================
// SECTION & TAB NAVIGATION
// ============================================================

function switchSection(sectionId) {
    // Hide all sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => section.classList.remove('active'));

    // Show selected section
    const section = document.getElementById(sectionId);
    if (section) {
        section.classList.add('active');
    }

    // Update nav items
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => item.classList.remove('active'));
    event.target.classList.add('active');

    // Update header title
    const titles = {
        'dashboard': '📊 Dashboard',
        'ip-analysis': '🔍 Análisis de IPs',
        'file-analysis': '📄 Análisis Archivos',
        'network': '🌐 Rastreo de Red',
        'violations': '⚠️ Violaciones',
        'ai-gateway': '🤖 AI Gateway'
    };
    document.getElementById('sectionTitle').textContent = titles[sectionId] || sectionId;
}

function switchTab(tabId, buttonElement) {
    // Get parent card or container to limit scope
    const container = buttonElement.closest('.section') || document.body;

    // Hide all tab contents within this container
    const tabContents = container.querySelectorAll('.tab-content');
    tabContents.forEach(content => content.classList.remove('active'));

    // Show selected tab
    const tabContent = document.getElementById(tabId);
    if (tabContent) {
        tabContent.classList.add('active');
    }

    // Update button states
    const buttons = container.querySelectorAll('.tab-btn');
    buttons.forEach(btn => btn.classList.remove('active'));
    buttonElement.classList.add('active');
}

// ============================================================
// DASHBOARD SECTION
// ============================================================

async function loadDashboard() {
    try {
        showLoading('systemStatus');
        showLoading('trafficStats');
        showLoading('complianceReport');

        // Load system status
        try {
            const statusRes = await fetch(`${API_BASE}/ai/status`);
            const statusData = await statusRes.json();
            const statusHTML = `
                <strong>Estado del Sistema:</strong><br>
                ${statusData.status === 'online' ? '✅ ONLINE' : '❌ OFFLINE'}<br>
                <br>
                <strong>Detalles:</strong><br>
                ${Object.entries(statusData).map(([k, v]) => `${k}: <code>${v}</code>`).join('<br>')}
            `;
            displayResult('systemStatus', statusHTML, 'success');
        } catch (e) {
            displayResult('systemStatus', '❌ No se pudo cargar el estado del sistema', 'error');
        }

        // Load traffic stats
        try {
            const statsRes = await fetch(`${API_BASE}/ai/traffic-stats`);
            const statsData = await statsRes.json();
            const statsHTML = `
                <strong>Estadísticas de Tráfico:</strong><br>
                Total Requests: <code>${statsData.total_requests || 0}</code><br>
                Requests Permitidos: <code>${statsData.allowed_requests || 0}</code><br>
                Requests Bloqueados: <code>${statsData.blocked_requests || 0}</code><br>
                Tasa de Bloqueo: <code>${((statsData.blocked_requests / statsData.total_requests * 100) || 0).toFixed(2)}%</code>
            `;
            displayResult('trafficStats', statsHTML, 'success');
        } catch (e) {
            displayResult('trafficStats', '❌ No se pudo cargar las estadísticas', 'error');
        }

        // Load compliance report
        try {
            const compRes = await fetch(`${API_BASE}/ai/compliance`);
            const compData = await compRes.json();
            const compHTML = `
                <strong>Reporte de Compliance:</strong><br>
                Status: <code>${compData.status || 'UNKNOWN'}</code><br>
                Violations: <code>${compData.violations || 0}</code><br>
                Last Check: <code>${compData.last_check || 'N/A'}</code><br>
                <br>
                <strong>Detalles:</strong><br>
                ${Object.entries(compData).filter(([k]) => k !== 'status' && k !== 'violations' && k !== 'last_check')
                    .map(([k, v]) => `${k}: <code>${JSON.stringify(v)}</code>`).join('<br>')}
            `;
            displayResult('complianceReport', compHTML, 'success');
        } catch (e) {
            displayResult('complianceReport', '❌ No se pudo cargar el reporte de compliance', 'error');
        }
    } catch (error) {
        handleAPIError(error, 'systemStatus');
    }
}

// ============================================================
// IP ANALYSIS SECTION
// ============================================================

async function verifyIP() {
    const ip = document.getElementById('verifyIPInput').value.trim();
    if (!ip) {
        displayResult('verifyIPResult', '❌ Ingresa una IP válida', 'error');
        return;
    }

    showLoading('verifyIPResult');
    try {
        const response = await fetch(`${API_BASE}/security/ip/verify?ip=${ip}`);
        const data = await response.json();

        const status = data.allowed ? 'success' : 'error';
        const html = `
            <strong>IP: ${ip}</strong><br>
            Estado: ${data.allowed ? '✅ PERMITIDA' : '❌ BLOQUEADA'}<br>
            <br>
            <strong>Tipo de Regla:</strong> ${data.rule_type || 'N/A'}<br>
            <strong>Descripción:</strong> ${data.description || 'Sin descripción'}<br>
            ${data.risk_level ? `<strong>Nivel de Riesgo:</strong> <code>${data.risk_level}</code><br>` : ''}
            ${data.timestamp ? `<strong>Timestamp:</strong> <code>${data.timestamp}</code>` : ''}
        `;
        displayResult('verifyIPResult', html, status);
    } catch (error) {
        handleAPIError(error, 'verifyIPResult');
    }
}

async function loadIPRules() {
    showLoading('ipRulesResult');
    try {
        const response = await fetch(`${API_BASE}/security/ip/rules`);
        const data = await response.json();

        if (!data.whitelist && !data.blacklist) {
            displayResult('ipRulesResult', 'No hay reglas de IP configuradas', 'info');
            return;
        }

        let html = '';

        // Whitelist
        if (data.whitelist && Object.keys(data.whitelist).length > 0) {
            html += '<strong style="color: #4caf50;">✅ WHITELIST:</strong><br>';
            Object.entries(data.whitelist).forEach(([ip, desc]) => {
                html += `<code>${ip}</code> - ${desc || 'Sin descripción'}<br>`;
            });
            html += '<br>';
        }

        // Blacklist
        if (data.blacklist && Object.keys(data.blacklist).length > 0) {
            html += '<strong style="color: #f44336;">🚫 BLACKLIST:</strong><br>';
            Object.entries(data.blacklist).forEach(([ip, reason]) => {
                html += `<code>${ip}</code> - ${reason || 'Sin razón'}<br>`;
            });
        }

        if (!html) {
            html = 'No hay reglas de IP configuradas';
        }

        displayResult('ipRulesResult', html, 'success');
    } catch (error) {
        handleAPIError(error, 'ipRulesResult');
    }
}

async function addWhitelist() {
    const ip = document.getElementById('whitelistIP').value.trim();
    const desc = document.getElementById('whitelistDesc').value.trim();

    if (!ip) {
        displayResult('whitelistResult', '❌ Ingresa una IP válida', 'error');
        return;
    }

    showLoading('whitelistResult');
    try {
        const response = await fetch(`${API_BASE}/security/ip/whitelist`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ip, description: desc || 'Added via Dashboard' })
        });
        const data = await response.json();

        if (response.ok) {
            displayResult('whitelistResult', `✅ IP ${ip} agregada a WHITELIST`, 'success');
            document.getElementById('whitelistIP').value = '';
            document.getElementById('whitelistDesc').value = '';
        } else {
            displayResult('whitelistResult', `❌ Error: ${data.error || 'No se pudo agregar la IP'}`, 'error');
        }
    } catch (error) {
        handleAPIError(error, 'whitelistResult');
    }
}

async function addBlacklist() {
    const ip = document.getElementById('blacklistIP').value.trim();
    const reason = document.getElementById('blacklistReason').value.trim();

    if (!ip) {
        displayResult('blacklistResult', '❌ Ingresa una IP válida', 'error');
        return;
    }

    showLoading('blacklistResult');
    try {
        const response = await fetch(`${API_BASE}/security/ip/blacklist`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ ip, reason: reason || 'Added via Dashboard' })
        });
        const data = await response.json();

        if (response.ok) {
            displayResult('blacklistResult', `✅ IP ${ip} agregada a BLACKLIST`, 'success');
            document.getElementById('blacklistIP').value = '';
            document.getElementById('blacklistReason').value = '';
        } else {
            displayResult('blacklistResult', `❌ Error: ${data.error || 'No se pudo bloquear la IP'}`, 'error');
        }
    } catch (error) {
        handleAPIError(error, 'blacklistResult');
    }
}

// ============================================================
// FILE ANALYSIS SECTION
// ============================================================

async function analyzeFile() {
    const fileInput = document.getElementById('fileInput');
    const clientIP = document.getElementById('clientIP').value.trim() || '192.168.1.100';

    if (!fileInput.files.length) {
        displayResult('fileAnalysisResult', '❌ Selecciona un archivo primero', 'error');
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);
    formData.append('client_ip', clientIP);

    showLoading('fileAnalysisResult');
    try {
        const response = await fetch(`${API_BASE}/security/file/analyze`, {
            method: 'POST',
            body: formData
        });
        const data = await response.json();

        if (response.ok) {
            const riskColor = {
                'SAFE': '#4caf50',
                'LOW': '#2196f3',
                'MEDIUM': '#ff9800',
                'HIGH': '#f44336',
                'CRITICAL': '#8b0000'
            }[data.risk_level] || '#999';

            const html = `
                <strong>Análisis del Archivo: ${file.name}</strong><br>
                Nivel de Riesgo: <span style="color: ${riskColor}; font-weight: bold;">${data.risk_level}</span><br>
                <br>
                <strong>Patrones Detectados:</strong><br>
                ${data.patterns_found ? `<code>${data.patterns_found.join(', ')}</code>` : 'Ninguno'}
                <br>
                <strong>Contenido Sensible Detectado:</strong><br>
                ${data.sensitive_content ? `<code>${JSON.stringify(data.sensitive_content)}</code>` : 'Ninguno'}
                <br>
                <strong>Timestamp:</strong> <code>${new Date().toLocaleString()}</code>
            `;
            displayResult('fileAnalysisResult', html, 'success');
            fileInput.value = '';
        } else {
            displayResult('fileAnalysisResult', `❌ Error: ${data.error || 'No se pudo analizar el archivo'}`, 'error');
        }
    } catch (error) {
        handleAPIError(error, 'fileAnalysisResult');
    }
}

async function getAnalysisSummary() {
    showLoading('analysisSummary');
    try {
        const response = await fetch(`${API_BASE}/security/file/analysis-summary`);
        const data = await response.json();

        const html = `
            <strong>Resumen de Análisis de Archivos:</strong><br>
            Total Archivos Analizados: <code>${data.total_analyzed || 0}</code><br>
            Archivos Seguros: <code>${data.safe || 0}</code><br>
            Archivos con Riesgo: <code>${data.at_risk || 0}</code><br>
            <br>
            <strong>Patrones Más Detectados:</strong><br>
            ${data.top_patterns ? Object.entries(data.top_patterns).map(([p, c]) => `${p}: <code>${c}</code>`).join('<br>') : 'No hay datos'}
        `;
        displayResult('analysisSummary', html, 'success');
    } catch (error) {
        handleAPIError(error, 'analysisSummary');
    }
}

// ============================================================
// NETWORK TRACKING SECTION
// ============================================================

async function getAllDevices() {
    showLoading('allDevicesResult');
    try {
        const response = await fetch(`${API_BASE}/network/devices`);
        const data = await response.json();

        if (!data.devices || data.devices.length === 0) {
            displayResult('allDevicesResult', 'No hay dispositivos registrados', 'info');
            return;
        }

        let html = `<strong>Total de Dispositivos: ${data.devices.length}</strong><br><br>`;
        data.devices.forEach(device => {
            const riskClass = device.risk_level?.includes('HIGH') || device.risk_level?.includes('CRITICAL') ? 'high-risk' :
                            device.risk_level?.includes('MEDIUM') ? 'medium-risk' : 'low-risk';
            html += `
                <div class="device-card ${riskClass}">
                    <strong>IP:</strong> <code>${device.ip}</code><br>
                    <strong>Hostname:</strong> ${device.hostname || 'Desconocido'}<br>
                    <strong>Nivel de Riesgo:</strong> <code>${device.risk_level || 'UNKNOWN'}</code><br>
                    <strong>Última Actividad:</strong> ${device.last_activity || 'N/A'}
                </div>
            `;
        });

        displayResult('allDevicesResult', html, 'success');
    } catch (error) {
        handleAPIError(error, 'allDevicesResult');
    }
}

async function getNetworkSummary() {
    showLoading('networkSummaryResult');
    try {
        const response = await fetch(`${API_BASE}/network/summary`);
        const data = await response.json();

        const html = `
            <strong>Resumen de Red:</strong><br>
            Dispositivos Conectados: <code>${data.connected_devices || 0}</code><br>
            IPs Whitelist: <code>${data.whitelist_ips || 0}</code><br>
            IPs Blacklist: <code>${data.blacklist_ips || 0}</code><br>
            Riesgo Promedio: <code>${data.average_risk || 'N/A'}</code><br>
            <br>
            <strong>Estadísticas:</strong><br>
            ${Object.entries(data).filter(([k]) => !['connected_devices', 'whitelist_ips', 'blacklist_ips', 'average_risk'].includes(k))
                .map(([k, v]) => `${k}: <code>${JSON.stringify(v)}</code>`).join('<br>')}
        `;
        displayResult('networkSummaryResult', html, 'success');
    } catch (error) {
        handleAPIError(error, 'networkSummaryResult');
    }
}

async function getDeviceProfile() {
    const ip = document.getElementById('deviceIP').value.trim();
    if (!ip) {
        displayResult('deviceProfileResult', '❌ Ingresa una IP válida', 'error');
        return;
    }

    showLoading('deviceProfileResult');
    try {
        const response = await fetch(`${API_BASE}/network/device-profile?ip=${ip}`);
        const data = await response.json();

        const html = `
            <strong>Perfil del Dispositivo: ${ip}</strong><br>
            <br>
            <strong>Información Básica:</strong><br>
            Hostname: <code>${data.hostname || 'Desconocido'}</code><br>
            User Agent: <code>${data.user_agent || 'N/A'}</code><br>
            Modelo IA: <code>${data.ai_model || 'N/A'}</code><br>
            <br>
            <strong>Métricas de Seguridad:</strong><br>
            Nivel de Riesgo: <code>${data.risk_level || 'UNKNOWN'}</code><br>
            Requests Totales: <code>${data.total_requests || 0}</code><br>
            Requests Bloqueados: <code>${data.blocked_requests || 0}</code><br>
            <br>
            <strong>Actividad:</strong><br>
            Primera Vista: ${data.first_seen || 'N/A'}<br>
            Última Actividad: ${data.last_activity || 'N/A'}
        `;
        displayResult('deviceProfileResult', html, 'success');
    } catch (error) {
        handleAPIError(error, 'deviceProfileResult');
    }
}

async function trackDevice() {
    const ip = document.getElementById('trackIP').value.trim();
    const hostname = document.getElementById('trackHostname').value.trim();
    const ua = document.getElementById('trackUA').value.trim();
    const model = document.getElementById('trackModel').value.trim();

    if (!ip) {
        displayResult('trackResult', '❌ Ingresa una IP válida', 'error');
        return;
    }

    showLoading('trackResult');
    try {
        const response = await fetch(`${API_BASE}/network/track-device`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ip,
                hostname: hostname || 'Unknown',
                user_agent: ua || 'Unknown',
                ai_model: model || 'Unknown'
            })
        });
        const data = await response.json();

        if (response.ok) {
            displayResult('trackResult', `✅ Dispositivo ${ip} rastreado exitosamente`, 'success');
            document.getElementById('trackIP').value = '';
            document.getElementById('trackHostname').value = '';
            document.getElementById('trackUA').value = '';
            document.getElementById('trackModel').value = '';
        } else {
            displayResult('trackResult', `❌ Error: ${data.error || 'No se pudo rastrear el dispositivo'}`, 'error');
        }
    } catch (error) {
        handleAPIError(error, 'trackResult');
    }
}

// ============================================================
// VIOLATIONS SECTION
// ============================================================

async function getViolations() {
    showLoading('violationsResult');
    try {
        const response = await fetch(`${API_BASE}/security/violations`);
        const data = await response.json();

        if (!data.violations || data.violations.length === 0) {
            displayResult('violationsResult', 'No hay violaciones registradas', 'info');
            return;
        }

        let html = `<strong>Total de Violaciones: ${data.violations.length}</strong><br><br>`;
        data.violations.forEach((violation, index) => {
            html += `
                <div class="violation-card">
                    <strong>#${index + 1} - ${violation.type || 'UNKNOWN'}</strong><br>
                    IP: <code>${violation.ip}</code><br>
                    Descripción: ${violation.description || 'N/A'}<br>
                    Timestamp: ${violation.timestamp || 'N/A'}
                </div>
            `;
        });

        displayResult('violationsResult', html, 'error');
    } catch (error) {
        handleAPIError(error, 'violationsResult');
    }
}

async function reportViolation() {
    const ip = document.getElementById('violationIP').value.trim();
    const type = document.getElementById('violationType').value.trim();
    const desc = document.getElementById('violationDesc').value.trim();

    if (!ip || !type) {
        displayResult('reportViolationResult', '❌ Ingresa IP y tipo de violación', 'error');
        return;
    }

    showLoading('reportViolationResult');
    try {
        const response = await fetch(`${API_BASE}/security/violations`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                ip,
                type,
                description: desc || 'Reported via Dashboard'
            })
        });
        const data = await response.json();

        if (response.ok) {
            displayResult('reportViolationResult', `✅ Violación reportada para IP ${ip}`, 'success');
            document.getElementById('violationIP').value = '';
            document.getElementById('violationType').value = '';
            document.getElementById('violationDesc').value = '';
        } else {
            displayResult('reportViolationResult', `❌ Error: ${data.error || 'No se pudo reportar la violación'}`, 'error');
        }
    } catch (error) {
        handleAPIError(error, 'reportViolationResult');
    }
}

// ============================================================
// AI GATEWAY SECTION
// ============================================================

async function generateText() {
    const prompt = document.getElementById('generatePrompt').value.trim();
    if (!prompt) {
        displayResult('generateResult', '❌ Ingresa un prompt válido', 'error');
        return;
    }

    showLoading('generateResult');
    try {
        const response = await fetch(`${API_BASE}/ai/generate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt })
        });
        const data = await response.json();

        if (response.ok) {
            const html = `
                <strong>Generación de Texto:</strong><br>
                <br>
                <strong>Prompt:</strong> ${prompt}<br>
                <br>
                <strong>Resultado:</strong><br>
                ${data.generated_text || 'Sin resultado'}
            `;
            displayResult('generateResult', html, 'success');
            document.getElementById('generatePrompt').value = '';
        } else {
            displayResult('generateResult', `❌ Error: ${data.error || 'No se pudo generar texto'}`, 'error');
        }
    } catch (error) {
        handleAPIError(error, 'generateResult');
    }
}

async function sendChat() {
    const message = document.getElementById('chatMessage').value.trim();
    if (!message) {
        displayResult('chatResult', '❌ Ingresa un mensaje válido', 'error');
        return;
    }

    showLoading('chatResult');
    try {
        const response = await fetch(`${API_BASE}/ai/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        const data = await response.json();

        if (response.ok) {
            const html = `
                <strong>Tú:</strong> ${message}<br>
                <br>
                <strong>AI:</strong><br>
                ${data.response || 'Sin respuesta'}
            `;
            displayResult('chatResult', html, 'success');
            document.getElementById('chatMessage').value = '';
        } else {
            displayResult('chatResult', `❌ Error: ${data.error || 'No se pudo enviar el mensaje'}`, 'error');
        }
    } catch (error) {
        handleAPIError(error, 'chatResult');
    }
}

// ============================================================
// INITIALIZATION
// ============================================================

// Load dashboard on page load
window.addEventListener('DOMContentLoaded', () => {
    console.log('🟢 Dashboard.js loaded - Connecting to:', API_BASE);
    loadDashboard();

    // Auto-refresh dashboard every 30 seconds
    setInterval(() => {
        if (document.getElementById('dashboard').classList.contains('active')) {
            loadDashboard();
        }
    }, 30000);
});
