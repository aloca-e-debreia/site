import { existantDataValue, isFieldBlank, isValidField, isValidForm} from './registerFunctions.js'

var blankSpaces = 0

document.addEventListener('DOMContentLoaded', () => {    

    const buttonForm = document.getElementById('button')
    const authForm = document.getElementById('auth-form')


    let elements = [ 'name','email','cpf','data','nation','phone',
                     'country','state','city','CEP','road','hood',
                     'password','confirm-password']

    let validateMessage = {
        'email' : 'Por favor, digite um email válido',
        'password' : 'Por favor, digite uma senha de pelo menos 8 dígitos',
        'CPF': 'Digite um CPF válido',
        'phone' : 'Digite um número válido',
        'CEP' : 'Digite um CEP válido'
    }

    buttonForm.addEventListener('click', async event => {
        event.preventDefault()

        let validFields = {
            'email' : false,
            'password' : false,
            'CPF' : false,
            'data': false
        }

        blankSpaces = 0
       
        elements.forEach((id) => blankSpaces += isFieldBlank(id, validFields))
 
        elements.forEach((id) => isValidField(id, validFields, validateMessage))

        if (validFields['email']) await existantDataValue('email', validFields)
        console.log(validFields)
        if (blankSpaces > 0) document.getElementById('register-warning').textContent = 'Todos os campos são obrigatórios!'
       
        else document.getElementById('register-warning').textContent = ''

        if (isValidForm(validFields)) authForm.submit()

    })
})