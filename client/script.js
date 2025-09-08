let displayElement = null;
let currentExpression = '';
let lastResult = null;
let historyElement = null;

document.addEventListener('DOMContentLoaded', function() {
    initializeCalculator();
});

function initializeCalculator() {
    displayElement = document.getElementById('display');
    historyElement = document.getElementById('history-input');
    
    if (!displayElement || !historyElement) {
        console.error('Required calculator elements not found');
        return;
    }
    
    setupEventListeners();
    clearDisplay();
    refreshHistoryFromServer();
}

function setupEventListeners() {
    const digitButtons = document.querySelectorAll('.digits');
    digitButtons.forEach(button => {
        button.addEventListener('click', () => handleDigitInput(button.value));
    });
    
    const mathButtons = document.querySelectorAll('.mathButtons');
    mathButtons.forEach(button => {
        if (button.value === '=') {
            button.addEventListener('click', handleEquals);
        } else {
            button.addEventListener('click', () => handleOperatorInput(button.value));
        }
    });
    
    const bracketButtons = document.querySelectorAll('.BracketButtons');
    bracketButtons.forEach(button => {
        button.addEventListener('click', () => handleBracketInput(button.value));
    });
    
    const dotButton = document.querySelector('.dotButton');
    if (dotButton) {
        dotButton.addEventListener('click', () => handleDotInput());
    }
    
    const clearButton = document.getElementById('clearButton');
    if (clearButton) {
        clearButton.addEventListener('click', clearDisplay);
    }
    
    const delButton = document.querySelector('.delButton');
    if (delButton) {
        delButton.addEventListener('click', handleDelete);
    }
}

function handleDigitInput(digit) {
    if (lastResult !== null && currentExpression === lastResult.toString()) {
        currentExpression = '';
        lastResult = null;
    }
    currentExpression += digit;
    updateDisplay('right');
}

function handleOperatorInput(operator) {
    if (currentExpression === '' && operator === '-') {
        currentExpression += operator;
    } else if (currentExpression !== '') {
        const backendOperator = operator === 'x' ? '*' : operator;
        const lastChar = currentExpression.slice(-1);
        if (isOperator(lastChar)) {
            currentExpression = currentExpression.slice(0, -1) + backendOperator;
        } else {
            currentExpression += backendOperator;
        }
    }
    updateDisplay('right');
}

function handleBracketInput(bracket) {
    currentExpression += bracket;
    updateDisplay('right');
}

function handleDotInput() {
    const lastNumberMatch = currentExpression.match(/([0-9]*\.?[0-9]*)$/);
    const lastNumber = lastNumberMatch ? lastNumberMatch[0] : '';
    
    if (!lastNumber.includes('.')) {
        if (lastNumber === '' || isOperator(currentExpression.slice(-1))) {
            currentExpression += '0.';
        } else {
            currentExpression += '.';
        }
        updateDisplay('right');
    }
}

function handleDelete() {
    if (currentExpression.length > 0) {
        currentExpression = currentExpression.slice(0, -1);
        updateDisplay('right');
    }
}

function clearDisplay() {
    currentExpression = '';
    lastResult = null;
    updateDisplay('right');
}

function updateDisplay(scrollDirection = 'right') {
    displayElement.value = currentExpression;
    if (scrollDirection === 'left') {
        displayElement.scrollLeft = 0;
    } else {
        displayElement.scrollLeft = displayElement.scrollWidth;
    }
}

function isOperator(char) {
    return ['+', '-', '*', '/', 'x'].includes(char);
}

async function handleEquals() {
    if (currentExpression === '') {
        return;
    }
    
    try {
        const originalExpression = currentExpression;
        displayElement.value = 'Calculating...';
        
        const response = await fetch(`/calculate?expression=${encodeURIComponent(originalExpression)}`, {
            method: 'POST',
        });
        
        if (response.ok) {
            const data = await response.json();
            const result = data.result;
            currentExpression = result.toString();
            lastResult = result;
            updateDisplay('left');
            refreshHistoryFromServer();
                
        } else {
            const errorText = await response.text();
            displayElement.value = 'error';
            displayElement.scrollLeft = 0;
            refreshHistoryFromServer();
            setTimeout(() => {
                currentExpression = originalExpression;
                updateDisplay('right');
            }, 1000);
        }
        
    } catch (error) {
        console.error('Calculation error:', error);
        displayElement.value = 'error';
        displayElement.scrollLeft = 0;
        setTimeout(() => {
            currentExpression = originalExpression;
            updateDisplay('right');
        }, 2000);
    }
}


function bindHistoryLines() {
    document.querySelectorAll('.history-line').forEach(line => {
        line.addEventListener('click', function() {
            const full = this.innerHTML;
            const eqIndex = full.indexOf('=');
            const onlyExpression = eqIndex !== -1 ? full.slice(0, eqIndex).trim() : full;
            currentExpression = onlyExpression;
            updateDisplay();
        });
    });
}


async function refreshHistoryFromServer() {
    try {
        const resp = await fetch('/history');
        if (!resp.ok) return;
        const items = await resp.json();
        const list = Array.isArray(items) ? items.slice().reverse() : [];
        let value = "";
        list.forEach((expression, index) => {
            value += `<span class=\"history-line\">${expression}</span>`;
            if (index < list.length - 1) {
                value += `<span class=\"history-separator\" style=\"pointer-events:none; user-select:none; display:block; color:#888;\">-------</span>`;
            }
        })
        historyElement.innerHTML = value;
        bindHistoryLines();
        historyElement.scrollTop = 0;
    } catch (e) {
    }
}
