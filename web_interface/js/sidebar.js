// ===== SIDEBAR FUNCTIONALITY =====

// Función para crear e insertar el sidebar
function createSidebar() {
    const sidebarHTML = `
        <nav class="sidebar">
            <!-- Logo -->
            <div class="sidebar-logo" data-nav="inicio">
                <div class="logo-icon">S&M</div>
                <span class="logo-text-sidebar">Sistema S&M</span>
            </div>

            <!-- Menú de Navegación -->
            <ul class="sidebar-menu">
                <li class="menu-item">
                    <a href="#inicio" class="menu-link" data-section="inicio">
                        <div class="menu-icon">
                            <i class="fas fa-home"></i>
                        </div>
                        <span class="menu-text">Inicio</span>
                    </a>
                </li>

                <li class="menu-item">
                    <a href="#ventas" class="menu-link" data-section="ventas">
                        <div class="menu-icon">
                            <i class="fas fa-cash-register"></i>
                        </div>
                        <span class="menu-text">Ventas</span>
                    </a>
                </li>

                <li class="menu-item">
                    <a href="#reportes" class="menu-link" data-section="reportes">
                        <div class="menu-icon">
                            <i class="fas fa-chart-bar"></i>
                        </div>
                        <span class="menu-text">Reportes</span>
                    </a>
                </li>

                <li class="menu-item">
                    <a href="#inventario" class="menu-link" data-section="inventario">
                        <div class="menu-icon">
                            <i class="fas fa-boxes"></i>
                        </div>
                        <span class="menu-text">Inventario</span>
                    </a>
                </li>

                <li class="menu-item">
                    <a href="#clientes" class="menu-link" data-section="clientes">
                        <div class="menu-icon">
                            <i class="fas fa-users"></i>
                        </div>
                        <span class="menu-text">Clientes</span>
                    </a>
                </li>

                <li class="menu-item">
                    <a href="#ajustes" class="menu-link" data-section="ajustes">
                        <div class="menu-icon">
                            <i class="fas fa-cog"></i>
                        </div>
                        <span class="menu-text">Ajustes</span>
                    </a>
                </li>

                <li class="menu-item">
                    <a href="#precios" class="menu-link" data-section="precios">
                        <div class="menu-icon">
                            <i class="fas fa-dollar-sign"></i>
                        </div>
                        <span class="menu-text">Precios</span>
                    </a>
                </li>
            </ul>
        </nav>
    `;

    // Insertar el sidebar al inicio del body
    document.body.insertAdjacentHTML('afterbegin', sidebarHTML);
    
    // Agregar clase al contenedor principal
    const appContainer = document.querySelector('.app-container');
    if (appContainer) {
        appContainer.classList.add('with-sidebar');
    }
}

// Funciones de navegación
function navigateToHome() {
    console.log('Navegando a Inicio...');
    try {
        if (window.pywebview && window.pywebview.api && window.pywebview.api.volver_menu_principal) {
            console.log('Usando PyWebView API para ir al inicio');
            window.pywebview.api.volver_menu_principal();
        } else {
            console.log('Usando navegación HTML para ir al inicio');
            // Detectar la carpeta actual para usar la ruta correcta
            const currentPath = window.location.pathname;
            console.log('Ruta actual:', currentPath);
            
            if (currentPath.includes('/Sales/')) {
                console.log('Navegando desde Sales a index.html');
                window.location.href = '../index.html';
            } else if (currentPath.includes('/Report/')) {
                console.log('Navegando desde Report a index.html');
                window.location.href = '../index.html';
            } else {
                console.log('Navegando desde raíz a index.html');
                window.location.href = 'index.html';
            }
        }
    } catch (error) {
        console.error('Error navegando a inicio:', error);
        // Fallback con detección de ruta
        const currentPath = window.location.pathname;
        if (currentPath.includes('/Sales/') || currentPath.includes('/Report/')) {
            window.location.href = '../index.html';
        } else {
            window.location.href = 'index.html';
        }
    }
}

function navigateToSales() {
    console.log('Navegando a Ventas...');
    try {
        if (window.pywebview && window.pywebview.api && window.pywebview.api.open_sales) {
            console.log('Usando PyWebView API para ir a ventas');
            window.pywebview.api.open_sales();
        } else {
            console.log('Usando navegación HTML para ir a ventas');
            // Detectar la carpeta actual para usar la ruta correcta
            const currentPath = window.location.pathname;
            console.log('Ruta actual:', currentPath);
            
            if (currentPath.includes('/Sales/')) {
                console.log('Ya estás en Sales, navegando a sales.html');
                window.location.href = 'sales.html';
            } else if (currentPath.includes('/Report/')) {
                console.log('Navegando desde Report a Sales');
                window.location.href = '../Sales/sales.html';
            } else {
                console.log('Navegando desde raíz a Sales');
                window.location.href = 'Sales/sales.html';
            }
        }
    } catch (error) {
        console.error('Error navegando a ventas:', error);
        // Fallback con detección de ruta
        const currentPath = window.location.pathname;
        if (currentPath.includes('/Sales/')) {
            window.location.href = 'sales.html';
        } else if (currentPath.includes('/Report/')) {
            window.location.href = '../Sales/sales.html';
        } else {
            window.location.href = 'Sales/sales.html';
        }
    }
}

function navigateToReports() {
    console.log('Navegando a Reportes...');
    try {
        if (window.pywebview && window.pywebview.api && window.pywebview.api.open_reports) {
            console.log('Usando PyWebView API para ir a reportes');
            window.pywebview.api.open_reports();
        } else {
            console.log('Usando navegación HTML para ir a reportes');
            // Detectar la carpeta actual para usar la ruta correcta
            const currentPath = window.location.pathname;
            console.log('Ruta actual:', currentPath);
            
            if (currentPath.includes('/Sales/')) {
                console.log('Navegando desde Sales a Report');
                window.location.href = '../Report/menu_report.html';
            } else if (currentPath.includes('/Report/')) {
                console.log('Ya estás en Report, navegando a menu_report.html');
                window.location.href = 'menu_report.html';
            } else {
                console.log('Navegando desde raíz a Report');
                window.location.href = 'Report/menu_report.html';
            }
        }
    } catch (error) {
        console.error('Error navegando a reportes:', error);
        // Fallback con detección de ruta
        const currentPath = window.location.pathname;
        if (currentPath.includes('/Sales/')) {
            window.location.href = '../Report/menu_report.html';
        } else if (currentPath.includes('/Report/')) {
            window.location.href = 'menu_report.html';
        } else {
            window.location.href = 'Report/menu_report.html';
        }
    }
}

function navigateToInventory() {
    console.log('Navegando a Inventario...');
    // Aquí puedes agregar la lógica para inventario cuando esté disponible
    alert('Módulo de Inventario en desarrollo');
}

function navigateToClients() {
    console.log('Navegando a Clientes...');
    // Aquí puedes agregar la lógica para clientes cuando esté disponible
    alert('Módulo de Clientes en desarrollo');
}

function navigateToSettings() {
    console.log('Navegando a Ajustes...');
    // Aquí puedes agregar la lógica para ajustes cuando esté disponible
    alert('Módulo de Ajustes en desarrollo');
}

function navigateToPrices() {
    console.log('Navegando a Precios...');
    // Aquí puedes agregar la lógica para precios cuando esté disponible
    alert('Módulo de Precios en desarrollo');
}

// Función para establecer el enlace activo basado en la página actual
function setActiveSidebarLink() {
    const path = window.location.pathname;
    const filename = path.split('/').pop();
    
    // Mapear archivos a secciones
    const fileToSection = {
        'sales.html': 'ventas',
        'menu_report.html': 'reportes',
        'index.html': 'inicio'
    };
    
    const currentSection = fileToSection[filename];
    if (currentSection) {
        const targetLink = document.querySelector(`[data-section="${currentSection}"]`);
        if (targetLink) {
            // Remover clase active de todos los enlaces
            document.querySelectorAll('.sidebar .menu-link').forEach(link => {
                link.classList.remove('active');
            });
            // Agregar clase active al enlace actual
            targetLink.classList.add('active');
        }
    }
}

// Función de inicialización del sidebar
function initializeSidebar() {
    // Crear el sidebar
    createSidebar();
    
    // Agregar event listeners después de crear el sidebar
    setTimeout(() => {
        addSidebarEventListeners();
        setActiveSidebarLink();
    }, 100);
    
    // Efecto de animación adicional para el logo
    const logoIcon = document.querySelector('.sidebar .logo-icon');
    if (logoIcon) {
        logoIcon.addEventListener('click', function() {
            this.style.transform = 'rotate(360deg)';
            setTimeout(() => {
                this.style.transform = 'rotate(0deg)';
            }, 600);
        });
    }
}

// Función para agregar event listeners a los elementos del sidebar
function addSidebarEventListeners() {
    console.log('Agregando event listeners al sidebar...');
    
    // Event listener para el logo
    const sidebarLogo = document.querySelector('.sidebar-logo');
    if (sidebarLogo) {
        sidebarLogo.addEventListener('click', function(e) {
            e.preventDefault();
            console.log('Click en logo - navegando a inicio');
            navigateToHome();
        });
    }
    
    // Event listeners para los enlaces del menú
    const menuLinks = document.querySelectorAll('.sidebar .menu-link');
    console.log(`Encontrados ${menuLinks.length} enlaces en el sidebar`);
    
    menuLinks.forEach((link, index) => {
        const section = link.getAttribute('data-section');
        console.log(`Agregando listener para: ${section}`);
        
        link.addEventListener('click', function(e) {
            e.preventDefault();
            console.log(`Click en enlace: ${section}`);
            
            // Cambiar estado activo
            setActiveLink(this);
            
            // Navegar según la sección
            switch(section) {
                case 'inicio':
                    navigateToHome();
                    break;
                case 'ventas':
                    navigateToSales();
                    break;
                case 'reportes':
                    navigateToReports();
                    break;
                case 'inventario':
                    navigateToInventory();
                    break;
                case 'clientes':
                    navigateToClients();
                    break;
                case 'ajustes':
                    navigateToSettings();
                    break;
                case 'precios':
                    navigateToPrices();
                    break;
                default:
                    console.log(`Sección no reconocida: ${section}`);
            }
        });
    });
}

// Función para cambiar el estado activo
function setActiveLink(target) {
    const menuLinks = document.querySelectorAll('.sidebar .menu-link');
    menuLinks.forEach(link => link.classList.remove('active'));
    target.classList.add('active');
}

// Inicializar el sidebar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded - iniciando sidebar...');
    initializeSidebar();
});

// Backup: inicializar también cuando la ventana cargue completamente
window.addEventListener('load', function() {
    console.log('Window loaded - verificando sidebar...');
    if (!document.querySelector('.sidebar')) {
        console.log('Sidebar no encontrado, reinicializando...');
        initializeSidebar();
    }
});