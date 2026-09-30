import { createSignal, createEffect, createMemo } from "../reactive.js";

import { useFilterHandler } from "../hooks/useFilterHandler.js";
import { useSortHandler } from "../hooks/useSortHandler.js";


const [q, setQ] = createSignal("");
const [filters, setFilters] = createSignal([]);
const [sortPrimary, setSortPrimary] = createSignal("");
const [sortSecondary, setSortSecondary] = createSignal("");

function onInputSearch(event) {
    setQ(event.value);
}
window.onInputSearch = onInputSearch;

const filterHandler = useFilterHandler();
filterHandler.init(setFilters);

const sortHandler = useSortHandler();
sortHandler.init(setSortPrimary, setSortSecondary);

export { q, setQ , filters, setFilters, sortPrimary, setSortPrimary, sortSecondary, setSortSecondary };