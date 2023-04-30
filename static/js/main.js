const form = document.getElementById('essay-form');
const scoreContainer = document.getElementById('score-container');

form.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(form);

    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        scoreContainer.innerHTML = `<h2>Essay Score: ${data.score}</h2>`;
    })
    .catch(error => {
        console.error(error);
    });
});
