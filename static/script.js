document.addEventListener('DOMContentLoaded', () => {
    // --- Landing Page Logic ---
    const startBtn = document.querySelector('.btn-primary');
    if (startBtn) {
        startBtn.addEventListener('click', () => {
            window.location.href = '/register';
        });
    }

    // --- Dashboard "New Scan" Logic ---
    const scanBtn = document.querySelector('.new-scan-btn');
    const statusText = document.querySelector('.status-text');

    if (scanBtn) {
        scanBtn.addEventListener('click', () => {
            // Visual feedback that the AI is working
            scanBtn.innerText = "Scanning...";
            scanBtn.disabled = true;
            scanBtn.style.opacity = "0.6";
            
            if(statusText) statusText.innerText = "Analyzing latest skills...";

            // Simulate the delay of an AI processing data
            setTimeout(() => {
                alert("Zenith AI: Scan complete. Matches updated based on your latest profile activity.");
                scanBtn.innerText = "New Scan";
                scanBtn.disabled = false;
                scanBtn.style.opacity = "1";
                if(statusText) statusText.innerText = "Analyzing profile...";
            }, 2000);
        });
    }
});