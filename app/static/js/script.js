function valido(cpf) {
    let soma = 0, resto
    if (cpf == "00000000000") return false

    for (i=1; i<=9; i++) soma += parseInt(cpf.substring(i-1, i)) * (11 - i)
    resto = (soma * 10) % 11

    if ((resto == 10) || (resto == 11))  resto = 0
    if (resto != parseInt(cpf.substring(9, 10)) ) return false

    soma = 0
    for (i = 1; i <= 10; i++) soma += parseInt(cpf.substring(i-1, i)) * (12 - i)
    resto = (soma * 10) % 11

    if ((resto == 10) || (resto == 11)) resto = 0
    if (resto != parseInt(cpf.substring(10, 11) ) ) return false
    return true
}

async function CPFExistente(cpf, erroCampo) {
    try {
        const resposta = await fetch('/cadastro/api/cpf-existente', {
            method : "POST",
            headers : {"Content-Type" : "application/json"},
            body : JSON.stringify({cpf})
        })
        const dados = await resposta.json()
        if (!dados.success) { //usuário existente
            erroCampo.textContent = dados.message
            return true
        }
        return false
    } catch(error) {
        console.log('Erro:', error)
    }
}

async function CPFExistenteValor(camposValidos) {
    camposValidos['CPF'] = ! await CPFExistente(document.getElementById('CPF').value, document.getElementById('CPF-error'))
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
    return true
}

function validarSenha(valorCampo, erroCampo, mensagem) {
    if (valorCampo.length < 8) {
        erroCampo.textContent = mensagem
        return false
    }
    return true
}

function validarCampo(id, camposValidos, mensagemValidar) {
    const campoValor = document.getElementById(id).value.trim()
    const campoErro = document.getElementById(id+'-error')

    camposValidos[id] = !CampoVazio(campoValor, campoErro, `Por favor, digite seu ${id}`)
    if (!camposValidos[id]) ++espacosVazios

    switch (id) {
        case 'CPF':
            camposValidos['CPF'] = validarCPF(campoValor, campoErro, mensagemValidar['CPF'])
            break
        case 'idade':
            camposValidos['idade'] = validarIdade(campoValor, campoErro, mensagemValidar['idade'])
            break
        case 'email':
            camposValidos['email'] = validarEmail(campoValor, campoErro, mensagemValidar['email'])
            break
        case 'senha':
            camposValidos['senha'] = validarSenha(campoValor, campoErro, mensagemValidar['senha'])
            break
    }
}

function formularioValido(camposValidos) {
    for (campo in camposValidos) if (!camposValidos[campo]) return false
    return true
}

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

    formularioBotao.addEventListener('click', async event => {
        event.preventDefault()

        let camposValidos = {
            'nome' : false,
            'sobrenome' : false,
            'CPF' : false,
            'idade' :  false,
            'email' : false,
            'senha' : false
        }
        espacosVazios = 0

        elementos.forEach((id) => validarCampo(id, camposValidos, mensagemValidar))

        if (camposValidos['CPF']) await CPFExistenteValor(camposValidos)
        console.log(camposValidos)
        if (espacosVazios > 0) document.getElementById('aviso').textContent = 'Todos os campos são obrigatórios!'
        else document.getElementById('aviso').textContent = ''

        if (formularioValido(camposValidos)) authFormulario.submit()
    })
})