import {existantDataValue, isFieldBlank, isValidField, isValidForm} from './registerFunctions.js'

var blankSpaces = 0

document.addEventListener('DOMContentLoaded', () => {    

    const buttonForm = document.getElementById('button')
    const authForm = document.getElementById('auth-form')


    let elements = ['name', 'CPF', 'age', 'email']

    let validateMessage = {
        'CPF' : 'Por favor, digite um CPF válido',
        'age' : 'Por favor, digite uma idade entre 0 e 120 anos',
        'email' : 'Por favor, digite um email válido',
    }

    buttonForm.addEventListener('click', async event => {
        event.preventDefault()

        let validFields = {
            'name' : true,
            'CPF' : false,
            'age' :  false,
            'email' : false,
        }

        blankSpaces = 0
        elements.forEach((id) => blankSpaces += isFieldBlank(id, validFields))

        elements.forEach((id) => isValidField(id, validFields, validateMessage))

        if (validFields['CPF']) await existantDataValue('CPF', validFields)

        if (validFields['email']) await existantDataValue('email', validFields)

        if (blankSpaces > 0) document.getElementById('warning').textContent = 'Todos os campos são obrigatórios!'        
        else document.getElementById('warning').textContent = ''
        
        if (isValidForm(validFields)) authForm.submit()
    })
})