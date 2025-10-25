async function CPFExistente(cpf, email, erroCampo) {
    try {
        const resposta = await fetch('/auth/cadastro/api/cpf-existente', {
            method : "POST",
            headers : {"Content-Type" : "application/json"},
            body : JSON.stringify({"cpf" : cpf, "email" : email})
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

export async function CPFExistenteValor(camposValidos) {
    camposValidos['CPF'] = ! await CPFExistente(document.getElementById('CPF').value.trim(), document.getElementById('email').value.trim(), document.getElementById('CPF-error'))
}

function valido(cpf) {
    let soma = 0, resto
    if (cpf == "00000000000") return false

    for (let i=1; i<=9; i++) soma += parseInt(cpf.substring(i-1, i)) * (11 - i)
    resto = (soma * 10) % 11

    if ((resto == 10) || (resto == 11))  resto = 0
    if (resto != parseInt(cpf.substring(9, 10)) ) return false

    soma = 0
    for (let i = 1; i <= 10; i++) soma += parseInt(cpf.substring(i-1, i)) * (12 - i)
    resto = (soma * 10) % 11

    if ((resto == 10) || (resto == 11)) resto = 0
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
    return true
}

function validarSenha(valorCampo, erroCampo, mensagem) {
    if (valorCampo.length < 8) {
        erroCampo.textContent = mensagem
        return false
    }
    return true
}

export function validarCampo(id, camposValidos, mensagemValidar) {
    const campoValor = document.getElementById(id).value.trim()
    const campoErro = document.getElementById(id+'-error')

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

export function checarCampoVazio(id, camposValidos) {
    const campoValor = document.getElementById(id).value.trim()
    const campoErro = document.getElementById(id+'-error')
    if (CampoVazio(campoValor, campoErro, `Por favor, digite seu ${id}`)) {
        camposValidos[id] = false
        return true
    }
    return false
}

export function formularioValido(camposValidos) {
    for (let campo in camposValidos) if (!camposValidos[campo]) return false
    return true
}