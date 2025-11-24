document.addEventListener("DOMContentLoaded", () => {
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
    document.querySelectorAll(".extra-right").forEach(extraForm => {
        extraForm.addEventListener("submit", async event => {
            event.preventDefault()
            document.getElementById("ContHeader").scrollIntoView({behavior : "smooth"})
            
            const formData = new FormData(extraForm)
            
            try {
                const response = await fetch(extraForm.action, {
                    method: "POST",
                    body : formData
                })

                data = await response.json()

                if (data.success) {
                    const extrasHtmlResponse = await fetch(`/api/pay/${extraForm.rental_id.value}/extras`)
                    const extrasHtml = await extrasHtmlResponse.text()

                    document.getElementById("rental-extras-container").innerHTML = extrasHtml
                }

            } catch(error) {
                console.error("Erro:", error)
            }
        })
    })
})