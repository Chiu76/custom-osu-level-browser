import { createSignal, createEffect, createMemo } from "../reactive.js";

import { FilterHandler } from "../components/FilterHandler.js";
import { SortHandler } from "../components/SortHandler.js";

const [q, setQ] = createSignal("");
const [filters, setFilters] = createSignal([]);
const [sort, setSort] = createSignal([]);

function onInputSearch(event) {
    setQ(event.value);
}
window.onInputSearch = onInputSearch;

const filterHandler = FilterHandler();
filterHandler.init(setFilters);

const sortHandler = SortHandler();
sortHandler.init(sort, setSort);

export { q, setQ , filters, setFilters, sort, setSort };