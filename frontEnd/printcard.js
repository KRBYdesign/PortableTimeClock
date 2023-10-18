const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);

let sentName = urlParams.get("name");
let id = urlParams.get("id");

document.title = `${sentName}, your print card is ready`;

let guardName = document.getElementById("idName");
let gaurdNumber = document.getElementById("idNumber");

gaurdNumber.innerText = id;
guardName.innerText = sentName;

JsBarcode("#idBarcode", id, {
  height: 150,
  width: 1.5,
});
