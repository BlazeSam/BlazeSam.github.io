
window.addEventListener("keydown", (event) => {
    if (event.defaultPrevented) {
        return;
    }

    if (event.key === "Enter") {
        document.getElementById("screen0").setAttribute("hidden", "");
        document.getElementById("screen1").removeAttribute("hidden", "");
    }
});
