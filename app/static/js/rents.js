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
            return data
        } catch(error) {
            console.error('Erro:', error)
        }   
    }

    function ButtonAlterStatus(btnClass, message, newStatus) {
        document.querySelectorAll("."+btnClass).forEach(btn => {
            btn.addEventListener("click", async event => {
                event.preventDefault()

                if (!await swal({
                    title : message,
                    text : "Uma vez confirmado, o cliente receberá um email confirmando a operação.",
                    icon : "info",
                    buttons : true,
                    dangermode : true
                })) {
                    swal("Operação cancelada.")
                    return
                }

                rentId = btn.dataset.rentId
                
                var loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
                
                loadingModal.show();
        
                try {
                    const result = await alterRentStatus(rentId, newStatus)
                    loadingModal.hide();
                    await swal(result.title, result.message, result.type)
                }
                catch (error) {
                    console.error(error)
                    data.message
                }
                finally {
                    loadingModal.hide();
                }
            })
        })
    }

    ButtonAlterStatus("pending", "Desejas atestar retirada do veículo?", "ACTIVE")
    ButtonAlterStatus("active", "Desejas atestar devolução do veículo?", "CLOSED")
    ButtonAlterStatus("late", "Desejas atestar devolução do veículo com atraso?", "CLOSED_LATE")
})