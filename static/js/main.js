window.addEventListener("load", () => {
    const loader = document.getElementById("loader");
    if (loader) loader.style.display = "none";

    const progressBars = document.querySelectorAll(".progress-bar[aria-valuenow]");
    progressBars.forEach((bar) => {
        const value = Number.parseFloat(bar.getAttribute("aria-valuenow") || "0");
        const clamped = Number.isFinite(value) ? Math.max(0, Math.min(100, value)) : 0;
        bar.style.width = `${clamped}%`;
    });
});

// Dark mode
const toggleBtn = document.getElementById("darkModeToggle");
if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
        const html = document.documentElement;
        const current = html.getAttribute("data-theme");
        html.setAttribute("data-theme", current === "dark" ? "light" : "dark");
    });
}

// Pomodoro
let timer;
let timeLeft = 25 * 60;
let isBreak = false;

function updateDisplay() {
    const display = document.getElementById("timerDisplay");
    if (!display) return;
    const min = String(Math.floor(timeLeft / 60)).padStart(2, "0");
    const sec = String(timeLeft % 60).padStart(2, "0");
    display.textContent = `${min}:${sec}`;
}

function startPomodoro() {
    if (timer) return;
    timer = setInterval(() => {
        timeLeft--;
        updateDisplay();
        if (timeLeft <= 0) {
            clearInterval(timer);
            timer = null;
            alert(isBreak ? "Break over! Back to study." : "Study session complete! Take a 5 min break.");
            isBreak = !isBreak;
            timeLeft = isBreak ? 5 * 60 : 25 * 60;
            updateDisplay();
        }
    }, 1000);
}

function resetPomodoro() {
    clearInterval(timer);
    timer = null;
    isBreak = false;
    timeLeft = 25 * 60;
    updateDisplay();
}
updateDisplay();

window.startPomodoro = startPomodoro;
window.resetPomodoro = resetPomodoro;