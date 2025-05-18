document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('userInfoForm');
    const gestacaoInfoDiv = document.getElementById('gestacaoInfo');
    const weekGestationInput = document.getElementById('week_gestation');
    const bebeInfoDiv = document.getElementById('bebeInfo');
    const babyNameInput = document.getElementById('baby_name');
    const babyAgeInput = document.getElementById('baby_age');

    const loadingDiv = document.getElementById('loading');
    const resultsSection = document.getElementById('results');

    const resultDivs = {
        //gestation_info: document.querySelector('#gestation_info_res pre'),
        //newborn_info: document.querySelector('#newborn_info_res pre'),
        //development_info: document.querySelector('#development_info_res pre'),
        //health_info: document.querySelector('#health_info_res pre'),
        refinement_info: document.querySelector('#refinement_info_res pre')
    };
    const resultContainerDivs = {
        //gestation_info: document.getElementById('gestation_info_res'),
        //newborn_info: document.getElementById('newborn_info_res'),
        //development_info: document.getElementById('development_info_res'),
        //health_info: document.getElementById('health_info_res'),
        refinement_info: document.getElementById('refinement_info_res')
    }


    document.querySelectorAll('input[name="is_gestation"]').forEach(radio => {
        radio.addEventListener('change', (event) => {
            if (event.target.value === 'sim') {
                gestacaoInfoDiv.classList.remove('hidden');
                weekGestationInput.required = true;
                bebeInfoDiv.classList.add('hidden');
                babyNameInput.required = false;
                babyAgeInput.required = false;
            } else {
                gestacaoInfoDiv.classList.add('hidden');
                weekGestationInput.required = false;
                bebeInfoDiv.classList.remove('hidden');
                babyNameInput.required = true;
                babyAgeInput.required = true;
            }
        });
    });

    form.addEventListener('submit', async (event) => {
        event.preventDefault();
        loadingDiv.classList.remove('hidden');
        resultsSection.classList.add('hidden');
        // Esconder todas as caixas de resultado individuais
        Object.values(resultContainerDivs).forEach(div => div.classList.add('hidden'));


        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        try {
            // Use http://127.0.0.1:5000 ou o endereço do seu servidor Flask
            const response = await fetch('/api/process_info', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            loadingDiv.classList.add('hidden');

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }

            const results = await response.json();
            displayResults(results);
            resultsSection.classList.remove('hidden');

        } catch (error) {
            loadingDiv.classList.add('hidden');
            alert('Erro ao processar informações: ' + error.message);
            console.error('Erro:', error);
        }
    });

    function displayResults(results) {
        for (const key in resultDivs) {
            if (results[key]) {
                resultDivs[key].textContent = results[key];
                resultContainerDivs[key].classList.remove('hidden');
            } else {
                 resultContainerDivs[key].classList.add('hidden');
            }
        }
    }

    // Service Worker Registration
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/service-worker.js')
                .then(registration => {
                    console.log('ServiceWorker registration successful with scope: ', registration.scope);
                })
                .catch(err => {
                    console.log('ServiceWorker registration failed: ', err);
                });
        });
    }

    // Atualizar ano no rodapé
    document.getElementById('currentYear').textContent = new Date().getFullYear();
});