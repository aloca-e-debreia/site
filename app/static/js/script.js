function valido(cpf) {
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

function CampoVazio(campo, erroCampo, mensagem) {
    if (campo === '') {
        erroCampo.textContent = mensagem
        return true
    }
    erroCampo.textContent = ''
    return false
}

function validarIdade(valorCampo, erroCampo, mensagem) {
    if (!(Number(valorCampo) > 0 && Number(valorCampo) < 120)) {
        erroCampo.textContent = mensagem
        return false
    }
    erroCampo.textContent = ''
    return true
}

function validarCPF(valorCampo, erroCampo, mensagem) {
    if (!valido(valorCampo)) {
        erroCampo.textContent = mensagem
        return false
    }
    erroCampo.textContent = ''
    return true
}

function validarEmail(valorCampo, erroCampo, mensagem) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(valorCampo)) {
        erroCampo.textContent = mensagem
        return false
    }
    erroCampo.textContent = ''
    return false
}

function validarSenha(valorCampo, erroCampo, mensagem) {
    if (valorCampo.length < 8) {
        erroCampo.textContent = mensagem
        return false
    }
    erroCampo.textContent = ''
    return true
}

function validarCampo(id, mensagemValidar) {
    const campoValor = document.getElementById(id).value.trim()
    const campoErro = document.getElementById(id+'-error')

    if (CampoVazio(campoValor, campoErro, `Por favor, digite seu ${id}`)) {
        ++espacosVazios
    } else ++camposValidos

    switch (id) {
        case 'CPF':
            camposValidos += validarCPF(campoValor, campoErro, mensagemValidar['CPF'])
            break
        case 'idade':
            camposValidos += validarIdade(campoValor, campoErro, mensagemValidar['idade'])
            break
        case 'email':
            camposValidos += validarEmail(campoValor, campoErro, mensagemValidar['email'])
            break
        case 'senha':
            camposValidos += validarSenha(campoValor, campoErro, mensagemValidar['senha'])
            break
    }
}

var camposValidos
var espacosVazios

document.addEventListener('DOMContentLoaded', () => {    

    const formularioBotao = document.getElementById('botao')
    const authFormulario = document.getElementById('auth-formulario')

    let elementos = ['nome', 'sobrenome', 'CPF', 'idade', 'email', 'senha']

    let mensagemValidar = {
        'CPF' : 'Por favor, digite um CPF válido',
        'idade' : 'Por favor, digite uma idade entre 0 e 120 anos',
        'email' : 'Por favor, digite um email válido',
        'senha' : 'Por favor, digite uma senha de pelo menos 8 dígitos'
    }

    formularioBotao.addEventListener('click', (event) => {
        event.preventDefault()

        camposValidos = 0; espacosVazios = 0

        elementos.forEach((id) => validarCampo(id, mensagemValidar))

        if (espacosVazios > 0) document.getElementById('aviso').textContent = 'Todos os campos são obrigatórios!'

        if (camposValidos === 9) authFormulario.submit()

    })
})