import { schemas } from "../utils.js";

export function SortHandler() {
    let getter;
    let setter;

    const fieldValues = schemas["Sorting"]["properties"]["field"]["enum"].sort();
    // const fieldValuesRegex = new RegExp(fieldValues.join("|"), "g");
    
    function updateSortSelect(parentId, value) {
        const sortSelect = document.getElementById(parentId).getElementsByTagName("select")[0];
        sortSelect.value = value;
        sortSelect.dispatchEvent(new Event("change"));
    }

    function updateSortAtIndex(index, field, dir) {
        const sortContent = getter();
        sortContent[index] = { field: field, dir: dir };
        return sortContent;
    }

    function createElementOption(value) {
        const option = document.createElement("option");
        option.value = value;
        option.innerText = value;
        return option;
    }

    function instantiateSortDir(sortSelect, sortDir) {
        sortDir.innerText = "asc";
        sortDir.addEventListener("click", () => { 
            if (sortDir.innerText == "asc") sortDir.innerText = "desc";
            else if (sortDir.innerText == "desc") sortDir.innerText = "asc";
            sortSelect.dispatchEvent(new Event("change"));
        });
    }
    
    function instantiateSortSelect(sortSelect, sortDir, index) {
        for (let fieldValue of fieldValues) {
            sortSelect.appendChild(createElementOption(fieldValue));
        }
        sortSelect.addEventListener("change", (event) => { 
            setter(
                updateSortAtIndex(index, event.target.value, sortDir.innerText)
            ); 
        });        
    }

    function instantiateSort(parentId, index) {
        const sortParent = document.getElementById(parentId);
        const sortSelect = sortParent.getElementsByTagName("select")[0];
        const sortDir = sortParent.getElementsByClassName("dir")[0];

        instantiateSortSelect(sortSelect, sortDir, index);
        instantiateSortDir(sortSelect, sortDir);
    }

    function init(sort, setSort) {
        getter = sort;
        setter = setSort;

        instantiateSort("sort-primary", 0);
        instantiateSort("sort-secondary", 1);
        instantiateSort("sort-third", 2);

        // default values
        // todo: when reactive batching is implemented, these should be batched
        updateSortSelect("sort-primary", "artist");
        updateSortSelect("sort-secondary", "title");
        updateSortSelect("sort-third", "beatmap_set_id");
    }

    return {
        init,
    };
}