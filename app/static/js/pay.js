let contMotor = 0
function addmotorista(){
    const motorista = document.getElementById("add-motorista")
    contMotor+=1
    motorista.innerHTML = `${contMotor}`
}

function rmvmotorista(){
    const motorista = document.getElementById("add-motorista")
    contMotor-=1
    if (contMotor<0){
        contMotor=0
    }
    motorista.innerHTML = `${contMotor}`   
}

let contBaby = 0
function addbaby(){
    const bebe = document.getElementById("add-baby")
    contBaby+=1
    bebe.innerHTML = `${contBaby}`   
}

function rmvbaby(){
    const bebe = document.getElementById("add-baby")
    contBaby-=1
    if (contBaby<0){
        contBaby=0
    }
    bebe.innerHTML = `${contBaby}`   
}