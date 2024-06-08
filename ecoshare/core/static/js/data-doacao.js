document.addEventListener('DOMContentLoaded', (event) => {
    const dateField = document.getElementById('data');
    const today = new Date().toISOString().split('T')[0];
    dateField.value = today;
    dateField.readOnly = true;
});