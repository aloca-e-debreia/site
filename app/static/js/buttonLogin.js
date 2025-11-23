const filterPrice = document.getElementById("filterPrice");

// Função que ordena
function ordenar() {
    const criterio = filterPrice.value.toLowerCase();

    // Converter NodeList em array
    const carrosArray = Array.from(carros);

    carrosArray.sort((a, b) => {
        const precoA = parseFloat(a.querySelector("h2").innerText.replace("/Dia", ""));
        const precoB = parseFloat(b.querySelector("h2").innerText.replace("/Dia", ""));

        if (criterio === "mais barato" || criterio === "menor → maior") {
            return precoA - precoB; // Crescente
        }
        if (criterio === "mais caro" || criterio === "maior → menor") {
            return precoB - precoA; // Decrescente
        }
    });

    const container = document.querySelector(".carros");
    container.innerHTML = "";

    carrosArray.forEach(carro => container.appendChild(carro));
}

filterPrice.addEventListener("input", ordenar);