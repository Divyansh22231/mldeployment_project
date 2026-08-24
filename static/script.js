document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const hoursInput = document.getElementById('hours');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const spinner = submitBtn.querySelector('.spinner');
    
    const resultContainer = document.getElementById('result-container');
    const resultBadge = document.getElementById('result-badge');
    const resultText = document.getElementById('result-text');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const hours = hoursInput.value;
        if (!hours) return;

        // UI Loading State
        btnText.textContent = 'Predicting...';
        spinner.classList.remove('hidden');
        submitBtn.disabled = true;
        resultContainer.classList.add('hidden');
        resultBadge.className = ''; // reset classes

        try {
            // Call the existing FastAPI endpoint
            // Notice how we pass hours as a query parameter because that's what the backend expects
            const response = await fetch(`/prediction?hours=${encodeURIComponent(hours)}`, {
                method: 'POST',
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            // Handle Response (e.g. {"prediction": 1.0, "status": "Pass"})
            if (data.status.toLowerCase() === 'pass') {
                resultBadge.classList.add('pass');
                resultText.textContent = 'Pass';
            } else {
                resultBadge.classList.add('fail');
                resultText.textContent = 'Fail';
            }

            // Show Result
            resultContainer.classList.remove('hidden');
            
        } catch (error) {
            console.error('Error during prediction:', error);
            alert('Something went wrong. Please check the console or ensure your API is running.');
        } finally {
            // Reset UI Loading State
            btnText.textContent = 'Predict Now';
            spinner.classList.add('hidden');
            submitBtn.disabled = false;
        }
    });
});
