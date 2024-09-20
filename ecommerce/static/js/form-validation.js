document.addEventListener("DOMContentLoaded", function() {
  const userTypeField = document.querySelectorAll('input[name="user-type"]');
  const clienteFields = document.querySelector('.cliente-fields');
  const venditoreFields = document.querySelector('.venditore-fields');

  function toggleFields() {
    if (document.querySelector('input[name="user-type"]:checked').value === 'CLIENTE') {
      clienteFields.style.display = 'block';
      venditoreFields.style.display = 'none';
    } else {
      clienteFields.style.display = 'none';
      venditoreFields.style.display = 'block';
    }
  }

  // Inizializzazione
  toggleFields();

  // Aggiungi event listener per ogni radio button
  userTypeField.forEach(radio => {
    radio.addEventListener('change', toggleFields);
  });
});
