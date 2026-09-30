import { createSignal, createEffect, createMemo } from "../reactive.js";

import { useFilterParser } from "../hooks/useFilterParser.js";


const [q, setQ] = createSignal("");
const [filters, setFilters] = createSignal([]);
const [sortings, setSortings] = createSignal("");

function onInputSearch(event) {
    setQ(event.value);
}

const filterParser = useFilterParser();

function onInputFilter(event) {
    const filterParsedResult = filterParser.parseUserInput(event.value);
    if (!filterParsedResult.successful) {
        // todo: create and set some signals to show the error in the interface
        console.log("filterParsedResult: ", filterParsedResult.reason);
        return;
    }
    setFilters(filterParsedResult.result);
}

function onInputSort(event) {
    setSortings(event.value);
}

window.onInputSearch = onInputSearch;
window.onInputFilter = onInputFilter;
window.onInputSort = onInputSort;

export { q, setQ , filters, setFilters, sortings, setSortings };