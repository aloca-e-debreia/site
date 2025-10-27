async function existantCPF(cpf, email, errorField) {
    try {
        const response = await fetch('/auth/register/api/existant-cpf', {
            method : "POST",
            headers : {"Content-Type" : "application/json"},
            body : JSON.stringify({"cpf" : cpf, "email" : email})
        })
        const data = await response.json()
        if (!data.success) { //usuário existente
            errorField.textContent = data.message
            return true
        }
        return false
    } catch(error) {
        console.error('Erro:', error)
    }
}

export async function existantCPFValue(validFields) {
    validFields['CPF'] = ! await existantCPF(document.getElementById('CPF').value.trim(), document.getElementById('email').value.trim(), document.getElementById('CPF-error'))
}

function valid(cpf) {
    let sum = 0, remainder
    if (cpf == "00000000000") return false

    for (let i=1; i<=9; i++) sum += parseInt(cpf.substring(i-1, i)) * (11 - i)
    remainder = (sum * 10) % 11

    if ((remainder == 10) || (remainder == 11))  remainder = 0
    if (remainder != parseInt(cpf.substring(9, 10)) ) return false

    sum = 0
    for (let i = 1; i <= 10; i++) sum += parseInt(cpf.substring(i-1, i)) * (12 - i)
    remainder = (sum * 10) % 11

    if ((remainder == 10) || (remainder == 11)) remainder = 0
    if (remainder != parseInt(cpf.substring(10, 11) ) ) return false
    return true
}

function blankField(field, errorField, message) {
    if (field === '') {
        errorField.textContent = message
        return true
    }
    errorField.textContent = ''
    return false
}

function isValidAge(fieldValue, errorField, message) {
    if (!(Number(fieldValue) > 0 && Number(fieldValue) < 120)) {
        errorField.textContent = message
        return false
    }
    errorField.textContent = ''
    return true
}

function isValidCPF(fieldValue, errorField, message) {
    if (!valid(fieldValue)) {
        errorField.textContent = message
        return false
    }
    errorField.textContent = ''
    return true
}

function isValidEmail(fieldValue, errorField, message) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(fieldValue)) {
        errorField.textContent = message
        return false
    }
    return true
}

function isValidPassword(fieldValue, errorField, message) {
    if (fieldValue.length < 8) {
        errorField.textContent = message
        return false
    }
    return true
}

export function isValidField(id, validFields, validateMessage) {
    const fieldValue = document.getElementById(id).value.trim()
    const errorField = document.getElementById(id+'-error')

    switch (id) {
        case 'CPF':
            validFields['CPF'] = isValidCPF(fieldValue, errorField, validateMessage['CPF'])
            break
        case 'age':
            validFields['age'] = isValidAge(fieldValue, errorField, validateMessage['age'])
            break
        case 'email':
            validFields['email'] = isValidEmail(fieldValue, errorField, validateMessage['email'])
            break
        case 'password':
            validFields['password'] = isValidPassword(fieldValue, errorField, validateMessage['password'])
            break
    }
}

export function isFieldBlank(id, validFields) {
    const fieldValue = document.getElementById(id).value.trim()
    const errorField = document.getElementById(id+'-error')
    if (blankField(fieldValue, errorField, `Por favor, digite seu ${id}`)) {
        validFields[id] = false
        return true
    }
    return false
}

export function isValidForm(validFields) {
    for (let field in validFields) if (!validFields[field]) return false
    return true
}