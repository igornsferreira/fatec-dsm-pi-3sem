document.addEventListener('DOMContentLoaded', function() {
    var paisInput = document.getElementById('pais');
    if (!paisInput.value) {
        paisInput.value = 'Brasil';
    }

    // Função para consultar o CEP
    function consultaCEP() {
        const cep = document.getElementById('cep').value.replace(/\D/g, '');
        if (cep.length === 8) {
            fetch(`https://viacep.com.br/ws/${cep}/json/`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('CEP não encontrado');
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.erro) {
                        throw new Error('CEP não encontrado');
                    } else {
                        document.getElementById('rua').value = data.logradouro || '';
                        document.getElementById('bairro').value = data.bairro || '';
                        document.getElementById('cidade').value = data.localidade || '';
                        document.getElementById('estado').value = data.uf || '';
                    }
                })
                .catch(error => {
                    console.error('Erro ao buscar CEP:', error);
                });
        }
    }

    // Adicionar evento ao campo de CEP
    document.getElementById('cep').addEventListener('blur', consultaCEP);

    // Deixar input date transparente
    var dateInput = document.querySelector('#cadastro form input[type="date"]');
    updateDateInputState(dateInput);

    dateInput.addEventListener('input', function() {
        updateDateInputState(dateInput);
    });

    function updateDateInputState(input) {
        if (input.value) {
            input.classList.remove('empty');
        } else {
            input.classList.add('empty');
        }
    }
});