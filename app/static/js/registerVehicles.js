import { configureDatalists } from "./datalistsConfig.js"

document.addEventListener('DOMContentLoaded', () => {
    configureDatalists('search', true)

    document.getElementById('btn').addEventListener("click", async event => {
        event.preventDefault()
        const formData = new FormData(document.getElementById('register-vehicle-form'))
        try {
            const response = await fetch('/dashboard/register-vehicles', {
                method: "POST",
                body: formData
            })
            const data = await response.json()
            alert(data.message)
            if (data.success) {
                window.location.reload()
            }
        } catch(error) {
            console.error('Erro:', error)
        }
    })
})