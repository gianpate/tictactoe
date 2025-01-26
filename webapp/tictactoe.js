// 'x' is matched to player and 'o' is matched to computer
// tree has been loaded from the load.js file and is accesible through the tree variable

console.log('loaded')

// ------------help text-----------------------

const helpText = document.querySelector('.help-text');

setTimeout( () => {
        helpText.classList.remove('help-text-on');
    }, 9000)

helpTextButton = document.querySelector('.instruction-bnt')
helpTextButton.addEventListener('click', () => {
    helpText.classList.toggle('help-text-on');
})

// ----------------------------------------------




// ----------------------- score ------------------------------


const humanScoreElement = document.querySelector('.points-you');
const computerScoreElement = document.querySelector('.points-computer');

let humanScore = localStorage.getItem('score-human');
if (humanScore === null) {
    humanScore = 0; 
    localStorage.setItem('score-human', 0);
} else {
    humanScore = parseInt(humanScore);
     
}

let computerScore = localStorage.getItem('score-computer');
if (computerScore === null) {
    computerScore = 0; 
    localStorage.setItem('score-computer', 0); 
} else {
    computerScore = parseInt(computerScore);
    
}


humanScoreElement.textContent = humanScore;
computerScoreElement.textContent = computerScore;


function incrementHumanScore() {
    humanScore++;
    humanScoreElement.textContent = humanScore;
    localStorage.setItem('score-human', humanScore);
}

function incrementComputerScore() {
    computerScore++;
    computerScoreElement.textContent = computerScore;
    localStorage.setItem('score-computer', computerScore);
}


scoreBoard = document.querySelector('.score');
scoreBoard.addEventListener('click', () => {
    computerScore = 0;
    humanScore = 0;
    humanScoreElement.textContent = humanScore;
    computerScoreElement.textContent = computerScore;
    localStorage.setItem('score-human', humanScore);
    localStorage.setItem('score-computer', computerScore);
})


// ----------------------- score ------------------------------


// initialize players
player = '2';
computer = '1';



function faint(index) {
    document.querySelector(`#id-${index} .x`).classList.remove('x-on');
    document.querySelector(`#id-${index} .o`).classList.remove('o-on');
}


function startGame() {
    currentState = '000000000'; // global
    turn = '1'; // global
    subtree = tree; // global
    for (let i = 0; i < 9; i++) {
        faint(i);
    }
    if (computer == '1') {
        firstComputerMove(); 
    }
}

function prepareNewGame() {
    if (player == '2') {
        player = '1';
        computer = '2';
    } else if (player == '1') {
        player = '2';
        computer = '1';
    }
    startGame();
}



// ---------------- check for win ---------------------------------------------


function countZeros(state) {
    let count = 0
    for (let i = 0; i < 9; i++) {
        if (state[i] == '0') {
            count++
        }
    }
    return count
}


function win(state) {
    // if it is a winning state it returs an array with the winning positions
    // if it is a tie it returns 'tie'
    // else it returns 0

    const col1 = state[0] == state[3] && state[3] == state[6] && state[6] != '0';
    if (col1){
        return [0, 3, 6];
    }
    const col2 = state[1] == state[4] && state[4] == state[7] && state[7] != '0';
    if (col2){
        return [1, 4, 7];
    }
    const col3 = state[2] == state[5] && state[5] == state[8] && state[8] != '0';
    if (col3) {
        return [2, 5, 8];
    }
    const row1 = state[0] == state[1] && state[1] == state[2] && state[2] != '0';
    if (row1) {
        return [0, 1, 2];
    }
    const row2 = state[3] == state[4] && state[4] == state[5] && state[5] != '0';
    if (row2) { 
        return [3, 4, 5];
    }
    const row3 = state[6] == state[7] && state[7] == state[8] && state[8] != '0';
    if (row3) {
        return [6, 7, 8];
    }
    const main_diagonal = state[0] == state[4] && state[4] == state[8] && state[8] != '0';
    if (main_diagonal) {
        return [0, 4, 8];
    }
    const second_diagonal = state[2] == state[4] && state[4] == state[6] && state[6] != '0';
    if (second_diagonal) {
        return [2, 4, 6];
    }
    if (!countZeros(state)) {
        return 'tie'
    }
    return 0
}

// ---------------- check for win --------------------------------------------------------




// --------------------------manage win and tie -----------------------------------------


function handleWin(winArray, winner) {
    for (let i = 0; i < 9; i++) {
        if (!winArray.includes(i)) {
            faint(i);
        }
    }
    setTimeout(() => {
        if (winner == 'human'){
            incrementHumanScore();
        } else if (winner== 'computer'){
            incrementComputerScore();
        } 
        prepareNewGame();
    }, 2000)

}


function handleTie() {
    setTimeout(() => {
        prepareNewGame();
    }, 2000)
}


// --------------------------manage win and tie -----------------------------------------




// ----------------------------player move -----------------------------------------------

function playerMove(i) {
    if (i == 0) {
        return player + currentState.substring(i + 1, 9);
    } else if (i == 8) {
        return currentState.substring(0, i) + player;
    } else {
        return currentState.substring(0, i) + player + currentState.substring(i + 1);
    }
}

// ----------------------------player move -----------------------------------------------




// ---------------------------computer move ---------------------------------------------

function adjustComputer(current) {
    currentState = current
    for (const state of subtree[1]) {
        if (state[0] == current) {
            subtree = state;
            break
        }
    }
}


function chooseMove(moveList) {
    const len = moveList.length
    const probability = parseFloat((1 / len).toFixed(2));
    const rand = parseFloat(Math.random().toFixed(2));
    for (let i = 0; i < len; i++) {
        if ((i * probability) <= rand && rand < ((i+1) * probability)) {
            return moveList[i]
        }
    }
}


function getChange(s) {
    for (let i = 0; i < 9; i++) {
        if (currentState[i] != s[i]) {
            return i
        }
    }
}


function firstComputerMove() {
    setTimeout(() => {
        const rand = parseFloat(Math.random().toFixed(2));
        if (rand < 0.1) {
            let newState = chooseMove(["010000000", "000100000", "000001000", "000000010"]);
            let index = getChange(newState);
            document.querySelector(`#id-${index} .o`).classList.add('o-on');
            adjustComputer(newState);
        } else if(rand < 0.5) {
            let newState = "000010000";
            let index = getChange(newState);
            document.querySelector(`#id-${index} .o`).classList.add('o-on');
            adjustComputer(newState);
        } else {
            let newState = chooseMove(["100000000", "001000000", "000000100", "000000001"]);
            let index = getChange(newState);
            document.querySelector(`#id-${index} .o`).classList.add('o-on');
            adjustComputer(newState);
        }
        turn = player;
    }, 1200)
}


function computerMove() {
    setTimeout(() => {
        let newState = chooseMove(subtree[2]);
        let index = getChange(newState);
        document.querySelector(`#id-${index} .o`).classList.add('o-on');
        adjustComputer(newState);
        const w = win(currentState);
        if (Array.isArray(w)) {
            handleWin(w, 'computer');
        } else if (w == 'tie') {
            handleTie();
        } else if (w == 0) {
            turn = player;
        }    
    }, 1200)
}

// ---------------------------computer move ---------------------------------------------






function defineEventListeners() {
    for (let i = 0; i < 9; i++) {
        let cell = document.getElementById(`id-${i}`)
        cell.addEventListener('click', () => {
            if (turn == player) {
                if (currentState[i] == '0') {
                    let newState = playerMove(i);
                    turn = computer;
                    document.querySelector(`#id-${i} .x`).classList.add('x-on');
                    adjustComputer(newState);
                    const w = win(currentState);
                    if (Array.isArray(w)) {
                        turn = computer; // to block user from playing
                        handleWin(w, 'human');
                    } else if (w == 'tie') {
                        turn = computer; // to block user from playing
                        handleTie();
                    } else if (w == 0) {
                        computerMove();
                    }    
                }
            }
        })
    }
}

prepareNewGame();
defineEventListeners();

// fetch('tree.txt')
//     .then( response => {
//         if (!response.ok) {
//             throw new Error('Response was not ok ');
//         }
//         console.log('loaded');
//         return response.json();
//     })
//     .then(result => {
//         console.log('parsing');
//         tree = result; // global 
//         here we run the defineEventListeners function and 
//     })
//     .catch(error => {
//         console.error('Error:', error);
//     });






