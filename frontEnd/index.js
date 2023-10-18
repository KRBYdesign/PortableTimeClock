const IP = "192.168.1.2";
const PORT = "5000";

let barcodeEntry = document.getElementById("barcode-entry");
barcodeEntry.focus();

function intakeBarcode() {
  let value = barcodeEntry.value;
  console.log(`Barcode: ${value}`);
  barcodeEntry.value = "";
  barcodeEntry.focus();

  sendClockInRequest(value);
}

async function sendClockInRequest(value) {
  let myHeaders = new Headers();
  myHeaders.append("Content-Type", "application/json");

  fetch(`http://${IP}:${PORT}/in`, {
    method: "POST",
    headers: myHeaders,
    mode: "cors",
    body: JSON.stringify({
      id: value,
    }),
  })
    .then((response) => response.json())
    .then((response) => {
      console.log(response);

      displayResponse(response);
    });
}

function displayResponse(response) {
  let container = document.getElementById("guard-info-container");

  container.classList.remove("hide");

  let name = document.getElementById("guard-name");
  let number = document.getElementById("guard-number");
  let action = document.getElementById("action");

  JsBarcode("#guard-barcode", response.id, {
    height: 150,
    width: 1.5,
  });

  name.innerText = response.name;
  number.innerText = response.id;
  action.innerText = `CLOCKED ${response.action}`;

  setTimeout(() => {
    window.location.reload();
  }, 3000);
}
