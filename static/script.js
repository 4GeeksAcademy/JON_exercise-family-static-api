// script.js

// 1) URL base de la API. Si corres localmente:
// const baseURL = 'http://127.0.0.1:5000';
// En Codespaces o GitHub.dev, reemplaza con tu dominio real.
// Para que funcione "en todos lados", podemos usar la URL relativa:
const baseURL = window.location.origin;

// Referencias al DOM
const btnGet = document.getElementById('btn-get');
const btnPost = document.getElementById('btn-post');
const inputFirstName = document.getElementById('new-first-name');
const memberListEl = document.getElementById('member-list');
const emptyMessageEl = document.getElementById('empty-message');

/**
 * 1. fetchMembers(): hace GET /members y renderiza la lista de miembros en el UL.
 */
async function fetchMembers() {
  try {
    const resp = await fetch(`${baseURL}/members`);
    if (!resp.ok) {
      alert('Error al obtener miembros: ' + resp.status);
      return;
    }
    const members = await resp.json();

    // Si no hay miembros, muestra mensaje
    if (members.length === 0) {
      memberListEl.innerHTML = '';
      emptyMessageEl.textContent = 'No hay miembros en la familia.';
      return;
    }

    // Hay miembros: ocultamos el mensaje y pintamos la lista
    emptyMessageEl.textContent = '';
    memberListEl.innerHTML = ''; // limpiamos

    members.forEach((member) => {
      const li = document.createElement('li');

      // Texto: "John Jackson (33 años) — Lucky: [7, 13, 22]"
      const spanText = document.createElement('span');
      spanText.textContent = `${member.first_name} ${member.last_name} (edad: ${member.age}) — Lucky: [${member.lucky_numbers.join(', ')}]`;

      li.appendChild(spanText);

      // Botón DELETE /members/:id
      const btnDel = document.createElement('button');
      btnDel.textContent = `DELETE /members/${member.id}`;
      btnDel.className = 'btn-delete';
      btnDel.onclick = async () => {
        try {
          const delResp = await fetch(`${baseURL}/members/${member.id}`, {
            method: 'DELETE'
          });
          if (!delResp.ok) {
            const err = await delResp.json();
            alert('Error al borrar: ' + (err.error || delResp.status));
            return;
          }
          // Al borrar con éxito, recargamos la lista
          fetchMembers();
        } catch (error) {
          console.error(error);
          alert('Error en la petición de borrado.');
        }
      };

      li.appendChild(btnDel);
      memberListEl.appendChild(li);
    });
  } catch (error) {
    console.error(error);
    memberListEl.innerHTML = '<li>Error al cargar la lista.</li>';
  }
}

/**
 * 2. createMember(): toma el primer nombre del input y envía un POST /members
 *    con datos mínimos. (Aquí fijamos age=20 y lucky_numbers aleatorios a modo demo.)
 */
async function createMember() {
  const fname = inputFirstName.value.trim();
  if (!fname) {
    alert('Escribe un nombre para el nuevo miembro.');
    return;
  }
  try {
    // Por simplicidad, asignamos edad = 20 y lucky_numbers = [Math.random()...]
    // Tú puedes cambiarlo para pedir más campos en un formulario más completo.
    const payload = {
      first_name: fname,
      age: 20,
      lucky_numbers: [ Math.floor(Math.random() * 50) + 1 ]
    };

    const resp = await fetch(`${baseURL}/members`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (resp.ok) {
      // Limpiamos input y recargamos lista
      inputFirstName.value = '';
      fetchMembers();
    } else {
      const err = await resp.json();
      alert('Error al crear: ' + (err.error || resp.status));
    }
  } catch (error) {
    console.error(error);
    alert('Error en la petición de creación.');
  }
}

// 3) Asociamos los botones con las funciones
btnGet.addEventListener('click', fetchMembers);
btnPost.addEventListener('click', createMember);

// Nota: Podrías llamar a fetchMembers() automáticamente cuando cargue la página.
// Por ejemplo, descomenta esta línea si quieres que al abrir index.html ya se muestre la lista:
// window.addEventListener('DOMContentLoaded', fetchMembers);
