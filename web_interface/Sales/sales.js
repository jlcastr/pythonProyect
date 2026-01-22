// JavaScript para el Módulo de Ventas
// Sistema de Ventas S&M - Interfaz Web

class VentasManager {
    constructor() {
        this.productos = [];
        this.folio = null;
        this.cliente = "Consumidor Final";
        this.total = 0;
        this.productoEditando = -1;
        
        // Esperar a que el DOM esté listo
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => {
                this.initialize();
            });
        } else {
            this.initialize();
        }
    }
    
    initialize() {
        this.initializeElements();
        this.bindEvents();
        this.checkPyWebView();
        
        console.log("[Ventas] Módulo de ventas inicializado");
    }
    
    checkPyWebView() {
        // Verificar si PyWebView está disponible
        console.log("[DEBUG] ===== VERIFICANDO PYWEBVIEW =====");
        console.log("[DEBUG] typeof window.pywebview:", typeof window.pywebview);
        console.log("[DEBUG] window.pywebview:", window.pywebview);
        
        // Esperar un poco porque PyWebView puede tardar en cargar
        setTimeout(() => {
            console.log("[DEBUG] Verificación retrasada...");
            console.log("[DEBUG] typeof window.pywebview (retrasado):", typeof window.pywebview);
            console.log("[DEBUG] window.pywebview (retrasado):", window.pywebview);
            
            if (typeof window.pywebview !== 'undefined' && window.pywebview && window.pywebview.api) {
                console.log("[Ventas] ✅ PyWebView detectado correctamente");
                console.log("[DEBUG] window.pywebview.api:", window.pywebview.api);
                this.pywebviewReady = true;
            } else {
                console.log("[Ventas] ❌ PyWebView no disponible - Modo demostración");
                this.pywebviewReady = false;
            }
            console.log("[DEBUG] pywebviewReady FINAL:", this.pywebviewReady);
        }, 1000);
        
        // Verificación inmediata también
        if (typeof window.pywebview !== 'undefined' && window.pywebview && window.pywebview.api) {
            console.log("[Ventas] PyWebView detectado inmediatamente");
            this.pywebviewReady = true;
        } else {
            console.log("[Ventas] PyWebView no detectado inmediatamente");
            this.pywebviewReady = false;
        }
    }
    

    
    initializeElements() {
        // Elementos del DOM
        this.folioInput = document.getElementById('folio');
        this.clienteInput = document.getElementById('cliente');
        this.descripcionInput = document.getElementById('descripcion');
        this.precioInput = document.getElementById('precio');
        this.contadorProductos = document.getElementById('contador-productos');
        this.productosContainer = document.getElementById('productos-container');
        this.productosTabla = document.getElementById('productos-tabla');
        this.productosTbody = document.getElementById('productos-tbody');
        this.productosAcciones = document.getElementById('productos-acciones');
        this.finalizacionSection = document.getElementById('finalizacion-section');
        this.postVentaSection = document.getElementById('post-venta-section');
        this.totalVenta = document.getElementById('total-venta');
    }
    
    bindEvents() {
        // Enter en campos de entrada
        this.descripcionInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.precioInput.focus();
            }
        });
        
        this.precioInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.agregarProducto();
            }
        });
        
        // Validación de precio en tiempo real
        this.precioInput.addEventListener('input', (e) => {
            this.validarPrecio(e.target);
        });
        
        // Permitir teclas especiales en el campo de precio
        this.precioInput.addEventListener('keydown', (e) => {
            // Permitir: backspace, delete, tab, escape, enter
            if ([8, 9, 27, 13, 46].indexOf(e.keyCode) !== -1 ||
                // Permitir: Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+X
                (e.keyCode === 65 && e.ctrlKey === true) ||
                (e.keyCode === 67 && e.ctrlKey === true) ||
                (e.keyCode === 86 && e.ctrlKey === true) ||
                (e.keyCode === 88 && e.ctrlKey === true) ||
                // Permitir: home, end, left, right
                (e.keyCode >= 35 && e.keyCode <= 39)) {
                return;
            }
            // Permitir: números (0-9)
            if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
                // Permitir punto decimal (190 = . y 110 = . del teclado numérico)
                if (e.keyCode !== 190 && e.keyCode !== 110) {
                    e.preventDefault();
                }
            }
        });
        
        // Actualizar cliente
        this.clienteInput.addEventListener('change', (e) => {
            this.cliente = e.target.value.trim() || "Consumidor Final";
        });
    }
    
    validarPrecio(input) {
        let valor = input.value;
        
        // Permitir solo números, punto y coma
        valor = valor.replace(/[^0-9.,]/g, '');
        
        // Reemplazar coma por punto para estandarizar
        valor = valor.replace(/,/g, '.');
        
        // Permitir solo un punto decimal
        const partes = valor.split('.');
        if (partes.length > 2) {
            valor = partes[0] + '.' + partes[1];
        }
        
        // Limitar a 2 decimales máximo
        if (partes.length === 2 && partes[1].length > 2) {
            valor = partes[0] + '.' + partes[1].substring(0, 2);
        }
        
        // Actualizar el valor del campo
        input.value = valor;
    }
    
    generarFolio() {
        if (!this.folio) {
            const fecha = new Date();
            this.folio = fecha.getFullYear().toString().slice(-2) +
                        (fecha.getMonth() + 1).toString().padStart(2, '0') +
                        fecha.getDate().toString().padStart(2, '0') +
                        fecha.getHours().toString().padStart(2, '0') +
                        fecha.getMinutes().toString().padStart(2, '0') +
                        fecha.getSeconds().toString().padStart(2, '0');
            this.folioInput.value = this.folio;
        }
        return this.folio;
    }
    
    agregarProducto() {
        console.log('[DEBUG] ====== AGREGAR PRODUCTO INICIADO ======');
        
        const descripcion = this.descripcionInput.value.trim();
        const precioStr = this.precioInput.value.trim();
        
        console.log(`[DEBUG] Descripción: "${descripcion}", Precio: "${precioStr}"`);
        
        // Validaciones
        if (!descripcion) {
            this.mostrarNotificacion('La descripción no puede estar vacía', 'error');
            this.descripcionInput.focus();
            return;
        }
        
        if (!precioStr) {
            this.mostrarNotificacion('El precio no puede estar vacío', 'error');
            this.precioInput.focus();
            return;
        }
        
        // Permitir tanto punto como coma para decimales
        const precio = parseFloat(precioStr.replace(',', '.'));
        
        console.log(`[DEBUG] Precio convertido: ${precio} (tipo: ${typeof precio})`);
        
        if (isNaN(precio) || precio <= 0) {
            this.mostrarNotificacion('El precio debe ser un número mayor a cero', 'error');
            this.precioInput.focus();
            return;
        }
        
        // Generar folio si no existe
        this.generarFolio();
        
        // Crear producto
        const producto = {
            descripcion: descripcion,
            precio: precio,
            fecha: new Date().toLocaleString('es-MX'),
            folio: this.folio
        };
        
        if (this.productoEditando >= 0) {
            // Modificar producto existente
            this.productos[this.productoEditando] = producto;
            this.productoEditando = -1;
            this.mostrarNotificacion('Producto modificado correctamente', 'success');
        } else {
            // Agregar nuevo producto
            this.productos.push(producto);
            this.mostrarNotificacion('Producto agregado correctamente', 'success');
        }
        
        // Limpiar campos
        this.limpiarCampos();
        
        // Actualizar interfaz
        this.actualizarInterfaz();
        
        // Comunicar con Python si está disponible
        console.log('[DEBUG] Preparando para comunicar con Python...');
        console.log('[DEBUG] Producto a enviar:', producto);
        this.comunicarConPython('agregar_producto', producto)
            .then(resultado => {
                console.log('[DEBUG] Respuesta de Python recibida:', resultado);
            })
            .catch(error => {
                console.error('[DEBUG] Error en comunicación:', error);
            });
    }
    
    eliminarProducto(indice) {
        const producto = this.productos[indice];
        
        window.mostrarConfirmacion({
            titulo: 'Eliminar Producto',
            mensaje: '¿Está seguro de eliminar este producto?',
            detalles: `
                <p><strong>Producto:</strong> ${producto.descripcion}</p>
                <p><strong>Precio:</strong> $${producto.precio}</p>
            `,
            icono: 'fas fa-trash-alt',
            colorIcono: '#e74c3c',
            textoAceptar: 'Eliminar',
            iconoAceptar: 'fas fa-trash-alt',
            callback: () => {
                const productoEliminado = this.productos.splice(indice, 1)[0];
                this.mostrarNotificacion('Producto eliminado correctamente', 'success');
                this.actualizarInterfaz();
                
                // Comunicar con Python si está disponible
                this.comunicarConPython('eliminar_producto', { indice: indice, producto: productoEliminado }).catch(console.error);
            }
        });
    }
    
    editarProducto(indice) {
        const producto = this.productos[indice];
        
        this.descripcionInput.value = producto.descripcion;
        this.precioInput.value = producto.precio.toFixed(2);
        this.productoEditando = indice;
        
        this.descripcionInput.focus();
        this.mostrarNotificacion('Modificando producto. Presione Agregar para confirmar', 'success');
    }
    
    limpiarCampos() {
        this.descripcionInput.value = '';
        this.precioInput.value = '';
        this.productoEditando = -1;
        this.descripcionInput.focus();
    }
    
    limpiarTodo() {
        if (this.productos.length === 0) {
            this.mostrarNotificacion('No hay productos para limpiar', 'error');
            return;
        }
        
        window.mostrarConfirmacion({
            titulo: 'Limpiar Venta',
            mensaje: '¿Está seguro de limpiar todos los productos?',
            detalles: `
                <p><strong>Productos a eliminar:</strong> ${this.productos.length}</p>
                <p style="color: #e74c3c;">
                    <i class="fas fa-exclamation-triangle" style="margin-right: 0.5rem;"></i>
                    Esta acción no se puede deshacer
                </p>
            `,
            icono: 'fas fa-broom',
            colorIcono: '#f39c12',
            textoAceptar: 'Limpiar Todo',
            iconoAceptar: 'fas fa-broom',
            callback: () => {
                this.productos = [];
                this.folio = null;
                this.folioInput.value = '';
                this.cliente = "Consumidor Final";
                this.clienteInput.value = '';  // Limpiar el campo, no establecer valor
                this.limpiarCampos();
                this.actualizarInterfaz();
                this.mostrarNotificacion('Venta limpiada correctamente', 'success');
                
                // Comunicar con Python si está disponible
                this.comunicarConPython('limpiar_venta', {});
            }
        });
    }
    
    cancelarOperacion() {
        this.limpiarCampos();
        this.mostrarNotificacion('Operación cancelada', 'success');
    }
    
    finalizarVenta() {
        if (this.productos.length === 0) {
            this.mostrarNotificacion('No hay productos en la venta', 'error');
            return;
        }
        
        // Usar modal personalizado para confirmación
        const clienteActual = this.clienteInput.value.trim() || "Consumidor Final";
        
        window.mostrarConfirmacion({
            titulo: 'Finalizar Venta',
            mensaje: '¿Está seguro de finalizar la venta?',
            detalles: `
                <p><strong>Folio:</strong> ${this.folio}</p>
                <p><strong>Cliente:</strong> ${clienteActual}</p>
                <p><strong>Productos:</strong> ${this.productos.length}</p>
                <p><strong>Total:</strong> $${this.total.toFixed(2)}</p>
            `,
            icono: 'fas fa-question-circle',
            colorIcono: 'var(--primary-color)',
            textoAceptar: 'Finalizar Venta',
            iconoAceptar: 'fas fa-check',
            callback: () => {
                console.log(`[DEBUG] Cliente del objeto: "${this.cliente}"`);
                console.log(`[DEBUG] Cliente del input: "${clienteActual}"`);
                
                const ventaFinalizada = {
                    folio: this.folio,
                    cliente: clienteActual, // Usar el valor del input directamente
                    productos: [...this.productos],
                    total: this.total,
                fecha: new Date().toLocaleString('es-MX')
            };
            
            console.log(`[DEBUG] Enviando venta con cliente: "${ventaFinalizada.cliente}"`);
            
            // DEBUG: Mostrar toda la información que se va a enviar
            const debugInfo = {
                folio: this.folio,
                cliente: clienteActual,
                productos_count: this.productos.length,
                productos: this.productos,
                total: this.total
            };
            console.log('DATOS PARA BD:', JSON.stringify(debugInfo, null, 2));
            
            // Mostrar sección post-venta
            this.finalizacionSection.style.display = 'none';
            this.postVentaSection.style.display = 'block';
            
            this.mostrarNotificacion('Venta finalizada correctamente', 'success');
            
            // Comunicar con Python si está disponible
            this.comunicarConPython('finalizar_venta', ventaFinalizada);
            }
        });
    }
    
    imprimirVenta() {
        if (!this.folio) {
            this.mostrarNotificacion('No hay venta para imprimir', 'error');
            return;
        }
        
        this.mostrarNotificacion('Enviando venta a impresión...', 'success');
        
        // Comunicar con Python si está disponible
        this.comunicarConPython('imprimir_venta', { folio: this.folio });
    }
    
    enviarPorCorreo() {
        console.log('[DEBUG] enviarPorCorreo() llamado');
        console.log('[DEBUG] Folio actual:', this.folio);
        console.log('[DEBUG] Productos:', this.productos.length);
        
        if (!this.folio) {
            console.log('[DEBUG] No hay folio - mostrando error');
            this.mostrarNotificacion('Primero debe finalizar una venta para poder enviarla por correo', 'error');
            return;
        }
        
        console.log('[DEBUG] Mostrando modal de email');
        // Mostrar modal con información de la venta
        this.mostrarModalEmail();
    }
    
    nuevaVenta() {
        this.productos = [];
        this.folio = null;
        this.folioInput.value = '';
        this.cliente = "Consumidor Final";
        this.clienteInput.value = '';  // Limpiar el campo, no establecer valor
        this.limpiarCampos();
        
        // Ocultar secciones post-venta
        this.finalizacionSection.style.display = 'none';
        this.postVentaSection.style.display = 'none';
        
        this.actualizarInterfaz();
        this.mostrarNotificacion('Nueva venta iniciada', 'success');
    }
    
    actualizarInterfaz() {
        // Actualizar contador
        this.contadorProductos.textContent = this.productos.length;
        
        // Calcular total
        this.total = this.productos.reduce((sum, p) => sum + p.precio, 0);
        this.totalVenta.textContent = `$${this.total.toFixed(2)}`;
        
        if (this.productos.length === 0) {
            // Mostrar estado vacío
            this.productosContainer.style.display = 'block';
            this.productosTabla.style.display = 'none';
            this.productosAcciones.style.display = 'none';
            this.finalizacionSection.style.display = 'none';
        } else {
            // Mostrar tabla de productos
            this.productosContainer.style.display = 'none';
            this.productosTabla.style.display = 'table';
            this.productosAcciones.style.display = 'block';
            this.finalizacionSection.style.display = 'block';
            
            this.actualizarTablaProductos();
        }
    }
    
    actualizarTablaProductos() {
        this.productosTbody.innerHTML = '';
        
        this.productos.forEach((producto, indice) => {
            const fila = document.createElement('tr');
            
            fila.innerHTML = `
                <td>${producto.descripcion}</td>
                <td>$${producto.precio.toFixed(2)}</td>
                <td>${producto.fecha}</td>
                <td>
                    <button class="btn-sales btn-warning" onclick="ventasManager.editarProducto(${indice})" style="padding: 0.5rem; font-size: 0.9rem;">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn-sales btn-danger" onclick="ventasManager.eliminarProducto(${indice})" style="padding: 0.5rem; font-size: 0.9rem;">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;
            
            this.productosTbody.appendChild(fila);
        });
    }
    
    mostrarNotificacion(mensaje, tipo = 'success') {
        // Eliminar notificaciones existentes
        const notificacionesExistentes = document.querySelectorAll('.notification');
        notificacionesExistentes.forEach(n => n.remove());
        
        // Configurar iconos según el tipo
        const iconos = {
            'success': 'check-circle',
            'error': 'exclamation-circle',
            'warning': 'exclamation-triangle',
            'info': 'info-circle'
        };
        
        // Crear nueva notificación
        const notificacion = document.createElement('div');
        notificacion.className = `notification ${tipo}`;
        notificacion.innerHTML = `
            <i class="fas fa-${iconos[tipo] || 'info-circle'}"></i>
            <span class="notification-message">${mensaje}</span>
        `;
        
        document.body.appendChild(notificacion);
        
        // Mostrar con animación
        setTimeout(() => {
            notificacion.classList.add('show');
        }, 100);
        
        // Duración según tipo (errores y advertencias se muestran más tiempo)
        const duracion = (tipo === 'error' || tipo === 'warning') ? 5000 : 3000;
        
        // Ocultar después del tiempo especificado
        setTimeout(() => {
            notificacion.classList.remove('show');
            setTimeout(() => {
                if (notificacion.parentNode) {
                    notificacion.parentNode.removeChild(notificacion);
                }
            }, 300);
        }, duracion);
    }
    
    validarEmail(email) {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return regex.test(email);
    }
    
    async comunicarConPython(accion, datos) {
        // Comunicación con Python a través de PyWebView
        console.log(`[DEBUG] ===== INICIO comunicarConPython =====`);
        console.log(`[DEBUG] Acción: ${accion}`);
        console.log(`[DEBUG] Datos:`, datos);
        console.log(`[DEBUG] PyWebView Ready: ${this.pywebviewReady}`);
        console.log(`[DEBUG] window.pywebview existe:`, !!window.pywebview);
        
        if (!this.pywebviewReady) {
            console.log('[Ventas] Modo demostración - acción:', accion, datos);
            return { status: 'demo', message: 'Modo demostración' };
        }
        
        try {
            let resultado;
            console.log(`[DEBUG] Entrando al switch para acción: ${accion}`);
            
            // Llamar a la API de Python según la acción
            switch (accion) {
                case 'agregar_producto':
                    console.log(`[DEBUG] Case agregar_producto ejecutado`);
                    console.log(`[DEBUG] window.pywebview:`, !!window.pywebview);
                    console.log(`[DEBUG] window.pywebview.api:`, !!window.pywebview?.api);
                    console.log(`[DEBUG] sales_agregar_producto:`, !!window.pywebview?.api?.sales_agregar_producto);
                    
                    if (window.pywebview && window.pywebview.api && window.pywebview.api.sales_agregar_producto) {
                        console.log(`[DEBUG] Llamando sales_agregar_producto con:`, datos.descripcion, datos.precio.toString());
                        resultado = await window.pywebview.api.sales_agregar_producto(datos.descripcion, datos.precio.toString());
                        console.log(`[DEBUG] Resultado de sales_agregar_producto:`, resultado);
                    } else {
                        console.log(`[ERROR] API sales_agregar_producto no disponible`);
                    }
                    break;
                case 'eliminar_producto':
                    if (window.pywebview && window.pywebview.api && window.pywebview.api.sales_eliminar_producto) {
                        resultado = await window.pywebview.api.sales_eliminar_producto(datos.indice);
                    }
                    break;
                case 'limpiar_venta':
                    if (window.pywebview && window.pywebview.api && window.pywebview.api.sales_limpiar_venta) {
                        resultado = await window.pywebview.api.sales_limpiar_venta();
                    }
                    break;
                case 'finalizar_venta':
                    if (window.pywebview && window.pywebview.api && window.pywebview.api.sales_finalizar_venta) {
                        resultado = await window.pywebview.api.sales_finalizar_venta(datos.cliente);
                    }
                    break;
                case 'imprimir_venta':
                    if (window.pywebview && window.pywebview.api && window.pywebview.api.sales_imprimir_venta) {
                        resultado = await window.pywebview.api.sales_imprimir_venta();
                    }
                    break;
                case 'enviar_correo':
                    if (window.pywebview && window.pywebview.api && window.pywebview.api.sales_enviar_correo) {
                        console.log('[DEBUG] Llamando sales_enviar_correo con email:', datos.email);
                        resultado = await window.pywebview.api.sales_enviar_correo(datos.email);
                        console.log('[DEBUG] Resultado del envío:', resultado);
                        
                        // Procesar la respuesta
                        if (resultado) {
                            if (resultado.status === 'success') {
                                this.mostrarNotificacion(`✅ ${resultado.message}`, 'success');
                            } else if (resultado.status === 'warning') {
                                // Manejar caso especial de advertencia
                                if (resultado.action === 'show_demo_option') {
                                    this.mostrarNotificacion(`⚠️ ${resultado.message}\n${resultado.details || ''}`, 'warning');
                                } else {
                                    this.mostrarNotificacion(`⚠️ ${resultado.message}`, 'warning');
                                }
                            } else {
                                this.mostrarNotificacion(`❌ ${resultado.message || 'Error desconocido'}`, 'error');
                            }
                        } else {
                            this.mostrarNotificacion('❌ No se recibió respuesta del servidor', 'error');
                        }
                    }
                    break;
                default:
                    console.log('[Ventas] Acción no reconocida:', accion);
                    return { status: 'error', message: 'Acción no reconocida' };
            }
            
            console.log(`[DEBUG] ===== FIN comunicarConPython =====`);
            console.log('[DEBUG] Resultado final de Python:', resultado);
            return resultado;
            
        } catch (error) {
            console.error('[DEBUG] ===== ERROR comunicarConPython =====');
            console.error('[DEBUG] Error comunicando con Python:', error);
            console.error('[DEBUG] Stack trace:', error.stack);
            return { status: 'error', message: error.message || 'Error de comunicación' };
        }
    }
    
    // Funciones del modal de correo
    mostrarModalEmail() {
        console.log('[DEBUG] mostrarModalEmail() llamado');
        
        const modal = document.getElementById('emailModal');
        const folioSpan = document.getElementById('modal-folio');
        const clienteSpan = document.getElementById('modal-cliente');
        const totalSpan = document.getElementById('modal-total');
        const emailInput = document.getElementById('email-input');
        
        console.log('[DEBUG] Elementos del modal:', {
            modal: modal ? 'encontrado' : 'NO ENCONTRADO',
            folioSpan: folioSpan ? 'encontrado' : 'NO ENCONTRADO',
            clienteSpan: clienteSpan ? 'encontrado' : 'NO ENCONTRADO',
            totalSpan: totalSpan ? 'encontrado' : 'NO ENCONTRADO',
            emailInput: emailInput ? 'encontrado' : 'NO ENCONTRADO'
        });
        
        if (!modal) {
            console.error('[ERROR] Modal emailModal no encontrado en el DOM');
            alert('Error: Modal de correo no encontrado');
            return;
        }
        
        // Llenar información de la venta
        if (folioSpan) folioSpan.textContent = this.folio;
        if (clienteSpan) clienteSpan.textContent = this.cliente;
        if (totalSpan) totalSpan.textContent = this.formatearPrecio(this.total);
        
        // Limpiar campo de email
        if (emailInput) emailInput.value = '';
        
        console.log('[DEBUG] Mostrando modal con clase show');
        // Mostrar modal con animación
        modal.classList.add('show');
        
        // Verificar si se aplicó la clase
        console.log('[DEBUG] Modal classes después de show:', modal.className);
        
        // Enfocar el campo de email
        if (emailInput) {
            setTimeout(() => {
                emailInput.focus();
                console.log('[DEBUG] Enfoque aplicado al campo de email');
            }, 300);
        }
    }
    
    cerrarModalEmail() {
        const modal = document.getElementById('emailModal');
        modal.classList.remove('show');
    }
    
    confirmarEnvioEmail() {
        const emailInput = document.getElementById('email-input');
        const email = emailInput.value.trim();
        
        if (!email) {
            this.mostrarNotificacion('Por favor ingrese un correo electrónico', 'error');
            emailInput.focus();
            return;
        }
        
        if (!this.validarEmail(email)) {
            this.mostrarNotificacion('El formato del correo electrónico no es válido', 'error');
            emailInput.focus();
            emailInput.select();
            return;
        }
        
        // Cerrar modal
        this.cerrarModalEmail();
        
        // Mostrar notificación de envío
        this.mostrarNotificacion(`📧 Enviando venta a ${email}...`, 'info');
        
        // Comunicar con Python si está disponible
        this.comunicarConPython('enviar_correo', { 
            folio: this.folio, 
            email: email,
            cliente: this.cliente,
            total: this.total,
            productos: this.productos
        }).catch(error => {
            console.error('[DEBUG] Error en envío de correo:', error);
            this.mostrarNotificacion('❌ Error al enviar correo: ' + error.message, 'error');
        });
    }
}

// Funciones globales para los botones
function agregarProducto() {
    ventasManager.agregarProducto();
}

function cancelarOperacion() {
    ventasManager.cancelarOperacion();
}

function limpiarTodo() {
    ventasManager.limpiarTodo();
}

function finalizarVenta() {
    ventasManager.finalizarVenta();
}

function imprimirVenta() {
    ventasManager.imprimirVenta();
}

function enviarPorCorreo() {
    console.log('[DEBUG] Función global enviarPorCorreo() llamada');
    if (ventasManager) {
        console.log('[DEBUG] ventasManager existe, llamando método');
        ventasManager.enviarPorCorreo();
    } else {
        console.error('[ERROR] ventasManager no está disponible');
        alert('Error: Sistema de ventas no inicializado');
    }
}

function nuevaVenta() {
    ventasManager.nuevaVenta();
}

// Funciones del modal de correo
function cerrarModalEmail() {
    if (ventasManager) {
        ventasManager.cerrarModalEmail();
    }
}

function confirmarEnvioEmail() {
    if (ventasManager) {
        ventasManager.confirmarEnvioEmail();
    }
}

// Inicializar cuando el DOM esté listo
let ventasManager;

document.addEventListener('DOMContentLoaded', function() {
    ventasManager = new VentasManager();
    console.log('[Ventas] Sistema de ventas web inicializado');
    
    // Agregar eventos para el modal de correo
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const modal = document.getElementById('emailModal');
            if (modal && modal.classList.contains('show')) {
                cerrarModalEmail();
            }
        }
    });
    
    // Cerrar modal al hacer clic fuera de él
    const emailModal = document.getElementById('emailModal');
    if (emailModal) {
        emailModal.addEventListener('click', function(e) {
            if (e.target === this) {
                cerrarModalEmail();
            }
        });
    }
    
    // Enviar con Enter en el campo de email
    const emailInput = document.getElementById('email-input');
    if (emailInput) {
        emailInput.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                confirmarEnvioEmail();
            }
        });
    }
});

// Exportar para uso global
window.VentasManager = VentasManager;