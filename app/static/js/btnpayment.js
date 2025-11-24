import { emailSendVerify } from "./emailSender.js";

document.addEventListener("DOMContentLoaded", () => {

    document.querySelectorAll('.payment-option').forEach(btn => {
        btn.addEventListener('click', () => {
            btn.classList.remove('active');
            btn.classList.add('active');
        });
    });

    document.getElementById("btn-confirm").addEventListener("click", async event => {
        event.preventDefault()

        const confirmForm = document.getElementById('confirm-form')
        var loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));
        
        loadingModal.show();

        try {
            const result = await emailSendVerify(event.target.dataset.confirmationEmail)
            loadingModal.hide();
            await swal({
                title : result.title,
                text : result.message,
                icon : result.type
            })
            confirmForm.submit()
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