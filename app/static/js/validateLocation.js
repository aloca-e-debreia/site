import { configureDatalists } from "./datalistsConfig.js"

document.addEventListener('DOMContentLoaded', () => {

    configureDatalists("branches", false)

    const pickupAddress = document.getElementById('pickup-branch');
    const pickupDate = document.getElementById('pickup-date');
    const pickupTime = document.getElementById('pickup-time');
    const dropoffAddress = document.getElementById('dropoff-branch');
    const dropoffDate = document.getElementById('dropoff-date');
    const dropoffTime = document.getElementById('dropoff-time')
    const btn = document.getElementById('btn')
    const devolucaoDiv = document.getElementById('devolucao');

    function verificarCampos() {
        if (pickupAddress.value.trim() !== "" &&
            pickupDate.value !== "" &&
            pickupTime.value !== "") {

            devolucaoDiv.style.display = "flex"; // mostra div
            if (dropoffAddress.value === "") dropoffAddress.value = pickupAddress.value
        } else {
            devolucaoDiv.style.display = "none"; // esconde se faltar algo
        }
    }

    function verificarCamposDev(){
        if (dropoffAddress.value.trim() !== "" && dropoffDate.value !== "" && dropoffTime.value !== ""){
                btn.style.display = "block";
            } else{
                btn.style.display = "none";
            }
    }
    
    pickupAddress.addEventListener("input", verificarCampos);
    pickupDate.addEventListener("change", verificarCampos);
    pickupTime.addEventListener("change", verificarCampos);
    dropoffAddress.addEventListener("input", verificarCamposDev);
    dropoffDate.addEventListener("change", verificarCamposDev);
    dropoffTime.addEventListener("change", verificarCamposDev);

})