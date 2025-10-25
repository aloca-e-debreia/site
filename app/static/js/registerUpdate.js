import {CPFExistenteValor, checarCampoVazio, validarCampo, formularioValido} from './registerFunctions.js'

var espacosVazios = 0

document.addEventListener('DOMContentLoaded', () => {    

    const formularioBotao = document.getElementById('botao')
    const authFormulario = document.getElementById('auth-formulario')


    let elementos = ['nome', 'CPF', 'idade', 'email']

    let mensagemValidar = {
        'CPF' : 'Por favor, digite um CPF válido',
        'idade' : 'Por favor, digite uma idade entre 0 e 120 anos',
        'email' : 'Por favor, digite um email válido',
    }

    formularioBotao.addEventListener('click', async event => {
        event.preventDefault()

        let camposValidos = {
            'nome' : true,
            'CPF' : false,
            'idade' :  false,
            'email' : false,
        }

        espacosVazios = 0
        elementos.forEach((id) => espacosVazios += checarCampoVazio(id, camposValidos))

        elementos.forEach((id) => validarCampo(id, camposValidos, mensagemValidar))

        if (camposValidos['CPF']) await CPFExistenteValor(camposValidos)

        if (espacosVazios > 0) document.getElementById('aviso').textContent = 'Todos os campos são obrigatórios!'        
        else document.getElementById('aviso').textContent = ''
        console.log(camposValidos)
        console.log(espacosVazios)
        if (formularioValido(camposValidos)) authFormulario.submit()
    })
})