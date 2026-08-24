document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('prediction-form');
    const hoursInput = document.getElementById('hours');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const spinner = submitBtn.querySelector('.spinner');
    
    const resultContainer = document.getElementById('result-container');
    const resultBadge = document.getElementById('result-badge');
    const resultText = document.getElementById('result-text');
    
    // Interactive Orbs (Follow Mouse)
    const orbs = document.querySelectorAll('.orb');
    document.addEventListener('mousemove', (e) => {
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;
        
        orbs.forEach((orb, index) => {
            const speed = (index + 1) * 20;
            const xOffset = (x - 0.5) * speed;
            const yOffset = (y - 0.5) * speed;
            orb.style.transform = `translate(${xOffset}px, ${yOffset}px)`;
        });
    });

    // Dynamic Button State
    hoursInput.addEventListener('input', () => {
        if (hoursInput.value > 0) {
            submitBtn.classList.add('ready');
        } else {
            submitBtn.classList.remove('ready');
        }
    });

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
        resultContainer.classList.remove('shake-animation'); // reset shake

        try {
            const response = await fetch(`/prediction?hours=${encodeURIComponent(hours)}`, {
                method: 'POST',
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            
            // Show Result container so animation can trigger
            resultContainer.classList.remove('hidden');

            if (data.status.toLowerCase() === 'pass') {
                resultBadge.classList.add('pass');
                resultText.textContent = 'PASS 🎉';
                
                // Trigger Confetti
                confetti({
                    particleCount: 100,
                    spread: 70,
                    origin: { y: 0.6 },
                    colors: ['#238636', '#58a6ff', '#ffffff']
                });
            } else {
                resultBadge.classList.add('fail');
                resultText.textContent = 'FAIL 💀';
                
                // Trigger Shake Effect
                resultContainer.classList.add('shake-animation');
            }
            
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
