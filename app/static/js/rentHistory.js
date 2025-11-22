document.addEventListener("DOMContentLoaded", () => {

    async function cancelRent(rentId) {
        try {
            const response = await fetch('/user/2/api/cancel', {
                method: "POST",
                headers : {"Content-Type" : "application/json"},
                body : JSON.stringify({'rentId' : rentId})
            })
            const data = await response.json()
            alert(data.message)
            if (data.success) window.location.reload()
        } catch(error) {
            console.error('Erro:', error)
        }
    }
    
    document.querySelectorAll(".btn-cancel-rent").forEach(button => {
        button.addEventListener("click", event => {
            event.preventDefault()

            if (!confirm("Deseja cancelar a locação?")) return
            
            cancelRent(button.dataset.rentId)
        }) 
    });

    document.querySelectorAll(".Cont").forEach(cont => {
        cont.addEventListener("click", () => {
            const details = cont.nextElementSibling;

            if (details && details.classList.contains("Cont-Details"))
                details.classList.toggle("open");    
        })
    })
})