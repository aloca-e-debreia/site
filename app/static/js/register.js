// register.js – validação completa do formulário

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("auth-form");

    const fields = {
        name: document.getElementById("name"),
        email: document.getElementById("email"),
        CPF: document.getElementById("CPF"),
        data: document.getElementById("data"),
        nation: document.getElementById("nation"),
        phone: document.getElementById("phone"),

        country: document.getElementById("country"),
        state: document.getElementById("state"),
        city: document.getElementById("city"),
        CEP: document.getElementById("CEP"),
        road: document.getElementById("road"),
        hood: document.getElementById("hood"),

        password: document.getElementById("password"),
        confirmPassword: document.getElementById("confirm-password"),
    };

    function showError(input, message) {
        const errorDiv = document.getElementById(`${input.id}-error`);
        errorDiv.textContent = message;
        input.classList.add("invalid");
    }

    function clearError(input) {
        const errorDiv = document.getElementById(`${input.id}-error`);
        errorDiv.textContent = "";
        input.classList.remove("invalid");
    }

    function validateName() {
        const value = fields.name.value.trim();
        if (value.length < 2) return showError(fields.name, "Nome muito curto.");
        clearError(fields.name);
        return true;
    }

    function validateEmail() {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!regex.test(fields.email.value))
            return showError(fields.email, "Email inválido.");
        clearError(fields.email);
        return true;
    }

    function validateCPF() {
        const cpf = fields.CPF.value.replace(/\D/g, "");

        if (!/^\d{11}$/.test(cpf))
            return showError(fields.CPF, "CPF deve conter 11 dígitos.");

        // Validação clássica
        let sum = 0;
        for (let i = 0; i < 9; i++) sum += parseInt(cpf[i]) * (10 - i);
        let d1 = 11 - (sum % 11);
        if (d1 > 9) d1 = 0;

        if (d1 != cpf[9])
            return showError(fields.CPF, "CPF inválido.");

        sum = 0;
        for (let i = 0; i < 10; i++) sum += parseInt(cpf[i]) * (11 - i);
        let d2 = 11 - (sum % 11);
        if (d2 > 9) d2 = 0;

        if (d2 != cpf[10])
            return showError(fields.CPF, "CPF inválido.");

        clearError(fields.CPF);
        return true;
    }

    function validateBirthdate() {
        const date = new Date(fields.data.value);
        const today = new Date();

        if (isNaN(date.getTime()))
            return showError(fields.data, "Data inválida.");

        if (date > today)
            return showError(fields.data, "Data não pode ser futura.");

        const age = today.getFullYear() - date.getFullYear();
        if (age < 18)
            return showError(fields.data, "Você deve ter ao menos 18 anos.");

        clearError(fields.data);
        return true;
    }

    function validatePhone() {
        const regex = /^\(?\d{2}\)?\s?\d{4,5}-?\d{4}$/;
        if (!regex.test(fields.phone.value))
            return showError(fields.phone, "Telefone inválido.");
        clearError(fields.phone);
        return true;
    }

    function validateCEP() {
        const regex = /^\d{5}-?\d{3}$/;
        if (!regex.test(fields.CEP.value))
            return showError(fields.CEP, "CEP inválido.");
        clearError(fields.CEP);
        return true;
    }

    function validateRequired(field) {
        if (field.value.trim() === "") {
            showError(field, "Campo obrigatório.");
            return false;
        }
        clearError(field);
        return true;
    }

    function validatePassword() {
        const pass = fields.password.value;

        if (pass.length < 8)
            return showError(fields.password, "A senha deve ter pelo menos 8 caracteres.");
        if (!/[A-Z]/.test(pass))
            return showError(fields.password, "A senha deve ter ao menos 1 letra maiúscula.");
        if (!/[a-z]/.test(pass))
            return showError(fields.password, "A senha deve ter ao menos 1 letra minúscula.");
        if (!/[0-9]/.test(pass))
            return showError(fields.password, "A senha deve ter ao menos 1 número.");
        if (!/[!@#$%&*]/.test(pass))
            return showError(fields.password, "A senha deve ter ao menos 1 caractere especial (!@#$%&*).");

        clearError(fields.password);
        return true;
    }

    function validatePasswordConfirm() {
        if (fields.password.value !== fields.confirmPassword.value)
            return showError(fields.confirmPassword, "As senhas não coincidem.");
        clearError(fields.confirmPassword);
        return true;
    }

    // disparar validação durante digitação
    Object.values(fields).forEach(field => {
        field.addEventListener("input", () => {
            const id = field.id;
            switch (id) {
                case "name": validateName(); break;
                case "email": validateEmail(); break;
                case "CPF": validateCPF(); break;
                case "data": validateBirthdate(); break;
                case "phone": validatePhone(); break;
                case "CEP": validateCEP(); break;
                case "password": validatePassword(); break;
                case "confirm-password": validatePasswordConfirm(); break;
                default: validateRequired(field);
            }
        });
    });

    form.addEventListener("submit", (e) => {
        let valid =
            validateName() &&
            validateEmail() &&
            validateCPF() &&
            validateBirthdate() &&
            validatePhone() &&
            validateCEP() &&
            validatePassword() &&
            validatePasswordConfirm() &&
            validateRequired(fields.nation) &&
            validateRequired(fields.country) &&
            validateRequired(fields.state) &&
            validateRequired(fields.city) &&
            validateRequired(fields.road) &&
            validateRequired(fields.hood);

        if (!valid) {
            e.preventDefault();
            alert("Por favor, corrija os erros antes de enviar.");
        }
    });
});