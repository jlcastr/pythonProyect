// ===== SIDEBAR SIMPLE Y FUNCIONAL =====

console.log('🚀 Sidebar.js cargado');

// Funciones de navegación directas
function navegarInicio() {
    console.log('🏠 Navegando a Inicio...');
    const path = window.location.pathname;
    if (path.includes('/Sales/')) {
        window.location.href = '../index.html';
    } else if (path.includes('/Report/')) {
        window.location.href = '../index.html';
    } else if (path.includes('/Settings/')) {
        window.location.href = '../index.html';
    } else if (path.includes('/Inventory/')) {
        window.location.href = '../index.html';
    } else {
        window.location.href = 'index.html';
    }
}

function navegarVentas() {
    console.log('💰 Navegando a Ventas...');
    const path = window.location.pathname;
    if (path.includes('/Sales/')) {
        window.location.href = 'sales.html';
    } else if (path.includes('/Report/')) {
        window.location.href = '../Sales/sales.html';
    } else if (path.includes('/Settings/')) {
        window.location.href = '../Sales/sales.html';
    } else if (path.includes('/Inventory/')) {
        window.location.href = '../Sales/sales.html';
    } else {
        window.location.href = 'Sales/sales.html';
    }
}

function navegarReportes() {
    console.log('📊 Navegando a Reportes...');
    const path = window.location.pathname;
    if (path.includes('/Sales/')) {
        window.location.href = '../Report/menu_report.html';
    } else if (path.includes('/Report/')) {
        window.location.href = 'menu_report.html';
    } else if (path.includes('/Settings/')) {
        window.location.href = '../Report/menu_report.html';
    } else if (path.includes('/Inventory/')) {
        window.location.href = '../Report/menu_report.html';
    } else {
        window.location.href = 'Report/menu_report.html';
    }
}

function navegarInventario() {
    console.log('📦 Navegando a Inventario...');
    const path = window.location.pathname;
    if (path.includes('/Sales/')) {
        window.location.href = '../Inventory/menu_inventory.html';
    } else if (path.includes('/Report/')) {
        window.location.href = '../Inventory/menu_inventory.html';
    } else if (path.includes('/Settings/')) {
        window.location.href = '../Inventory/menu_inventory.html';
    } else if (path.includes('/Inventory/')) {
        window.location.href = 'menu_inventory.html';
    } else {
        window.location.href = 'Inventory/menu_inventory.html';
    }
}

function navegarAjustes() {
    console.log('⚙️ Navegando a Ajustes...');
    const path = window.location.pathname;
    if (path.includes('/Sales/')) {
        window.location.href = '../Settings/menu_settings.html';
    } else if (path.includes('/Report/')) {
        window.location.href = '../Settings/menu_settings.html';
    } else if (path.includes('/Settings/')) {
        window.location.href = 'menu_settings.html';
    } else if (path.includes('/Inventory/')) {
        window.location.href = '../Settings/menu_settings.html';
    } else {
        window.location.href = 'Settings/menu_settings.html';
    }
}

function mostrarEnDesarrollo(modulo) {
    alert(`Módulo de ${modulo} en desarrollo`);
}

// Crear el HTML del sidebar
function crearSidebar() {
    console.log('🔧 Creando sidebar HTML...');
    
    const sidebarHTML = `
        <nav class="sidebar" id="main-sidebar">
            <!-- Logo -->
            <div class="sidebar-logo" style="cursor: pointer;">
                <div class="logo-icon">S&M</div>
                <span class="logo-text-sidebar">Sistema S&M</span>
            </div>

            <!-- Menú de Navegación -->
            <ul class="sidebar-menu">
                <li class="menu-item">
                    <a href="javascript:void(0)" class="menu-link" data-nav="inicio" style="cursor: pointer;">
                        <div class="menu-icon">
                            <i class="fas fa-home"></i>
                        </div>
                        <span class="menu-text">Inicio</span>
                    </a>
                </li>

                <li class="menu-item">
                    <a href="javascript:void(0)" class="menu-link" data-nav="ventas" style="cursor: pointer;">
                        <div class="menu-icon">
                            <i class="fas fa-cash-register"></i>
                        </div>
                        <span class="menu-text">Ventas</span>
                    </a>
                </li>

                <li class="menu-item">
                    <a href="javascript:void(0)" class="menu-link" data-nav="reportes" style="cursor: pointer;">
                        <div class="menu-icon">
                            <i class="fas fa-chart-bar"></i>
                        </div>
                        <span class="menu-text">Reportes</span>
                    </a>
                </li>

                <li class="menu-item">
                    <a href="javascript:void(0)" class="menu-link" data-nav="inventario" style="cursor: pointer;">
                        <div class="menu-icon">
                            <i class="fas fa-boxes"></i>
                        </div>
                        <span class="menu-text">Inventario</span>
                    </a>
                </li>

                <li class="menu-item">
                    <a href="javascript:void(0)" class="menu-link" data-nav="clientes" style="cursor: pointer;">
                        <div class="menu-icon">
                            <i class="fas fa-users"></i>
                        </div>
                        <span class="menu-text">Clientes</span>
                    </a>
                </li>

                <li class="menu-item">
                    <a href="javascript:void(0)" class="menu-link" data-nav="ajustes" style="cursor: pointer;">
                        <div class="menu-icon">
                            <i class="fas fa-cog"></i>
                        </div>
                        <span class="menu-text">Ajustes</span>
                    </a>
                </li>

                <li class="menu-item">
                    <a href="javascript:void(0)" class="menu-link" data-nav="precios" style="cursor: pointer;">
                        <div class="menu-icon">
                            <i class="fas fa-dollar-sign"></i>
                        </div>
                        <span class="menu-text">Precios</span>
                    </a>
                </li>
            </ul>
        </nav>
    `;

    // Insertar al inicio del body
    document.body.insertAdjacentHTML('afterbegin', sidebarHTML);
    
    // Agregar clase al contenedor principal
    const appContainer = document.querySelector('.app-container');
    if (appContainer) {
        appContainer.classList.add('with-sidebar');
        console.log('✅ Clase with-sidebar agregada');
    }
    
    console.log('✅ Sidebar HTML creado');
}

// Agregar event listeners
function agregarEventListeners() {
    console.log('🎯 Agregando event listeners...');
    
    // Logo click
    const logo = document.querySelector('.sidebar-logo');
    if (logo) {
        logo.onclick = function() {
            console.log('🖱️ Click en logo');
            navegarInicio();
        };
        console.log('✅ Event listener agregado al logo');
    }
    
    // Menu links clicks
    const menuLinks = document.querySelectorAll('.sidebar .menu-link');
    console.log(`🔍 Encontrados ${menuLinks.length} enlaces de menú`);
    
    menuLinks.forEach((link, index) => {
        const navTarget = link.getAttribute('data-nav');
        console.log(`📎 Configurando enlace ${index + 1}: ${navTarget}`);
        
        link.onclick = function(e) {
            e.preventDefault();
            e.stopPropagation();
            console.log(`🖱️ Click en: ${navTarget}`);
            
            // Cambiar estado activo
            document.querySelectorAll('.sidebar .menu-link').forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            
            // Navegar
            switch(navTarget) {
                case 'inicio':
                    navegarInicio();
                    break;
                case 'ventas':
                    navegarVentas();
                    break;
                case 'reportes':
                    navegarReportes();
                    break;
                case 'inventario':
                    navegarInventario();
                    break;
                case 'clientes':
                    mostrarEnDesarrollo('Clientes');
                    break;
                case 'ajustes':
                    navegarAjustes();
                    break;
                case 'precios':
                    mostrarEnDesarrollo('Precios');
                    break;
                default:
                    console.log(`❌ Navegación no reconocida: ${navTarget}`);
            }
        };
    });
    
    console.log(`✅ Event listeners agregados a ${menuLinks.length} enlaces`);
}

// Detectar página actual y marcar como activa
function marcarPaginaActiva() {
    const path = window.location.pathname;
    let seccionActiva = '';
    
    if (path.includes('sales.html')) {
        seccionActiva = 'ventas';
    } else if (path.includes('menu_report.html') || path.includes('report_sales')) {
        seccionActiva = 'reportes';
    } else if (path.includes('menu_settings.html') || path.includes('email.html') || path.includes('logo.html')) {
        seccionActiva = 'ajustes';
    } else if (path.includes('menu_inventory.html') || path.includes('inventory.html') || path.includes('typeofmerchandise.html')) {
        seccionActiva = 'inventario';
    } else if (path.includes('index.html') || path.endsWith('/')) {
        seccionActiva = 'inicio';
    }
    
    if (seccionActiva) {
        const enlaceActivo = document.querySelector(`[data-nav="${seccionActiva}"]`);
        if (enlaceActivo) {
            enlaceActivo.classList.add('active');
            console.log(`✅ Página activa marcada: ${seccionActiva}`);
        }
    }
}

// Función principal de inicialización
function inicializarSidebar() {
    console.log('🚀 Inicializando sidebar...');
    
    // Verificar si ya existe
    if (document.querySelector('#main-sidebar')) {
        console.log('⚠️ Sidebar ya existe, eliminando...');
        document.querySelector('#main-sidebar').remove();
    }
    
    // Crear sidebar
    crearSidebar();
    
    // Esperar un momento y agregar event listeners
    setTimeout(() => {
        agregarEventListeners();
        marcarPaginaActiva();
        console.log('🎉 Sidebar completamente inicializado');
    }, 100);
}

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inicializarSidebar);
} else {
    // DOM ya está listo
    inicializarSidebar();
}

// Backup: asegurar que funcione
window.addEventListener('load', function() {
    if (!document.querySelector('#main-sidebar')) {
        console.log('🔄 Reinicializando sidebar...');
        inicializarSidebar();
    }
});

console.log('✅ Sidebar.js configurado completamente');