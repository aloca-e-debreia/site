async function promoverUsuario(usuarioID, usuarioFuncao, promocao) {
    try {
        const resposta = await fetch('/dashboard/api/promover', {
            method : "POST",
            headers : {"Content-Type" : "application/json"},
            body : JSON.stringify({'id' : usuarioID, 'funcao' : usuarioFuncao, 'promocao' : promocao})
        })
        const dados = await resposta.json()
        alert(dados.message)
    } catch(error) {
        console.error('Erro:', error)
    }
}

document.addEventListener('DOMContentLoaded', () => {    

    const botoesPromover = document.querySelectorAll(".promover")

    botoesPromover.forEach(botao => {

        botao.addEventListener("click", event => {
            
            event.preventDefault()

            if (confirm("Promover o user?"))
                if (botao.dataset.funcao == "client") promoverUsuario(botao.dataset.id, botao.dataset.funcao, 'worker')
                else promoverUsuario(botao.dataset.id, botao.dataset.funcao, 'manager')

            window.location.reload()
        })
    })
})