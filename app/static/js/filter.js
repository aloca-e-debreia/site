const inputName = document.getElementById("filter");
const filterCategory = document.getElementById("filterCategory");
const filterFuel = document.getElementById("filterFuel");
const filterPrice = document.getElementById("filterPrice");

const carros = document.querySelectorAll(".carro-card");
const noResults = document.getElementById("SemResultados");
const container = document.querySelector(".carros-grid");

function aplicarFiltros() {
    const nomeTexto = inputName.value.toLowerCase();
    const categoriaTexto = filterCategory.value.toLowerCase();
    const fuelTexto = filterFuel.value.toLowerCase();

    let carrosArray = Array.from(carros);

    carrosArray.forEach(carro => {
        const nome = carro.querySelector(".vehicle-title").innerText.toLowerCase();
        const categoria = carro.querySelector(".category").innerText.toLowerCase();
        const fuel = carro.querySelector(".fuel").innerText.toLowerCase();

        const matchNome = nome.includes(nomeTexto);
        const matchCategoria = categoria.includes(categoriaTexto) || categoriaTexto === "";
        const matchFuel = fuel.includes(fuelTexto) || fuelTexto === "";

        if (matchNome && matchCategoria && matchFuel) {
            carro.style.display = "block";
        } else {
            carro.style.display = "none";
        }
    });

    // Se nenhum carro visível → avisar
    const temVisivel = carrosArray.some(c => c.style.display !== "none");
    noResults.style.display = temVisivel ? "none" : "block";

    // ORDENAR APENAS OS QUE ESTÃO VISÍVEIS
    const criterio = filterPrice.value.toLowerCase();
    let carrosOrdenados = carrosArray.filter(c => c.style.display !== "none");

    carrosOrdenados.sort((a, b) => {
        const precoA = parseFloat(
            a.querySelector(".preco").innerText.replace("R$", "").replace("/ dia", "").trim()
        );

        const precoB = parseFloat(
            b.querySelector(".preco").innerText.replace("R$", "").replace("/ dia", "").trim()
        );

        if (criterio === "mais barato" || criterio === "menor → maior") return precoA - precoB;
        if (criterio === "mais caro" || criterio === "maior → menor") return precoB - precoA;
        return 0;
    });

    container.innerHTML = "";
    carrosOrdenados.forEach(c => container.appendChild(c));
}

inputName.addEventListener("input", aplicarFiltros);
filterCategory.addEventListener("input", aplicarFiltros);
filterFuel.addEventListener("input", aplicarFiltros);
filterPrice.addEventListener("input", aplicarFiltros);
