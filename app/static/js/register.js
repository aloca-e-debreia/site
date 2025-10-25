import {checarCamposVazios, validarCampo, formularioValido} from './registerFunctions.js'

var espacosVazios = 0

document.addEventListener('DOMContentLoaded', () => {    

    const formularioBotao = document.getElementById('botao')
    const authFormulario = document.getElementById('auth-formulario')

    let elementos = ['email', 'senha']

    let mensagemValidar = {
        'email' : 'Por favor, digite um email válido',
        'senha' : 'Por favor, digite uma senha de pelo menos 8 dígitos'
    }

    formularioBotao.addEventListener('click', async event => {
        event.preventDefault()

        let camposValidos = {
            'email' : false,
            'senha' : false
        }
        espacosVazios = 0
        
        elementos.forEach((id) => espacosVazios += checarCamposVazios(id, camposValidos))

        elementos.forEach((id) => validarCampo(id, camposValidos, mensagemValidar))

        if (espacosVazios > 0) document.getElementById('aviso').textContent = 'Todos os campos são obrigatórios!'
        
        else document.getElementById('aviso').textContent = ''

        if (formularioValido(camposValidos)) authFormulario.submit()
    })
})