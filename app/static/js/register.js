import {isFieldBlank, isValidField, isValidForm} from './registerFunctions.js'

var blankSpaces = 0

document.addEventListener('DOMContentLoaded', () => {    

    const buttonForm = document.getElementById('button')
    const authForm = document.getElementById('auth-form')

    let elements = ['name', 'email', 'password']

    let validateMessage = {
        'email' : 'Por favor, digite um email válido',
        'password' : 'Por favor, digite uma senha de pelo menos 8 dígitos'
    }

    buttonForm.addEventListener('click', event => {
        event.preventDefault()

        let validFields = {
            'email' : false,
            'password' : false
        }
        blankSpaces = 0
        
        elements.forEach((id) => blankSpaces += isFieldBlank(id, validFields))
 
        elements.forEach((id) => isValidField(id, validFields, validateMessage))

        if (blankSpaces > 0) document.getElementById('warning').textContent = 'Todos os campos são obrigatórios!'
        
        else document.getElementById('warning').textContent = ''

        if (isValidForm(validFields)) authForm.submit()
    })
})