function getallusers(){
    fetch("http://localhost:4000/get/allusers", {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
        'X-API-Key': 'altooro'
    },
    }).then(res => {
        return res.json()
    }).then(data => console.log(data))
    .catch(err => console.log('Error'))
}

function getuserbyidusername(){
    let html = document.getElementById('9').value
    let uusername = document.getElementById('10').value
    let url = `http://localhost:4000/get/user-by-id-username?id=${html}&username=${uusername}`
    fetch(url, {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
        'X-API-Key': 'altooro'
    },
    }).then(res => {
        return res.json()
    }).then(user => {
        document.getElementById("1").innerHTML = `${user.id}`; 
        document.getElementById("2").innerHTML = `${user.username}`; 
        document.getElementById("3").innerHTML = `${user.email}`;
        document.getElementById("4").innerHTML = `${user.password}`;
        document.getElementById("5").innerHTML = `${user.age}`;
    })
    .catch(err => console.log('Error'))
}

function create_user(){
    console.log(document.getElementById('0').value);
    fetch('http://localhost:4000/create/user/',{
       method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-API-Key': 'altooro'
    },
    body: JSON.stringify({
        username: document.getElementById('0').value,
        email: document.getElementById('1').value,
        password: document.getElementById('2').value,
        gender: 'male',
        age: 0,
        birthday: '2022-03-21'
    })
    }).then(res => {
        return res.json();
    })
    .then(data => {
        document.getElementById("10").innerHTML = `user created succsessfully`
    })
    .catch(error => console.log('error'))
    
}
function hi(){
    getuserbyidusername()
}
function hi2(){
    create_user()
}
