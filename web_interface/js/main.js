// Configuración y variables globales
const AppConfig = {
    debug: true,
    animationDuration: 300,
    hoverEffects: true
};

// Sistema de logging
const Logger = {
    log: (message, data = null) => {
        if (AppConfig.debug) {
            console.log(`[App] ${message}`, data || '');
        }
    },
    error: (message, error = null) => {
        console.error(`[App Error] ${message}`, error || '');
    }
};

// Gestor de animaciones
class AnimationManager {
    static fadeIn(element, duration = AppConfig.animationDuration) {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = `all ${duration}ms ease`;
        
        setTimeout(() => {
            element.style.opacity = '1';
            element.style.transform = 'translateY(0)';
        }, 10);
    }

    static scaleUp(element, scale = 1.05, duration = 200) {
        element.style.transform = `scale(${scale})`;
        element.style.transition = `transform ${duration}ms ease`;
        
        setTimeout(() => {
            element.style.transform = 'scale(1)';
        }, duration);
    }

    static shake(element, intensity = 5) {
        const originalTransform = element.style.transform;
        let shakeCount = 0;
        const maxShakes = 6;
        
        const shakeInterval = setInterval(() => {
            if (shakeCount >= maxShakes) {
                clearInterval(shakeInterval);
                element.style.transform = originalTransform;
                return;
            }
            
            const offsetX = Math.random() * intensity * 2 - intensity;
            element.style.transform = `translateX(${offsetX}px)`;
            shakeCount++;
        }, 50);
    }
}

// Gestor de efectos de sonido (opcional)
class SoundManager {
    static playClickSound() {
        // Implementar sonidos si se requiere
        Logger.log('Click sound triggered');
    }
    
    static playHoverSound() {
        Logger.log('Hover sound triggered');
    }
}

// Gestor de la aplicación principal
class SalesSystemApp {
    constructor() {
        this.menuButtons = {};
        this.isInitialized = false;
        this.currentModule = null;
        
        Logger.log('Inicializando Sales System App');
        this.init();
    }

    init() {
        if (this.isInitialized) return;
        
        // Esperar a que el DOM esté completamente cargado
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupApp());
        } else {
            this.setupApp();
        }
    }

    setupApp() {
        Logger.log('Configurando aplicación');
        
        // Debug de PyWebView
        this.debugPyWebView();
        
        this.initializeMenuButtons();
        this.setupEventListeners();
        this.setupResponsiveHandling();
        this.showWelcomeAnimation();
        
        this.isInitialized = true;
        Logger.log('Aplicación inicializada correctamente');
    }
    
    debugPyWebView() {
        Logger.log('=== DEBUG PYWEBVIEW ===');
        Logger.log('window.pywebview existe:', !!window.pywebview);
        
        if (window.pywebview) {
            Logger.log('window.pywebview.api existe:', !!window.pywebview.api);
            
            if (window.pywebview.api) {
                Logger.log('Funciones API disponibles:', Object.keys(window.pywebview.api));
                Logger.log('open_sales disponible:', typeof window.pywebview.api.open_sales);
            }
        }
        Logger.log('=====================');
    }

    initializeMenuButtons() {
        const menuItems = document.querySelectorAll('.menu-item');
        
        menuItems.forEach((item, index) => {
            const button = item.querySelector('.menu-button');
            const buttonText = button.querySelector('.button-text').textContent.trim();
            
            this.menuButtons[buttonText] = {
                element: button,
                index: index,
                module: this.getModuleName(buttonText)
            };

            // Configurar eventos para cada botón
            this.setupButtonEvents(button, buttonText);
        });

        Logger.log('Botones del menú inicializados', this.menuButtons);
    }

    getModuleName(buttonText) {
        const moduleMap = {
            'VENTAS': 'sales',
            'REPORTES': 'reports',
            'INVENTARIO': 'inventory',
            'CLIENTES': 'customers',
            'AJUSTES': 'settings',
            'PRECIOS': 'prices',
            'SALIR': 'exit'
        };
        
        return moduleMap[buttonText] || buttonText.toLowerCase();
    }

    setupButtonEvents(button, buttonText) {
        // Evento de click
        button.addEventListener('click', (e) => {
            e.preventDefault();
            this.handleMenuClick(buttonText, button);
        });

        // Efectos de hover mejorados
        if (AppConfig.hoverEffects) {
            button.addEventListener('mouseenter', () => {
                SoundManager.playHoverSound();
                this.addHoverEffect(button);
            });

            button.addEventListener('mouseleave', () => {
                this.removeHoverEffect(button);
            });
        }

        // Soporte para dispositivos táctiles
        button.addEventListener('touchstart', (e) => {
            e.preventDefault();
            this.addTouchEffect(button);
        });

        button.addEventListener('touchend', (e) => {
            e.preventDefault();
            this.removeTouchEffect(button);
            setTimeout(() => {
                this.handleMenuClick(buttonText, button);
            }, 100);
        });
    }

    handleMenuClick(buttonText, buttonElement) {
        Logger.log(`Botón presionado: ${buttonText}`);
        
        SoundManager.playClickSound();
        AnimationManager.scaleUp(buttonElement);
        
        const module = this.getModuleName(buttonText);
        
        // Mostrar indicador de carga
        this.showLoadingIndicator(buttonElement);
        
        // Comunicación con Python
        const hasPyWebView = window.pywebview && 
                           window.pywebview.api && 
                           typeof window.pywebview.api.open_sales === 'function';
        
        Logger.log(`PyWebView disponible: ${hasPyWebView}`);
        
        if (hasPyWebView) {
            this.callPythonFunction(module, buttonText, buttonElement);
        } else {
            Logger.log('PyWebView no disponible, usando modo demostración');
            // Modo de desarrollo - simular respuesta
            this.simulateModuleLoad(module, buttonText, buttonElement);
        }
    }

    callPythonFunction(module, buttonText, buttonElement) {
        Logger.log(`Llamando función Python para módulo: ${module} (botón: ${buttonText})`);
        
        try {
            // Llamada a la función Python correspondiente
            switch(module) {
                case 'sales':
                    Logger.log('=== CASE SALES EJECUTADO ===');
                    Logger.log('ButtonText:', buttonText);
                    Logger.log('Module:', module);
                    Logger.log('ButtonElement:', buttonElement);
                    Logger.log('Ejecutando invokeOpenSales...');
                    
                    // Intentar navegación inmediata como test
                    setTimeout(() => {
                        Logger.log('Ejecutando navegación de emergencia...');
                        window.location.href = './Sales/sales.html';
                    }, 100);
                    
                    this.invokeOpenSales();
                    
                    // Ocultar loading después de un tiempo si no hay respuesta
                    setTimeout(() => {
                        this.hideLoadingIndicator(buttonElement);
                    }, 3000);
                    break;
                case 'reports':
                    Logger.log('Ejecutando invokeOpenReports...');
                    this.invokeOpenReports();
                    break;
                case 'inventory':
                    Logger.log('Ejecutando invokeOpenInventory...');
                    this.invokeOpenInventory();
                    break;
                case 'customers':
                    Logger.log('Ejecutando invokeOpenCustomers...');
                    this.invokeOpenCustomers();
                    break;
                case 'settings':
                    Logger.log('Ejecutando invokeOpenSettings...');
                    this.invokeOpenSettings();
                    break;
                case 'prices':
                    Logger.log('Ejecutando invokeOpenPrices...');
                    this.invokeOpenPrices();
                    break;
                case 'exit':
                    Logger.log('Ejecutando invokeExit...');
                    this.invokeExit();
                    break;
                default:
                    Logger.error(`Módulo no reconocido: ${module}`);
                    this.showError(`Módulo ${buttonText} no implementado`);
            }
        } catch (error) {
            Logger.error('Error al llamar función Python', error);
            this.showError('Error de comunicación con el sistema');
        } finally {
            this.hideLoadingIndicator(buttonElement);
        }
    }

    // Funciones de comunicación con Python
    invokeOpenSales() {
        Logger.log('=== INVOKE OPEN SALES ===');
        Logger.log('PyWebView API disponible:', !!(window.pywebview?.api?.open_sales));
        
        // Siempre usar navegación directa por simplicidad y confiabilidad
        Logger.log('Usando navegación directa a ventas');
        this.navigateToSales();
        
        // Opcional: también llamar a la API si está disponible (para backend logging)
        if (window.pywebview?.api?.open_sales) {
            try {
                Logger.log('También llamando API para logging backend...');
                window.pywebview.api.open_sales().then(result => {
                    Logger.log('API llamada exitosa (solo para logging):', result);
                }).catch(error => {
                    Logger.log('API falló pero navegación directa ya ejecutada:', error);
                });
            } catch (error) {
                Logger.log('Error en API pero navegación directa ya ejecutada:', error);
            }
        }
    }
    
    // Función de respaldo para navegar directamente
    navigateToSales() {
        try {
            Logger.log('=== NAVIGATE TO SALES ===');
            Logger.log('Iniciando navegación directa a ventas');
            Logger.log('URL actual:', window.location.href);
            Logger.log('Directorio actual:', window.location.pathname);
            
            // Determinar la ruta correcta basada en la ubicación actual
            const currentPath = window.location.pathname;
            let salesUrl;
            
            if (currentPath.includes('web_interface')) {
                // Estamos en el directorio web_interface
                salesUrl = './Sales/sales.html';
            } else {
                // Ruta absoluta como respaldo
                salesUrl = 'Sales/sales.html';
            }
            
            Logger.log(`URL de ventas calculada: ${salesUrl}`);
            
            // Verificar que podemos navegar
            if (typeof window.location.href === 'string') {
                Logger.log('Ejecutando navegación...');
                window.location.href = salesUrl;
                Logger.log('Navegación iniciada exitosamente');
            } else {
                throw new Error('window.location.href no está disponible');
            }
            
        } catch (error) {
            Logger.error('Error en navegación directa:', error);
            
            // Intentar métodos alternativos de navegación
        }
    }

    navigateToSettings() {
        try {
            Logger.log('=== NAVIGATE TO SETTINGS ===');
            Logger.log('Iniciando navegación directa a ajustes');
            Logger.log('URL actual:', window.location.href);
            Logger.log('Directorio actual:', window.location.pathname);
            
            // Determinar la ruta correcta basada en la ubicación actual
            const currentPath = window.location.pathname;
            let settingsUrl;
            
            if (currentPath.includes('web_interface')) {
                // Estamos en el directorio web_interface
                settingsUrl = './Settings/menu_settings.html';
            } else {
                // Ruta absoluta como respaldo
                settingsUrl = 'Settings/menu_settings.html';
            }
            
            Logger.log(`URL de ajustes calculada: ${settingsUrl}`);
            
            // Verificar que podemos navegar
            if (typeof window.location.href === 'string') {
                Logger.log('Ejecutando navegación...');
                window.location.href = settingsUrl;
                Logger.log('Navegación iniciada exitosamente');
            } else {
                throw new Error('window.location.href no está disponible');
            }
            
        } catch (error) {
            Logger.error('Error en navegación directa a ajustes:', error);
            
            // Intentar métodos alternativos de navegación
            try {
                Logger.log('Intentando método alternativo: window.location.assign');
                window.location.assign('./Settings/menu_settings.html');
            } catch (error2) {
                Logger.error('Error en método alternativo:', error2);
                
                // Último recurso: mostrar mensaje al usuario
                const errorMsg = 'No se pudo abrir el módulo de ajustes. Error de navegación.';
                Logger.error(errorMsg);
                
                if (typeof alert !== 'undefined') {
                    alert(errorMsg + '\n\nPor favor, recargue la página e intente nuevamente.');
                }
            }
        }
    }

    navigateToReports() {
        try {
            Logger.log('=== NAVIGATE TO REPORTS ===');
            Logger.log('Iniciando navegación directa a reportes');
            Logger.log('URL actual:', window.location.href);
            Logger.log('Directorio actual:', window.location.pathname);
            
            // Determinar la ruta correcta basada en la ubicación actual
            const currentPath = window.location.pathname;
            let reportsUrl;
            
            if (currentPath.includes('web_interface')) {
                // Estamos en el directorio web_interface
                reportsUrl = './Report/menu_report.html';
            } else {
                // Ruta absoluta como respaldo
                reportsUrl = 'Report/menu_report.html';
            }
            
            Logger.log(`URL de reportes calculada: ${reportsUrl}`);
            
            // Verificar que podemos navegar
            if (typeof window.location.href === 'string') {
                Logger.log('Ejecutando navegación...');
                window.location.href = reportsUrl;
                Logger.log('Navegación iniciada exitosamente');
            } else {
                throw new Error('window.location.href no está disponible');
            }
            
        } catch (error) {
            Logger.error('Error en navegación directa a reportes:', error);
            
            // Intentar métodos alternativos de navegación
            try {
                Logger.log('Intentando método alternativo: window.location.assign');
                window.location.assign('./Report/menu_report.html');
            } catch (error2) {
                Logger.error('Error en método alternativo:', error2);
                
                // Último recurso: mostrar mensaje al usuario
                const errorMsg = 'No se pudo abrir el módulo de reportes. Error de navegación.';
                Logger.error(errorMsg);
                
                if (typeof alert !== 'undefined') {
                    alert(errorMsg + '\n\nPor favor, recargue la página e intente nuevamente.');
                }
            }
        }
    }

    invokeOpenReports() {
        Logger.log('=== INVOKE OPEN REPORTS ===');
        Logger.log('Navegando al módulo de reportes...');
        
        // Navegar directamente a la página de reportes
        try {
            const reportsUrl = './Report/menu_report.html';
            Logger.log(`Navegando a: ${reportsUrl}`);
            window.location.href = reportsUrl;
        } catch (error) {
            Logger.error('Error navegando a reportes:', error);
            
            // Fallback: intentar con API si está disponible
            if (window.pywebview?.api?.open_reports) {
                window.pywebview.api.open_reports();
            } else {
                alert('No se pudo abrir el módulo de reportes. Verifique la instalación.');
            }
        }
    }

    invokeOpenInventory() {
        if (window.pywebview?.api?.open_inventory) {
            window.pywebview.api.open_inventory();
        } else {
            Logger.log('Abriendo módulo de inventario...');
        }
    }

    invokeOpenCustomers() {
        if (window.pywebview?.api?.open_customers) {
            window.pywebview.api.open_customers();
        } else {
            Logger.log('Abriendo módulo de clientes...');
        }
    }

    invokeOpenSettings() {
        if (window.pywebview?.api?.open_settings) {
            Logger.log('Usando PyWebView API para abrir ajustes...');
            window.pywebview.api.open_settings();
        } else {
            Logger.log('PyWebView no disponible, navegando directamente a configuraciones...');
            // Navegación HTML directa
            window.location.href = './Settings/menu_settings.html';
        }
    }

    invokeOpenPrices() {
        if (window.pywebview?.api?.open_prices) {
            window.pywebview.api.open_prices();
        } else {
            Logger.log('Abriendo gestión de precios...');
        }
    }

    invokeExit() {
        if (confirm('¿Está seguro que desea salir del sistema?')) {
            if (window.pywebview?.api?.exit_application) {
                window.pywebview.api.exit_application();
            } else {
                Logger.log('Cerrando aplicación...');
                window.close();
            }
        }
    }

    simulateModuleLoad(module, buttonText, buttonElement) {
        Logger.log(`Simulando carga del módulo: ${module}`);
        
        setTimeout(() => {
            this.hideLoadingIndicator(buttonElement);
            
            if (module === 'exit') {
                if (confirm('¿Está seguro que desea salir del sistema?')) {
                    Logger.log('Cerrando aplicación en modo desarrollo');
                }
                return;
            }
            
            // Manejar navegación para módulos específicos en modo demostración
            if (module === 'sales') {
                Logger.log('Navegando a ventas en modo demostración');
                this.navigateToSales();
                return;
            }
            
            if (module === 'settings') {
                Logger.log('Navegando a configuraciones en modo demostración');
                this.navigateToSettings();
                return;
            }
            
            if (module === 'reports') {
                Logger.log('Navegando a reportes en modo demostración');
                this.navigateToReports();
                return;
            }
            
            this.showModuleMessage(buttonText);
        }, 1000);
    }

    showModuleMessage(buttonText) {
        const message = `Módulo ${buttonText} cargado correctamente (modo demostración)`;
        this.showNotification(message, 'success');
    }

    // Efectos visuales
    addHoverEffect(button) {
        button.style.transform = 'translateY(-3px)';
    }

    removeHoverEffect(button) {
        button.style.transform = 'translateY(0)';
    }

    addTouchEffect(button) {
        button.style.transform = 'scale(0.95)';
    }

    removeTouchEffect(button) {
        button.style.transform = 'scale(1)';
    }

    showLoadingIndicator(buttonElement) {
        const icon = buttonElement.querySelector('.button-icon');
        const originalIcon = icon.className;
        
        icon.className = 'button-icon fas fa-spinner fa-spin';
        buttonElement.style.pointerEvents = 'none';
        
        // Guardar el icono original para restaurarlo
        buttonElement.setAttribute('data-original-icon', originalIcon);
    }

    hideLoadingIndicator(buttonElement) {
        const icon = buttonElement.querySelector('.button-icon');
        const originalIcon = buttonElement.getAttribute('data-original-icon');
        
        if (originalIcon) {
            icon.className = originalIcon;
            buttonElement.removeAttribute('data-original-icon');
        }
        
        buttonElement.style.pointerEvents = 'auto';
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${type === 'error' ? '#e74c3c' : type === 'success' ? '#27ae60' : '#3498db'};
            color: white;
            padding: 1rem 1.5rem;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            z-index: 1000;
            font-weight: 500;
            max-width: 300px;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease;
        `;
        
        document.body.appendChild(notification);
        
        // Animar entrada
        setTimeout(() => {
            notification.style.opacity = '1';
            notification.style.transform = 'translateX(0)';
        }, 10);
        
        // Auto-remover después de 3 segundos
        setTimeout(() => {
            notification.style.opacity = '0';
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    showError(message) {
        this.showNotification(message, 'error');
        Logger.error('Error mostrado al usuario:', message);
    }

    showWelcomeAnimation() {
        const menuItems = document.querySelectorAll('.menu-item');
        menuItems.forEach((item, index) => {
            item.style.opacity = '0';
            item.style.transform = 'translateY(30px)';
            
            setTimeout(() => {
                AnimationManager.fadeIn(item, 400);
            }, index * 100);
        });
    }

    setupEventListeners() {
        // Eventos de teclado
        document.addEventListener('keydown', (e) => {
            this.handleKeyboardShortcuts(e);
        });

        // Manejo de errores globales
        window.addEventListener('error', (e) => {
            Logger.error('Error global capturado', e.error);
        });

        // Eventos de redimensionamiento
        window.addEventListener('resize', () => {
            this.handleResize();
        });
    }

    handleKeyboardShortcuts(e) {
        // Accesos directos con Alt + número
        if (e.altKey && !e.ctrlKey && !e.shiftKey) {
            const numbers = ['1', '2', '3', '4', '5', '6', '7'];
            const keyIndex = numbers.indexOf(e.key);
            
            if (keyIndex !== -1) {
                e.preventDefault();
                const menuItems = Object.values(this.menuButtons);
                if (menuItems[keyIndex]) {
                    menuItems[keyIndex].element.click();
                }
            }
        }
        
        // ESC para salir
        if (e.key === 'Escape') {
            const exitButton = this.menuButtons['SALIR'];
            if (exitButton) {
                exitButton.element.click();
            }
        }
    }

    setupResponsiveHandling() {
        // Detectar cambios en el viewport
        const mediaQuery = window.matchMedia('(max-width: 768px)');
        mediaQuery.addListener((e) => {
            if (e.matches) {
                Logger.log('Cambiando a vista móvil');
            } else {
                Logger.log('Cambiando a vista desktop');
            }
        });
    }

    handleResize() {
        // Manejar redimensionamiento de ventana
        Logger.log('Ventana redimensionada');
    }
}

// API para comunicación con Python
class PythonAPI {
    static isAvailable() {
        return typeof window.pywebview !== 'undefined' && window.pywebview.api;
    }
    
    static async callMethod(methodName, ...args) {
        if (!this.isAvailable()) {
            Logger.error('PyWebView API no disponible');
            return null;
        }
        
        try {
            const result = await window.pywebview.api[methodName](...args);
            Logger.log(`Método Python ${methodName} ejecutado`, result);
            return result;
        } catch (error) {
            Logger.error(`Error ejecutando método Python ${methodName}`, error);
            throw error;
        }
    }
}

// Inicializar la aplicación cuando la página esté lista
let salesSystemApp;

document.addEventListener('DOMContentLoaded', () => {
    salesSystemApp = new SalesSystemApp();
    Logger.log('Sales System App iniciada');
});

// Exportar para uso global
window.SalesSystemApp = SalesSystemApp;
window.PythonAPI = PythonAPI;