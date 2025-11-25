document.addEventListener("DOMContentLoaded", () => {

    const initialRentalId = document.querySelector(".rental-id").value

    setupQuantityListeners()
    setupActionListeners(initialRentalId)

    function setupQuantityListeners () {
        document.querySelectorAll(".add-extra-btn").forEach(addExtraBtn => {
            addExtraBtn.addEventListener("click", event => {
                event.preventDefault()
                const extraId = addExtraBtn.dataset.id
                const extraField = document.getElementById(extraId)
                extraField.innerHTML = ++extraField.textContent
                document.getElementById(`${extraId}-quantity`).value = extraField.textContent
            })
        })
        document.querySelectorAll(".rmv-extra-btn").forEach(rmvExtraBtn => {
            rmvExtraBtn.addEventListener("click", event => {
                event.preventDefault()
                const extraId = rmvExtraBtn.dataset.id
                const extraField = document.getElementById(extraId)
                if (extraField.textContent == 0) return
                extraField.innerHTML = --extraField.textContent
                document.getElementById(`${extraId}-quantity`).value = extraField.textContent
            })
        })
    }

    function setupActionListeners(rentalId) {
        document.querySelectorAll(".remove-extra").forEach(removeExtra => {
            removeExtra.addEventListener("click", async event => {
                event.preventDefault()
                const extraId = removeExtra.dataset.extraId
                try {
                    const response = await fetch(`/api/pay/extra/remove`, {
                        method: "POST",
                        headers : {"Content-Type" : "application/json"},
                        body : JSON.stringify({
                            'extra_id' : extraId,
                            'rental_id' : rentalId
                        })
                    })
                    const data = await response.json()
                    if (data.success) updateExtras(rentalId)
                } catch(error) {
                    console.error('Erro:', error)
                }
            })
        })

        document.querySelectorAll(".send-extra-btn").forEach(addExtra => {
            addExtra.addEventListener("click", async event => {
                event.preventDefault()
                const extraId = addExtra.dataset.extraId
                try {
                    const response = await fetch('api/pay/add-extra', {
                        method: "POST",
                        headers : {"Content-Type" : "application/json"},
                        body : JSON.stringify({
                            'rental_id' : rentalId,
                            'extra_id' : extraId,
                            'quantity' : document.getElementById(extraId+'-quantity').value
                        })
                    })
                    const data = await response.json()
                    if (data.success) updateExtras(rentalId)
                } catch(error) {
                    console.error('Erro:', error)
                }
            })
        })
    }

    async function updateExtras(rental_id) {
        document.getElementById("ContHeader").scrollIntoView({behavior : "smooth"})

        const extrasHtmlResponse = await fetch(`/api/pay/${rental_id}/extras`)
        const extrasListHtmlResponse = await fetch(`/api/pay/${rental_id}/extras/list`)
        const carSummary = await fetch(`/api/pay/${rental_id}/car/summary`)

        const selectedExtrasHtml = await extrasHtmlResponse.text()
        const extrasHtml = await extrasListHtmlResponse.text()
        const carSummaryHtml = await carSummary.text()

        document.getElementById("rental-extras-container").innerHTML = selectedExtrasHtml
        document.getElementById("extras-container").innerHTML = extrasHtml
        document.getElementById("car-summary").innerHTML = carSummaryHtml

        setupQuantityListeners()
        setupActionListeners(rental_id)
    }

})