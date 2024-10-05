import { clearMarkers, addMapMarker } from "./locations.js";
import {
  addResultRow,
  clearTable,
  getFilteredResults,
  populateInputs,
} from "./results.js";
import { error } from "./logging.js";

window.onerror = (e) => showError(e);

// event is of type PromiseRejectionEvent
window.addEventListener("unhandledrejection", (event) => {
  event.preventDefault(); // This will not print the error in the console });
  error(event.reason);
});

function showError(errorMsg, url, lineNumber) {
  error(errorMsg);
  return true;
}

populateInputs();

document.getElementById("input-submit").onclick = async () => {
  clearTable();
  clearMarkers();

  let inputYear = document.getElementById("input-year");
  let yearIndices = inputYear.selectedOptions;

  let inputNummer = document.getElementById("input-nummer");
  let nummer = parseInt(inputNummer.value);

  let inputSpeciale = document.getElementById("input-speciale");
  let specialer = Array.from(inputSpeciale.selectedOptions).map((o) => o.label);

  let inputEnhed = document.getElementById("input-enhed");
  let enheder = Array.from(inputEnhed.selectedOptions).map((o) => o.label);

  let filteredResults = getFilteredResults(
    yearIndices,
    nummer,
    specialer,
    enheder
  );

  filteredResults
    .sort((a, b) => a.nummer - b.nummer)
    .forEach((r) => {
      addResultRow(r);
    });

  enheder
    .filter((e) => filteredResults.map((f) => f.enhed).includes(e))
    .forEach((e) => addMapMarker(e));
};
