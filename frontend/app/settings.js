import { createSignal, createEffect, createMemo } from "../reactive.js";

import { FilterHandler } from "../components/FilterHandler.js";
import { SortHandler } from "../components/SortHandler.js";
import { SearchHandler } from "../components/SearchHandler.js";

const [search, setSearch] = createSignal("");
const [filter, setFilter] = createSignal([]);
const [sort, setSort] = createSignal([]);

const searchHandler = SearchHandler();
searchHandler.init(search, setSearch);

const filterHandler = FilterHandler();
filterHandler.init(filter, setFilter);

const sortHandler = SortHandler();
sortHandler.init(sort, setSort);

export { search, setSearch, filter, setFilter, sort, setSort };