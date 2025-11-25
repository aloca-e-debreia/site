import { configureDatalists } from "./datalistsConfig.js"

document.addEventListener('DOMContentLoaded', async () => {

    (async () => {
        try {
            const response = await fetch('/', {
                method: "POST",
                headers : {"Content-Type" : "application/json"},
                body : JSON.stringify({})
            })
            const data = await response.json()
            if (!data.route) return
            const confirmation = await swal({
                title: "Você tem uma locação em andamento, deseja continuar?",
                icon: "info",
                buttons: true,
                dangermode: true
            })
            if (!confirmation) data.route = 'main.index'
            redirect(confirmation, data.route)
        } catch(error) {
            console.error('Erro:', error)
        }
    })()

    async function redirect(confirmation, route) {
        try {
            const response = await fetch('/api/resume/rent', {
                method: "POST",
                headers : {"Content-Type" : "application/json"},
                body : JSON.stringify({
                    "confirmation" : confirmation,
                    "route" : route
                })
            })
            const data = await response.json()
            if (!data.success) {
                swal({
                    title : data.message,
                    icon: "error",
                })
                return
            } 
            window.location.href = data.redirect_url
        } catch(error) {
            console.error('Erro:', error)
        }   
    }
    
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
            if (dropoffAddress.value === "") {
                dropoffAddress.value = pickupAddress.value
                document.getElementById("dropoff-branch-id").value = document.getElementById("pickup-branch-id").value
            }
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