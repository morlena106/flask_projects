document.addEventListener("DOMContentLoaded", () => {
    const surpriseButton = document.querySelector(".funny-surprise");

    surpriseButton.addEventListener("click", () => {
        const form = document.querySelector(".funny-form");
        const surpriseMessage = document.createElement("p");
        surpriseMessage.textContent = "🎉 You found the secret! 🎉";
        surpriseMessage.style.color = "#ff4500";
        surpriseMessage.style.fontSize = "1.5rem";
        form.appendChild(surpriseMessage);
        surpriseButton.disabled = true;
    });
});
