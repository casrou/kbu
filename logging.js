export { info, error };

const LOGGING_ENABLED = false;

function info(error) {
  if (!LOGGING_ENABLED) return;
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
  if (!LOGGING_ENABLED) return;
  alert(errorMsg);
  document.getElementById("results").innerHTML = errorMsg;
}
