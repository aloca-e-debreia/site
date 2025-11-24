document.addEventListener('DOMContentLoaded', () => {    

    async function promoteUser(userID, userRole, promotion) {
        try {
            const answer = await fetch('/dashboard/api/promote', {
                method : "POST",
                headers : {"Content-Type" : "application/json"},
                body : JSON.stringify({
                    'id' : userID,
                    'role' : userRole,
                    'promotion': promotion
                })
            })
            const data = await answer.json()
            await swal({
                title : data.title,
                icon : data.icon,
            })
            if (data.success) window.location.reload()
        } catch(error) {
            console.error('Erro:', error)
        }
    }

    const promoteButtons = document.querySelectorAll(".promote")

    promoteButtons.forEach(button => {

        button.addEventListener("click", async event => {
            
            event.preventDefault()

            if (! await swal({
                title : "Desejas promover o usuário?",
                message : "Ele(a) receberá um email comprovando a promoção",
                icon : "info",
                buttons : true,
                dangermode : true
            })) return 

            if (button.dataset.role == "client") promoteUser(button.dataset.id, button.dataset.role, 'worker')
            else promoteUser(button.dataset.id, button.dataset.role, 'manager')

        })
    })
})