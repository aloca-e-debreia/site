document.addEventListener('DOMContentLoaded', () => {    
    
    function validarCPF(cpf) {
        let soma, resto
        soma = 0
        if (cpf == "00000000000") return false

        for (i=1; i<=9; i++) soma = soma + parseInt(cpf.substring(i-1, i)) * (11 - i)
        resto = (soma * 10) % 11

        if ((resto == 10) || (resto == 11))  resto = 0
        if (resto != parseInt(cpf.substring(9, 10)) ) return false

        soma = 0
        for (i = 1; i <= 10; i++) soma = soma + parseInt(cpf.substring(i-1, i)) * (12 - i)
        resto = (soma * 10) % 11

        if ((resto == 10) || (resto == 11))  resto = 0
        if (resto != parseInt(cpf.substring(10, 11) ) ) return false
        return true
    }

    const cadastroFormulario = document.getElementById('cadastro-formulario')

    const nomeInput = document.getElementById('nome')
    const nomeError = document.getElementById('nome-error')

    const sobrenomeInput = document.getElementById('sobrenome')
    const sobrenomeError = document.getElementById('sobrenome-error')

    const cpfInput = document.getElementById('cpf')
    const cpfError = document.getElementById('cpf-error')

    const idadeInput = document.getElementById('idade')
    const idadeError = document.getElementById('idade-error')

    const emailInput = document.getElementById('email')
    const emailError = document.getElementById('email-error')

    const senhaInput = document.getElementById('senha')
    const senhaError = document.getElementById('senha-error')


    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

    cadastroFormulario.addEventListener('click', (event) => {
        event.preventDefault()

        emailError.textContent = ''

        let isValid = true

        let blankCounter = 0

        if (nomeInput.value.trim() === '') {
            nomeError.textContent = 'Por favor, digite seu nome.'
            ++blankCounter
            isValid = false
        }

        if (sobrenomeInput.value.trim() === '') {
            sobrenomeError.textContent = 'Por favor, digite seu sobrenome.'
            ++blankCounter
            isValid = false
        }

        if (cpfInput.value.trim() === '') {
            cpfError.textContent = 'Por favor, digite seu sobrenome.'
            ++blankCounter
            isValid = false
        } else if (!validarCPF(cpfInput.value)) {
            cpfError.textContent = 'Por favor, digite um CPF válido'
        }

        if (idadeInput.value.trim() === '') {
            idadeError.textContent = 'Por favor, digite sua idade.'
            ++blankCounter
            isValid = false
        } else if (! (Number(idadeInput.value) > 0 && Number(idadeInput.value) < 120)) {
            idadeError.textContent = 'Por favor, digite uma idade entre 0 e 120 anos.'
        }

        if (emailInput.value.trim() === '') {
            emailError.textContent = 'Por favor, digite seu e-mail.'
            isValid = false
            ++blankCounter
        } else if (!emailRegex.test(emailInput.value.trim())) {
            emailError.textContent = 'Por favor, digite um e-mail válido.'
            isValid = false
        }

        if (senhaInput.value.trim() === '') {
            senhaError.textContent = 'Por favor, digite sua senha.'
            ++blankCounter
            isValid = false
        } else if (senhaInput.value.length < 8) {
            senhaError.textContent = 'Entre com uma senha com ao menos 8 caracteres'
            isValid = false
        }

        if (blankCounter === 6) {
            document.getElementById('aviso').textContent = 'Todos os campos são obrigatórios!'
        }
        if (isValid) {
            cadastroFormulario.submit()
        }
    })
})