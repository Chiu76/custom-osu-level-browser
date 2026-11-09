import { createSignal } from "../reactive.js";
import { schemas } from "../utils.js";

export function BeatmapSearchFilterHandler() {
    const [search, setSearch] = createSignal([]);
    const [filter, setFilter] = createSignal([]);

    const parentElement = document.getElementById("beatmap-search-filter");
    const inputElement = parentElement.getElementsByTagName("input")[0];
    
    const filterValuesDefault = schemas["Filter"]["properties"]["field"]["anyOf"][0]["enum"];
    const filterValuesAlt = schemas["Filter"]["properties"]["field"]["anyOf"][1]["enum"];
    const fieldValues = filterValuesDefault.concat(filterValuesAlt);

    const opValues = schemas["Filter"]["properties"]["op"]["enum"];
    const opValuesRegex = new RegExp(opValues.join("|"), "g");

    function assertOp(filter) {
        return (filter.match(opValuesRegex) ?? []).length > 0;
    }

    function assertOpCount(filter) {
        return (filter.match(opValuesRegex) ?? []).length === 1;
    }

    function assertField(filter) {
        let field = filter.split(opValuesRegex)[0];
        return fieldValues.includes(field);
    }

    function parseUserInput(values) {
        // assumes input is an array of search or filter strings, such as:
        // ["touhou", "artist=demetori", "owner=monstrata", "bpm>67"]
        const resultSearch = [];
        const resultFilter = [];

        for (let value of values) {
            value = value.toLowerCase();
            // no operator in the user input -> parse it as a search string 
            if (!assertOp(value)) {
                resultSearch.push(value);
            }
            // otherwise parse it as a filter
            else {
                if (!assertOpCount(value)) {
                    return {
                        successful: false,
                        reason: `There is not exactly one operator in the filter: ${value}`,
                        resultSearch: [], 
                        resultFilter: [],
                    }
                }
                if (!assertField(value)) {
                    return {
                        successful: false,
                        reason: `Invalid filter field: ${value.split(opValuesRegex)[0]}`,
                        resultSearch: [], 
                        resultFilter: [],
                    }
                }
                const op = value.match(opValuesRegex)[0];
                const tokens = value.split(op);
                resultFilter.push({
                    field: tokens[0],
                    op: op,
                    value: tokens[1],
                });
            }
        }
        return {
            successful: true,
            reason: "",
            resultSearch: resultSearch,
            resultFilter: resultFilter,
        };
    }

    function processUserInput(value) {
        if (value === "") return { successful: true, reason: "", resultSearch: [], resultFilter: [] };
        if (value === value.split(" ")) return parseUserInput([value]);
        return parseUserInput(value.split(" "));
    }

    function onInput(value) {
        const filterParsedResult = processUserInput(value);
        if (!filterParsedResult.successful) {
            // todo: create and set some signals to show the error in the interface
            console.log("filterParsedResult: ", filterParsedResult.reason, filterParsedResult);
            return;
        }
        setSearch(filterParsedResult.resultSearch);
        setFilter(filterParsedResult.resultFilter);
    }

    function init() {
        let timeout;
        inputElement.addEventListener("input", (event) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => onInput(event.target.value), 250);
        });

        return [search, setSearch, filter, setFilter];
    }

    return {
        init,
    }
}