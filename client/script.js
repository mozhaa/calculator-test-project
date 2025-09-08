let displayElement = null;
let currentExpression = '';
let lastResult = null;

document.addEventListener('DOMContentLoaded', function() {
    initializeCalculator();
});

function initializeCalculator() {
    displayElement = document.getElementById('display');
    
    if (!displayElement) {
        console.error('Required calculator elements not found');
        return;
    }
    
    setupEventListeners();
    clearDisplay();
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
    updateDisplay();
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
    updateDisplay();
}

function handleBracketInput(bracket) {
    currentExpression += bracket;
    updateDisplay();
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
        updateDisplay();
    }
}

function handleDelete() {
    if (currentExpression.length > 0) {
        currentExpression = currentExpression.slice(0, -1);
        updateDisplay();
    }
}

function clearDisplay() {
    currentExpression = '';
    lastResult = null;
    updateDisplay();
}

function updateDisplay() {
    displayElement.value = currentExpression;
    displayElement.scrollLeft = displayElement.scrollWidth;
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
            updateDisplay();
                
        } else {
            const errorText = await response.text();
            displayElement.value = 'Error';
            
            setTimeout(() => {
                currentExpression = originalExpression;
                updateDisplay();
            }, 2000);
        }
        
    } catch (error) {
        console.error('Calculation error:', error);
        displayElement.value = 'Error';
        
        setTimeout(() => {
            updateDisplay();
        }, 2000);
    }
}
