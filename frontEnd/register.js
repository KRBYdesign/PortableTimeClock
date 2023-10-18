const IP = "192.168.1.2";
const PORT = "5000";

let idCard = document.getElementById("idCard");
let message = document.getElementById("message");
document.getElementById("name").focus();

function registerNewUser() {
  let id = ("" + Math.random()).substring(2, 11);
  id = id.concat("X");
  let name = document.getElementById("name").value;

  console.log(name, id);

  postUserInfoToPi(name, id);
}

async function postUserInfoToPi(name, id) {
  let myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  fetch(`http://${IP}:${PORT}/register`, {
    method: "POST",
    headers: myHeaders,
    mode: "cors",
    body: JSON.stringify({
      id: id,
      name: name,
    }),
  })
    .then((response) => response.json())
    .then((response) => {
      message.innerText = response.message;
      document.getElementById("idName").innerText = response.name;
      document.getElementById("idNumber").innerText = response.id;

      if (response.success) {
        idCard.style.display = "block";
        document.getElementById("idName").innerText = `${response.name}`;
        document.getElementById("idNumber").innerText = `${response.id}`;

        JsBarcode("#idBarcode", response.id, {
          width: 1.5,
          height: 100,
        });

        window.print();
        setTimeout(location.reload.bind(location), 1000);
      } else {
        idCard.style.display = "none";
        setTimeout(location.reload.bind(location), 3000);
      }
    });
}

function lookUpUser() {
  let name = document.getElementById("name").value;

  let myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  fetch(`http://${IP}:${PORT}/register/${name}`, {
    method: "GET",
    headers: myHeaders,
    mode: "cors",
  })
    .then((response) => response.json())
    .then((response) => {
      console.log(response.id);
      console.log(response.success);

      let container = document.getElementById("multiple-results-container");
      container.innerHTML = "";
      idCard.style.display = "none";

      if (response.payload.length == 1) {
        idCard.style.display = "block";
        document.getElementById(
          "idName"
        ).innerText = `${response.payload[0].name}`;
        document.getElementById(
          "idNumber"
        ).innerText = `${response.payload[0].number}`;

        JsBarcode("#idBarcode", response.payload[0].number, {
          width: 1.5,
          height: 100,
        });
      } else if (response.payload.length > 1) {
        response.payload.forEach((result) => {
          let url_name = result.name.replace(" ", "%20");
          container.innerHTML += `<div class='multi-result-card'><h3>${result.name}</h3><p>${result.number}</p><a style='background-color: #78C3FB; color: black; padding: .5em;' href="./printcard.html?name=${url_name}&id=${result.number}">Print</a></div>`;
        });
      } else {
        idCard.style.display = "none";
      }
    });
}
