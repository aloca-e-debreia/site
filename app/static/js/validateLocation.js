document.addEventListener('DOMContentLoaded', () => {

    document.querySelectorAll(".addresses").forEach((addressInput) => {
        addressInput.addEventListener("input", () => {
            const inputValue = addressInput.value;
            const datalist = document.getElementById(addressInput.dataset.type+"-addresses");
            const options = datalist.options;
            const hiddenInput = document.getElementById(addressInput.dataset.type+'-address-id')

            for (let option of options) {
                if (option.value === inputValue) {
                    hiddenInput.value = option.dataset.id;
                    return;
                }
            }
            hiddenInput.value = ""
        });
    })

    const pickupAddress = document.getElementById('pickup-address');
    const pickupDate = document.getElementById('pickup-date');
    const pickupTime = document.getElementById('pickup-time');
    const dropoffAddress = document.getElementById('dropoff-address');
    const dropoffDate = document.getElementById('dropoff-date');
    const dropoffTime = document.getElementById('dropoff-time')
    const btn = document.getElementById('btn')
    const devolucaoDiv = document.getElementById('devolucao');

    function verificarCampos() {
        if (pickupAddress.value.trim() !== "" &&
            pickupDate.value !== "" &&
            pickupTime.value !== "") {

            devolucaoDiv.style.display = "flex"; // mostra div
            dropoffAddress.value = pickupAddress.value
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