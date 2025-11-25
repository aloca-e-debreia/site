document.addEventListener("DOMContentLoaded", () => {

    async function removeAccount(userId) {
        try {
            const response = await fetch('/auth/api/account/remove', {
                method: "POST",
                headers : {"Content-Type" : "application/json"},
                body : JSON.stringify({'userId' : userId})
            })
            const data = await response.json()
            await swal({
                title : data.title,
                icon : data.icon
            })
            if (data.success) window.location.href = data.redirect_url
        } catch(error) {
            console.error('Erro:', error)
        }
    }

    async function cancelRent(rentId) {
        try {
            const response = await fetch('/user/2/api/cancel', {
                method: "POST",
                headers : {"Content-Type" : "application/json"},
                body : JSON.stringify({'rentId' : rentId})
            })
            const data = await response.json()
            await swal({
                title : data.title,
                icon : data.icon
            })
            if (data.success) window.location.reload()
        } catch(error) {
            console.error('Erro:', error)
        }
    }
    
    const cancelRentButtons = document.querySelectorAll(".btn-cancel-rent")
    if (cancelRentButtons) {
        cancelRentButtons.forEach(button => {
            button.addEventListener("click", async event => {
                event.preventDefault()

                if (!await swal({
                    title : "Desejas cancelar a locação?",
                    icon : "warning",
                    buttons : true,
                    dangermode : true
                })) return
                
                cancelRent(button.dataset.rentId)
            }) 
        })
    }
    
    const removeAccountBtn = document.getElementById("remove-account-btn")
    if (removeAccountBtn) {
        removeAccountBtn.addEventListener("click", async event => {
            event.preventDefault()
            if (await swal({
                title : "Desejas remover sua conta?",
                icon : "warning",
                buttons : true,
                dangermode : true
            })) removeAccount(event.target.dataset.id)
        })
    }

    const ContClass = document.querySelectorAll(".Cont")
    if (ContClass) {
        ContClass.forEach(cont => {
            cont.addEventListener("click", () => {
                const details = cont.nextElementSibling;

                if (details && details.classList.contains("Cont-Details"))
                    details.classList.toggle("open");    
            })
        })
    }   

    (function recentPaidRent() {
        const openedId = new URLSearchParams(window.location.search).get("opened")
        if (!openedId) return

        const target = document.querySelector(`[data-rental-id="${openedId}"]`)
        if (!target) return
        target.click()
        target.scrollIntoView({behavior : "smooth"})
    })()

    Array.from(document.getElementsByTagName("button")).forEach(btn => {
        btn.addEventListener("click", event => {
            event.preventDefault()
            if (btn.dataset.route) window.location.href=btn.dataset.route
        })
    })

    document.querySelectorAll(".box").forEach(box => {
        box.addEventListener("click", event => {
            event.preventDefault()
            if (box.dataset.route) window.location.href=box.dataset.route
        })
    })

})