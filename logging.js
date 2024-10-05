export { info, error };

function info(error) {
  let li = document.createElement("li");
  // let span = document.createElement("span")
  let text = document.createTextNode(error);
  // span.appendChild(text)
  li.appendChild(text);
  document.getElementById("error").appendChild(li);

  // let errorSpan = document.getElementById("error")
  // let existing = errorSpan.textContent
  // errorSpan.textContent = existing + "<br/>" + error;
}

function error(errorMsg) {
  alert(errorMsg);
  document.getElementById("results").innerHTML = errorMsg;
}
