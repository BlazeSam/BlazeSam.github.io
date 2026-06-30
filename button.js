function showLogin() {
    document.getElementById("screen0").hidden = true;
    document.getElementById("screen1").hidden = false;
}

// Enter key (desktop)
window.addEventListener("keydown", (event) => {
    if (event.defaultPrevented) {
        return;
    }
    if (event.key === "Enter") {
        showLogin();
    }
});

// Tap / click (mobile + mouse) — click fires on touch too, no touch events needed
document.getElementById("screen0").addEventListener("click", showLogin);
