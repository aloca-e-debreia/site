document.addEventListener("DOMContentLoaded", () => {
    const summaries = document.querySelectorAll(".rent-summary");

    summaries.forEach(summary => {
        summary.addEventListener("click", () => {
            const id = summary.getAttribute("data-toggle");
            const details = document.getElementById(id);
            const parent = summary.parentElement;

            // fecha outros abertos
            document.querySelectorAll(".rent-item.open").forEach(openItem => {
                if (openItem !== parent) {
                    openItem.classList.remove("open");
                    openItem.querySelector(".rent-details").style.display = "none";
                }
            });

            // toggle
            parent.classList.toggle("open");
            details.style.display = parent.classList.contains("open") ? "block" : "none";
        });
    });
});
