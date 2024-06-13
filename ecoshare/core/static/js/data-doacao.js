document.addEventListener('DOMContentLoaded', (event) => {
    const dateField = document.getElementById('data');

    const now = new Date();
    const options = { timeZone: 'America/Sao_Paulo', year: 'numeric', month: '2-digit', day: '2-digit' };
    const brazilDate = new Intl.DateTimeFormat('en-CA', options).format(now);

    dateField.value = brazilDate;
    dateField.readOnly = true;
});
