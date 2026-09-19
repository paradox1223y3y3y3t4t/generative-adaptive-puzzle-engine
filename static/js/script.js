document.addEventListener("DOMContentLoaded", function () {
    const timerElement = document.getElementById("timer");
    const responseTimeInput = document.getElementById("response-time");
    const puzzleForm = document.getElementById("puzzle-form");

    // Run timer only on the puzzle page.
    if (timerElement && responseTimeInput && puzzleForm) {
        const startTime = Date.now();

        setInterval(function () {
            const currentTime = Date.now();
            const seconds = Math.floor((currentTime - startTime) / 1000);

            timerElement.textContent = seconds;
            responseTimeInput.value = seconds;
        }, 1000);
    }
});