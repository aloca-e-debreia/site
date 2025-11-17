const input = document.getElementById("filter");
const carros = document.querySelectorAll(".carro");
const filterCategory = document.getElementById("filterCategory");
const filterFuel = document.getElementById("filterFuel");
const noResults = document.getElementById("SemResultados");

function verificarResultados() {
    const algumVisivel = Array.from(carros).some(carro => carro.style.display !== "none");
    carros.forEach(carro => {
        if (!algumVisivel) {
            noResults.style.display = "block";
        } else {
            noResults.style.display = "none";
    }})
}

input.addEventListener("input", function () {
    const texto = input.value.toLowerCase();

    carros.forEach(carro => {
        const nome = carro.querySelector(".vehicleName").innerText.toLowerCase();

        if (nome.includes(texto)) {
            carro.style.display = "block";
        } else {
            carro.style.display = "none";
        }
    });
    verificarResultados()
});
    

function filtrar() {
    const categoria = filterCategory.value.toLowerCase();
    const fuel = filterFuel.value.toLowerCase();

    carros.forEach(carro => {
        const carroCategoria = carro.querySelector("#category").innerText.toLowerCase();
        const carroFuel = carro.querySelector("li").innerText.toLowerCase(); 

        const matchCategoria = categoria === "" || carroCategoria.includes(categoria);
        const matchFuel = fuel === "" || carroFuel.includes(fuel);

        if (matchCategoria && matchFuel) {
            carro.style.display = "block";
        } else {
            carro.style.display = "none";
        }
        });
    verificarResultados()
}



filterCategory.addEventListener("input", filtrar);
filterFuel.addEventListener("input", filtrar);