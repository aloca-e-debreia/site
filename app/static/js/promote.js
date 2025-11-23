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
            alert(data.message)
            window.location.reload()
        } catch(error) {
            console.error('Erro:', error)
        }
    }

    const promoteButtons = document.querySelectorAll(".promote")

    promoteButtons.forEach(button => {

        button.addEventListener("click", event => {
            
            event.preventDefault()

            if (confirm("Promover o user?"))
                if (button.dataset.role == "client") promoteUser(button.dataset.id, button.dataset.role, 'worker')
                else promoteUser(button.dataset.id, button.dataset.role, 'manager')

        })
    })
})