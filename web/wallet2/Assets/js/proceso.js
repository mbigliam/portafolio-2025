$(document).ready(function() {

    // ==========================================
    // FUNCIONES GLOBALES Y SALDOS (Aplica a todas las pantallas)
    // ==========================================
    if (!localStorage.getItem("balances")) {
      localStorage.setItem("balances", JSON.stringify({ current: 600000, credit: 4800725 }));
    }
  
    function formatMoney(v) {
      return "$" + Number(v).toLocaleString("es-CL");
    }
  
    function updateSaldos() {
      const balances = JSON.parse(localStorage.getItem("balances"));
      // Verificamos si los IDs existen en la página actual antes de actualizar
      if ($('#currentBalance').length) $('#currentBalance').text(formatMoney(balances.current));
      if ($('#creditBalance').length) $('#creditBalance').text(formatMoney(balances.credit));
    }
  
    // Actualiza la UI de saldos inmediatamente al cargar
    updateSaldos();
  
  
    // ==========================================
  // LÓGICA: DEPOSIT.HTML
  // ==========================================
  if ($('#depositForm').length) {
    
    // NUEVO: Formatear input con separador de miles al escribir
    $('#depositAmount').on('input', function() {
      // 1. Quitar cualquier cosa que no sea número (letras, puntos, etc.)
      let valorLimpio = $(this).val().replace(/\D/g, '');
      
      // 2. Si hay números, ponerles el formato de miles chileno (con puntos)
      if (valorLimpio !== '') {
        $(this).val(Number(valorLimpio).toLocaleString('es-CL'));
      } else {
        $(this).val('');
      }
    });

    // Envío del formulario
    $('#depositForm').submit(function(e) {
      e.preventDefault();

      const account = $('#accountSelect').val();
      
      // MODIFICADO: Tomamos el texto, le quitamos los puntos y lo convertimos a número decimal
      const amountText = $('#depositAmount').val().replace(/\./g, ''); 
      const amount = parseFloat(amountText);

      if (!amount || amount <= 0) {
        $('#depositMessage').html('<div class="alert alert-danger">Ingrese un monto válido.</div>');
        return;
      }

      const balances = JSON.parse(localStorage.getItem("balances"));
      balances[account] = (balances[account] || 0) + amount;
      localStorage.setItem("balances", JSON.stringify(balances));

      // Registrar movimiento
      const movimientos = JSON.parse(localStorage.getItem("movimientos") || "[]");
      movimientos.unshift({
        tipo: `Depósito ${account === 'current' ? 'Cuenta Corriente' : 'Tarjeta de Crédito'}`,
        monto: amount,
        fecha: new Date().toLocaleString()
      });
      localStorage.setItem("movimientos", JSON.stringify(movimientos));

      // Actualizar UI
      updateSaldos();

      $('#depositMessage').html(`
        <div class="alert alert-success">Depósito realizado correctamente.</div>
        <p class="text-success text-center fw-bold mt-2">Monto depositado: ${formatMoney(amount)}</p>
      `);
      
      $('#depositForm')[0].reset(); 
      
      // Redireccionar
      setTimeout(function() { window.location.href = 'menu.html'; }, 2000);
    });
  }
  
  
    // ==========================================
    // LÓGICA: SENDMONEY.HTML
    // ==========================================
    if ($('#btnGuardar').length || $('#btnTransfer').length) {
      
      let contactoSeleccionado = null;

      // NUEVO: Formatear input con separador de miles al escribir en transferencias
      $('#transferAmount').on('input', function() {
        let valorLimpio = $(this).val().replace(/\D/g, '');
        if (valorLimpio !== '') {
          $(this).val(Number(valorLimpio).toLocaleString('es-CL'));
        } else {
          $(this).val('');
        }
      });
      // Renderizar contactos
      function renderContacts() {
        const contactos = JSON.parse(localStorage.getItem("contactos") || "[]");
        const $tbody = $('#tablaContactos tbody');
        $tbody.empty(); // Limpiamos la tabla
        
        contactos.forEach(c => {
          const fila = `
            <tr>
              <td>${c.nombre}</td>
              <td>${c.alias || "-"}</td>
              <td>${c.banco || "-"}</td>
              <td>****${(c.cuenta || "").slice(-4)}</td>
              <td><input class="form-check-input" type="radio" name="contact"></td>
            </tr>
          `;
          $tbody.append(fila);
        });
      }
  
      renderContacts();
  
      // Guardar nuevo contacto
      $('#btnGuardar').click(function() {
        const nombre = $('#nombre').val().trim();
        const alias = $('#alias').val().trim();
        const banco = $('#banco').val().trim();
        const cuenta = $('#cuenta').val().trim();
  
        if (!nombre || !cuenta) {
          Swal.fire("Error", "Nombre y cuenta son obligatorios", "error");
          return;
        }
  
        let contactos = JSON.parse(localStorage.getItem("contactos")) || [];
        contactos.push({ nombre, alias, banco, cuenta });
        localStorage.setItem("contactos", JSON.stringify(contactos));
  
        renderContacts();
  
        // Limpiar inputs
        $('#nombre, #alias, #banco, #cuenta').val('');
        $('#modalNuevo').modal('hide'); // Cierra el modal con Bootstrap/jQuery
        
        Swal.fire({ icon: "success", title: "Contacto guardado", timer: 1200, showConfirmButton: false });
      });
  
      // Búsqueda en la tabla
      $('#searchContact').on('input', function() {
        const texto = $(this).val().toLowerCase().trim();
        $('#tablaContactos tbody tr').each(function() {
          const contenido = $(this).text().toLowerCase();
          // toggle muestra u oculta según si la condición es true o false
          $(this).toggle(contenido.includes(texto)); 
        });
      });
  
      // Seleccionar contacto (usamos delegación de eventos .on en la tabla)
      $('#tablaContactos').on('change', 'input[name="contact"]', function() {
        const $fila = $(this).closest('tr');
        const $celdas = $fila.find('td');
  
        contactoSeleccionado = {
          nombre: $celdas.eq(0).text(),
          alias: $celdas.eq(1).text(),
          banco: $celdas.eq(2).text(),
          cuenta: $celdas.eq(3).text()
        };
  
        $('.border.rounded-3.p-3').html(`
          <div class="fw-bold">${contactoSeleccionado.nombre}</div>
          <div class="contact-details">
            Alias: ${contactoSeleccionado.alias} <br>
            Banco: ${contactoSeleccionado.banco} <br>
            Cuenta: ${contactoSeleccionado.cuenta}
          </div>
        `);
      });
  
     // Enviar dinero
    $('#btnTransfer').click(function() {
      
      // 1. Capturamos lo que el usuario ve en pantalla (Ej: "500.000")
      let valorPantalla = $('#transferAmount').val();
      
      // 2. Le quitamos TODOS los puntos usando una expresión regular global (Queda "500000")
      let valorSinPuntos = valorPantalla.replace(/\./g, '');
      
      // 3. Ahora sí, convertimos el texto limpio a número real para la matemática
      const monto = parseFloat(valorSinPuntos);

      // Verificación de seguridad
      if (!monto || monto <= 0) {
        Swal.fire("Error", "Ingresa un monto válido", "error");
        return;
      }

      const origen = $('#originAccount').val();
      const destinoCuenta = $('#destinationAccount').val();
      let balances = JSON.parse(localStorage.getItem("balances"));

      if (!balances[origen] || balances[origen] < monto) {
        Swal.fire("Fondos insuficientes", "No tienes saldo suficiente", "error");
        return;
      }

      const movimientos = JSON.parse(localStorage.getItem("movimientos") || "[]");

      if (contactoSeleccionado) {
        // Transferencia externa
        balances[origen] -= monto;
        movimientos.unshift({ tipo: `Transferencia a ${contactoSeleccionado.nombre}`, monto: -monto, fecha: new Date().toLocaleString() });
        
        Swal.fire({
          icon: "success",
          title: "Transferencia realizada",
          html: `<b>Destino:</b> ${contactoSeleccionado.nombre}<br><b>Monto:</b> ${formatMoney(monto)}`
        });
      } else {
        // Transferencia interna
        if (origen === destinoCuenta) {
          Swal.fire("Error", "Selecciona cuentas diferentes", "error");
          return;
        }
        balances[origen] -= monto;
        balances[destinoCuenta] = (balances[destinoCuenta] || 0) + monto;
        movimientos.unshift({ tipo: `Transferencia entre cuentas (${origen} → ${destinoCuenta})`, monto: -monto, fecha: new Date().toLocaleString() });

        Swal.fire({
          icon: "success",
          title: "Transferencia interna realizada",
          html: `<b>Origen:</b> ${origen}<br><b>Destino:</b> ${destinoCuenta}<br><b>Monto:</b> ${formatMoney(monto)}`
        });
      }

      localStorage.setItem("balances", JSON.stringify(balances));
      localStorage.setItem("movimientos", JSON.stringify(movimientos));
      
      updateSaldos();
      $('#transferAmount').val('');
    });
    }
  
  
    // ==========================================
    // LÓGICA: TRANSACTIONS.HTML
    // ==========================================
    if ($('#lista').length) {
      const movimientos = JSON.parse(localStorage.getItem("movimientos")) || [];
      const $lista = $('#lista');
      
      if (movimientos.length > 0) {
        // Opcional: $lista.empty(); si deseas borrar el HTML estático antes de inyectar
        
        movimientos.forEach(m => {
          // Evaluar si es ingreso por la palabra o porque el monto es positivo
          const esIngreso = m.tipo.toLowerCase().includes('depósito') || m.tipo.toLowerCase().includes('recibida') || m.tipo.toLowerCase().includes('ingreso') || m.monto > 0;
          const iconClass = esIngreso ? 'icon-ingreso' : 'icon-egreso';
          const icon = esIngreso ? 'bi-arrow-down-left' : 'bi-arrow-up-right';
          const montoClass = esIngreso ? 'monto-ingreso' : 'monto-egreso';
          
          // Formateo del signo
          const signo = esIngreso ? '+' : (m.monto > 0 ? '-' : ''); 
          
          $lista.append(`
            <li class="list-group-item">
              <div class="movimiento-info">
                <div class="icon-box ${iconClass}"><i class="bi ${icon}"></i></div>
                <div>
                  <span class="d-block fw-semibold text-dark">${m.tipo}</span>
                  <small class="text-muted">${m.fecha}</small>
                </div>
              </div>
              <span class="${montoClass}">${signo}${formatMoney(Math.abs(m.monto))}</span>
            </li>
          `);
        });
      }
    }
  
  });