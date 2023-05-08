let score = 0;
let timeLeft = 60;
const guessedWords = new Set();

const timer = setInterval(function () {
    timeLeft--;
    document.querySelector('#timer').innerText = `Time left: ${timeLeft}s`;

    if (timeLeft <= 0) {
        clearInterval(timer);
        endGame();
    }
}, 1000);

document.addEventListener('DOMContentLoaded', function () {
    document.querySelector('#guess-form').addEventListener('submit', async function (event) {
        event.preventDefault();

        if (timeLeft <= 0) {
            return;
        }

        const guessInput = document.querySelector('#guess');
        const guess = guessInput.value;

        if (!guess) {
            alert("Please enter a word.");
            return;
        }

        if (guessedWords.has(guess)) {
            alert("already-guessed");
            return;
        }

        const response = await axios.get('/check-word', {
            params: { word: guess }
        });

        if (response.data.result === "ok") {
            score += guess.length;
            document.querySelector('#score').innerText = `Score: ${score}`;
            guessedWords.add(guess);
            addGuessedWord(guess);
        } else {
            alert(response.data.result);
        }

        guessInput.value = '';
    });
});

async function endGame() {
    document.querySelector('#guess-form').disabled = true;
    document.querySelector('#guess').disabled = true;
    document.querySelector('#submit-btn').disabled = true;
    const response = await axios.post('/post-score', { score: score });
    document.querySelector('#plays').innerText = `Plays: ${response.data.plays}`;
    document.querySelector('#high-score').innerText = `High Score: ${response.data.high_score}`;

    const newGameButton = document.createElement('button');
    newGameButton.innerText = 'New Game';
    newGameButton.id = 'new-game';
    document.body.appendChild(newGameButton);

    newGameButton.addEventListener('click', function() {
        location.reload();
    });
}

function addGuessedWord(word) {
    const li = document.createElement('li');
    li.innerText = word;
    document.querySelector('#guessed-words').appendChild(li);
}
