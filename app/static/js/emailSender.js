export async function emailSendVerify (apiRoute, json=JSON.stringify({})) {
    
    const response = await fetch(apiRoute, {
        method: "POST",
        headers : {"Content-Type" : "application/json"},
        body : json
    })

    if (!response.ok) throw new Error("Falha na requisição")
    
    const data = await response.json()

    return data
}