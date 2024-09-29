import { clearMarkers, addMapMarker } from "./locations.js";
import {
  addResultRow,
  clearTable,
  getFilteredResults,
  populateInputs,
} from "./results.js";

await populateInputs();

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

  filteredResults.forEach((r) => {
    addResultRow(r);
  });

  enheder.forEach((e) => addMapMarker(e));
};
