import { schemas } from "../utils.js";


export function useFilterHandler() {
    const fieldValues = schemas["Filter"]["properties"]["field"]["enum"];
    const fieldValuesRegex = new RegExp(fieldValues.join("|"), "g");

    const opValues = schemas["Filter"]["properties"]["op"]["enum"];
    const opValuesRegex = new RegExp(opValues.join("|"), "g");

    function assertOp(filter) {
        return (filter.match(opValuesRegex) ?? []).length === 1;
    }

    function assertField(filter) {
        let field = filter.split(opValuesRegex)[0];
        return fieldValues.includes(field);
    }

    function parseFilters(filters) {
        // used internally
        // assumes input is an array of filter strings, such as:
        // ["artist=demetori", "owner=monstrata", "bpm>67"]
        const result = [];
        for (let filter of filters) {
            if (!assertField(filter)) {
                return {
                    successful: false,
                    reason: `Invalid filter field: ${filter.split(opValuesRegex)[0]}`,
                    result: [],
                }
            }
            if (!assertOp(filter)) {
                return {
                    successful: false,
                    reason: "Invalid filter operator, or there is not exactly one operator in the filter.",
                    result: [],
                }
            }
            const op = filter.match(opValuesRegex)[0];
            const tokens = filter.split(op);
            result.push({
                field: tokens[0],
                op: op,
                value: tokens[1],
            })
        }
        return {
            successful: true,
            reason: "",
            result: result,
        }
    }

    function parseUserInput(filters) {
        if (filters === "") return [];
        if (filters === filters.split(" ")) return parseFilters([filters]);
        return parseFilters(filters.split(" "));
    }

    function onInput(value, setFilters) {
        const filterParsedResult = parseUserInput(value);
        if (!filterParsedResult.successful) {
            // todo: create and set some signals to show the error in the interface
            console.log("filterParsedResult: ", filterParsedResult.reason);
            return;
        }
        setFilters(filterParsedResult.result);
    }

    function init(setFilters) {
        const filterInputElement = document.getElementById("beatmap-query-filter");
        filterInputElement.addEventListener("input", (event) => onInput(event.target.value, setFilters));
    }

    return {
        init,
    }
}