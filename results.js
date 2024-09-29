export { clearTable, getFilteredResults, addResultRow, populateInputs };

const FILES = [
  "KBU Forløb - Sommeren 2022 - Runde 29.json",
  "KBU Forløb - Vinter 2022_2023 - Runde 30.json",
  "KBU Forløb - Sommeren 2023 - Runde 31.json",
  "KBU Forløb - Vinter 2023_2024 - Runde 32.json",
];

const results = await fetchResults();

function getFilteredResults(yearIndices, nummer, specialer, enheder) {
  let filteredResults = [];

  for (let i = 0; i < yearIndices.length; i++) {
    const element = yearIndices[i];
    filteredResults = filteredResults.concat(results[element.value]);
  }

  return filteredResults.filter(
    (r) =>
      r.nummer >= nummer &&
      specialer.includes(r.speciale) &&
      enheder.includes(r.enhed)
  );
}

function populateInputs() {
  let resultsCombined = results.flat();
  var specialer = new Set();
  var enheder = new Set();
  for (let i = 0; i < resultsCombined.length; i++) {
    const r = resultsCombined[i];
    specialer.add(r.speciale);
    enheder.add(r.enhed);
  }

  const specialeSelect = document.getElementById("input-speciale");
  [...specialer].sort().forEach((s) => addOption(specialeSelect, s));

  const enhedSelect = document.getElementById("input-enhed");
  [...enheder].sort().forEach((e) => addOption(enhedSelect, e));
}

async function fetchResults() {
  let fetches = FILES.map((f) => fetch(f).then((r) => r.json()));
  return await Promise.all(fetches);
}

function addResultRow(r) {
  const results = document.getElementById("results");
  const tr = document.createElement("tr");
  tr.appendChild(createTd(r.nummer));
  tr.appendChild(createTd(r.speciale));
  tr.appendChild(createTd(r.enhed));
  tr.appendChild(createTd(r.afdeling));
  results.appendChild(tr);
}

function createTd(text) {
  var span = document.createElement("td");
  span.innerText = text;
  return span;
}

function clearTable() {
  var toBeRemoved = document
    .getElementById("results")
    .querySelectorAll("tr");
  toBeRemoved.forEach((tbr) => tbr.remove());
}

function addOption(select, option) {
  var child = document.createElement("option");
  child.innerText = option;
  select.appendChild(child);
}
