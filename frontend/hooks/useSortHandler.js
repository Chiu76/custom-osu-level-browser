import { schemas } from "../utils.js";


export function useSortHandler() {
    const fieldValues = schemas["Sorting"]["properties"]["field"]["enum"];
    const fieldValuesRegex = new RegExp(fieldValues.join("|"), "g");
    
    function createElementOption(value) {
        const option = document.createElement("option");
        option.value = value;
        option.innerText = value;
        return option;
    }

    function parseSort(field, dir='asc') {
        return {
            field: field,
            dir: dir,
        }
    }
    
    function populateSortSelect(id, setSort) {
        const sortSelect = document.getElementById(id);
        for (let fieldValue of fieldValues.sort()) {
            sortSelect.appendChild(createElementOption(fieldValue));
        }
        sortSelect.addEventListener("change", (event) => { setSort(parseSort(event.target.value)); });
    }

    function setSortSelect(id, value) {
        const sortSelect = document.getElementById(id);
        sortSelect.value = value;
        sortSelect.dispatchEvent(new Event("change"));
    }

    function init(setSortPrimary, setSortSecondary) {
        populateSortSelect("sort-select-primary", setSortPrimary);
        populateSortSelect("sort-select-secondary", setSortSecondary);

        // default values
        setSortSelect("sort-select-primary", "artist");
        setSortSelect("sort-select-secondary", "title");
    }

    return {
        init,
    };
}