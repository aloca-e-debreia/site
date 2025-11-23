export async function emailSendVerify (apiRoute) {
    
    const response = await fetch(apiRoute, {
        method: "POST",
        headers : {"Content-Type" : "application/json"},
        body : JSON.stringify({})
    })

    if (!response.ok) throw new Error("Falha na requisição")
    
    const data = await response.json()

    return data
}