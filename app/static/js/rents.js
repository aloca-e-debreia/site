document.addEventListener("DOMContentLoaded", () => {

    async function alterRentStatus(rentId, newStatus) {
        try {
            const answer = await fetch('/dashboard/api/alter/status', {
                method : "POST",
                headers : {"Content-Type" : "application/json"},
                body : JSON.stringify({
                    'rent_id' : rentId,
                    'new_status' : newStatus
                })
            })
            const data = await answer.json()
            alert(data.message)
            window.location.reload()
        } catch(error) {
            console.error('Erro:', error)
        }   
    }

    function ButtonAlterStatus(btnClass, message, newStatus) {
        document.querySelectorAll("."+btnClass).forEach(btn => {
            btn.addEventListener("click", () => {
                if (!confirm(message)) return
                rentId = btn.dataset.rentId
                alterRentStatus(rentId, newStatus)
            })
        })
    }

    ButtonAlterStatus("pending", "Desejas atestar retirada do veículo?", "ACTIVE")
    ButtonAlterStatus("active", "Desejas atestar devolução do veículo?", "CLOSED")
})