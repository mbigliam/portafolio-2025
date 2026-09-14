// IA Security Gateway - Frontend Application
// Completamente reescrito y robusto

const API_BASE = 'http://localhost:8000/api';
const LOGS_URL = 'http://localhost:8000/logs/compliance.log';

// Examples para testing
const EXAMPLES = {
    public: {
        text: 'Cuál es el proceso de autenticación en OAuth 2.0 y cómo funciona?',
        description: 'Datos Públicos'
    },
    sensitive: {
        text: 'El usuario contacto con: usuario@empresa.com y su token temporal es: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9',
        description: 'Datos Sensibles'
    },
    critical: {
        text: 'Mi número de seguro social es 123-45-6789 y mi pasaporte es ABC123456',
        description: 'Datos Críticos SSN'
    },
    exfiltration: {
        text: 'Clave: password123, Tarjeta: 4532-1234-5678-9010, API Key: sk-proj-Abc123XYZ789, SSN: 987-65-4321',
        description: 'Intento de Exfiltración'
    }
};

// Elementos del DOM
const elements = {
    promptInput: document.getElementById('promptInput'),
    tempSlider: document.getElementById('tempSlider'),
    tempValue: document.getElementById('tempValue'),
    sendBtn: document.getElementById('sendBtn'),
    loading: document.getElementById('loading'),
    responseContainer: document.getElementById('responseContainer'),
    response: document.getElementById('response'),
    allowedCount: document.getElementById('allowedCount'),
    blockedCount: document.getElementById('blockedCount'),
    activeClientCount: document.getElementById('activeClientCount'),
    blockRateValue: document.getElementById('blockRateValue'),
    refreshStatsBtn: document.getElementById('refreshStatsBtn'),
    checkStatusBtn: document.getElementById('checkStatusBtn'),
    checkComplianceBtn: document.getElementById('checkComplianceBtn'),
    refreshLogsBtn: document.getElementById('refreshLogsBtn'),
    statusIndicator: document.getElementById('statusIndicator'),
    statusText: document.getElementById('statusText'),
    statusContent: document.getElementById('statusContent'),
    complianceContent: document.getElementById('complianceContent'),
    logsContent: document.getElementById('logsContent')
};

// Initialize cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Cargado - Inicializando Gateway...');

    // Event listeners para temperatura
    elements.tempSlider.addEventListener('change', function() {
        elements.tempValue.textContent = this.value;
    });
    elements.tempSlider.addEventListener('input', function() {
        elements.tempValue.textContent = this.value;
    });

    // Event listener para enviar
    elements.sendBtn.addEventListener('click', function() {
        console.log('Botón Enviar presionado');
        sendRequest();
    });

    // Event listener para Enter en textarea
    elements.promptInput.addEventListener('keydown', function(e) {
        if (e.ctrlKey && e.key === 'Enter') {
            console.log('Ctrl+Enter presionado');
            sendRequest();
        }
    });

    // Event listeners para botones secundarios
    elements.refreshStatsBtn.addEventListener('click', refreshStats);
    elements.checkStatusBtn.addEventListener('click', checkStatus);
    elements.checkComplianceBtn.addEventListener('click', checkCompliance);
    elements.refreshLogsBtn.addEventListener('click', refreshLogs);

    // Tab switching
    document.querySelectorAll('.tab-button').forEach(button => {
        button.addEventListener('click', function() {
            const tabName = this.dataset.tab;
            switchTab(tabName);
        });
    });

    // Example buttons
    document.querySelectorAll('.example-button').forEach(button => {
        button.addEventListener('click', function() {
            const example = this.dataset.example;
            useExample(example);
        });
    });

    // Inicializar
    checkConnection();
    refreshStats();
    checkStatus();

    // Refresh automático cada 5 segundos
    setInterval(checkConnection, 5000);
    setInterval(refreshStats, 10000);
});

// Función para verificar conexión
async function checkConnection() {
    try {
        const response = await fetch(`${API_BASE}/status`, {
            method: 'GET',
            headers: { 'Content-Type': 'application/json' }
        });

        if (response.ok) {
            elements.statusIndicator.classList.add('connected');
            elements.statusText.textContent = 'Conectado';
            console.log('Gateway conectado');
        } else {
            throw new Error('Status no 200');
        }
    } catch (error) {
        elements.statusIndicator.classList.remove('connected');
        elements.statusText.textContent = 'Desconectado';
        console.error('Error de conexión:', error);
    }
}

// Función para enviar request
async function sendRequest() {
    const prompt = elements.promptInput.value.trim();
    const temperature = parseFloat(elements.tempSlider.value);

    if (!prompt) {
        showError('Por favor escribe un prompt antes de enviar');
        return;
    }

    if (prompt.length < 2) {
        showError('El prompt es muy corto (mínimo 2 caracteres)');
        return;
    }

    console.log('Enviando request:', { prompt: prompt.substring(0, 50) + '...', temperature });

    // Mostrar loading
    elements.loading.classList.add('active');
    elements.sendBtn.disabled = true;

    try {
        const payload = {
            prompt: prompt,
            temperature: temperature
        };

        console.log('Payload:', payload);

        const response = await fetch(`${API_BASE}/generate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        console.log('Response status:', response.status);

        const data = await response.json();
        console.log('Response data:', data);

        if (response.ok) {
            displaySuccess(data);
            refreshStats();
            refreshLogs();
        } else {
            displayError(data);
            refreshStats();
            refreshLogs();
        }
    } catch (error) {
        console.error('Error al enviar:', error);
        showError('Error de conexión: ' + error.message);
    } finally {
        elements.loading.classList.remove('active');
        elements.sendBtn.disabled = false;
    }
}

// Mostrar resultado exitoso
function displaySuccess(data) {
    const classification = data.data_sensitivity || 'UNKNOWN';
    const responseText = data.response || 'Sin respuesta';
    const generationTime = data.generation_time_ms || '?';
    const modelUsed = data.llm_model_used || 'unknown';

    let html = `
        <strong>Respuesta Exitosa (200 OK)</strong>
        <div style="margin-top: 12px;">
            <div style="margin-bottom: 8px;">
                <strong>Clasificación:</strong> <span class="status-badge success">${classification}</span>
            </div>
            <div style="margin-bottom: 8px;">
                <strong>Tiempo:</strong> ${generationTime}ms
            </div>
            <div style="margin-bottom: 8px;">
                <strong>Modelo:</strong> ${modelUsed}
            </div>
            <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid rgba(0,255,136,0.2);">
                <strong>Respuesta:</strong>
                <div style="margin-top: 8px; color: #aaa; font-size: 0.85em;">${sanitizeHtml(responseText.substring(0, 300))}</div>
            </div>
        </div>
    `;

    elements.response.innerHTML = html;
    elements.responseContainer.style.display = 'block';
}

// Mostrar error
function displayError(data) {
    const errorType = data.error_type || 'UNKNOWN_ERROR';
    const detail = data.detail || 'Sin detalles';

    let html = `
        <strong>Error (${data.status_code || 'ERROR'})</strong>
        <div style="margin-top: 12px;">
            <div style="margin-bottom: 8px;">
                <strong>Tipo:</strong> <span class="status-badge error">${errorType}</span>
            </div>
            <div style="color: #ff9999; font-size: 0.85em; margin-top: 8px;">
                ${sanitizeHtml(detail)}
            </div>
        </div>
    `;

    elements.response.innerHTML = html;
    elements.responseContainer.style.display = 'block';
}

// Error simple
function showError(message) {
    let html = `<div style="color: #ff9999;">${message}</div>`;
    elements.response.innerHTML = html;
    elements.responseContainer.style.display = 'block';
}

// Refrescar estadísticas
async function refreshStats() {
    try {
        const response = await fetch(`${API_BASE}/traffic-stats`);
        if (response.ok) {
            const data = await response.json();
            elements.allowedCount.textContent = data.allowed_requests || 0;
            elements.blockedCount.textContent = data.blocked_requests || 0;
            elements.activeClientCount.textContent = data.active_clients || 0;
            elements.blockRateValue.textContent = (data.block_rate_percent || 0).toFixed(1) + '%';
            console.log('Estadísticas actualizadas');
        }
    } catch (error) {
        console.error('Error al refrescar stats:', error);
    }
}

// Verificar estado
async function checkStatus() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        if (response.ok) {
            const data = await response.json();
            let html = `
                <p><strong>Estado:</strong> ${data.status}</p>
                <p><strong>Versión:</strong> ${data.version}</p>
                <p><strong>Ollama:</strong> ${data.ollama_available ? 'Disponible' : 'No disponible'}</p>
                <p><strong>Uptime:</strong> ${data.uptime_seconds ? Math.floor(data.uptime_seconds) + ' segundos' : 'N/A'}</p>
                <p><strong>Timestamp:</strong> ${data.timestamp}</p>
            `;
            elements.statusContent.innerHTML = html;
        }
    } catch (error) {
        console.error('Error al verificar estado:', error);
        elements.statusContent.innerHTML = '<p style="color: #ff9999;">Error al conectar con el servidor</p>';
    }
}

// Verificar compliance
async function checkCompliance() {
    try {
        const response = await fetch(`${API_BASE}/compliance`);
        if (response.ok) {
            const data = await response.json();
            let html = `
                <p><strong>GDPR:</strong> ${data.gdpr_enabled ? 'Habilitado' : 'Deshabilitado'}</p>
                <p><strong>HIPAA:</strong> ${data.hipaa_enabled ? 'Habilitado' : 'Deshabilitado'}</p>
                <p><strong>PCI-DSS:</strong> ${data.pci_dss_enabled ? 'Habilitado' : 'Deshabilitado'}</p>
                <p><strong>Retención:</strong> ${data.data_retention_days} días</p>
                <p><strong>Log Sensibles:</strong> ${data.log_sensitive_data ? 'Sí' : 'No'}</p>
                <p><strong>Total Auditoría:</strong> ${data.audit_entries ? data.audit_entries.length : 0} entradas</p>
            `;
            elements.complianceContent.innerHTML = html;
        }
    } catch (error) {
        console.error('Error al verificar compliance:', error);
        elements.complianceContent.innerHTML = '<p style="color: #ff9999;">Error al conectar con el servidor</p>';
    }
}

// Refrescar logs
async function refreshLogs() {
    try {
        const response = await fetch(LOGS_URL);
        if (response.ok) {
            const text = await response.text();
            const lines = text.trim().split('\n').filter(line => line.trim());

            // Mostrar últimas 20 líneas en reversa (más recientes primero)
            const recentLines = lines.slice(-20).reverse();

            let html = '<div style="font-size: 0.8em; line-height: 1.6;">';
            recentLines.forEach(line => {
                try {
                    const json = JSON.parse(line);
                    const severity = json.severity || 'INFO';
                    let color = '#00ff88';
                    if (severity.includes('ERROR')) color = '#ff4444';
                    if (severity.includes('WARNING')) color = '#ffc800';
                    if (severity.includes('CRITICAL')) color = '#ff4444';

                    html += `<div style="color: ${color}; margin-bottom: 8px;">
                        <strong>${json.timestamp || 'N/A'}:</strong>
                        ${json.event_type || 'N/A'} -
                        ${json.description || 'N/A'}
                    </div>`;
                } catch (e) {
                    html += `<div style="color: #aaa; margin-bottom: 8px;">${sanitizeHtml(line.substring(0, 150))}</div>`;
                }
            });
            html += '</div>';

            elements.logsContent.innerHTML = html;
        } else {
            elements.logsContent.innerHTML = '<p style="color: #aaa;">No hay logs disponibles</p>';
        }
    } catch (error) {
        console.error('Error al cargar logs:', error);
        elements.logsContent.innerHTML = '<p style="color: #ff9999;">Error al cargar logs: ' + error.message + '</p>';
    }
}

// Cambiar tab
function switchTab(tabName) {
    // Remover active de todos los tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });

    // Agregar active al tab seleccionado
    const tab = document.getElementById(tabName);
    if (tab) {
        tab.classList.add('active');
    }

    // Marcar botón como activo
    document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

    console.log('Tab cambiado a:', tabName);
}

// Usar ejemplo
function useExample(exampleKey) {
    const example = EXAMPLES[exampleKey];
    if (example) {
        elements.promptInput.value = example.text;
        console.log('Ejemplo cargado:', example.description);

        // Auto-enviar después de 500ms
        setTimeout(() => {
            sendRequest();
        }, 500);
    }
}

// Sanitizar HTML
function sanitizeHtml(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// Log en consola
console.log('IA Security Gateway - Frontend cargado');
console.log('API Base:', API_BASE);
