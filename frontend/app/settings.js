import { createSignal, createEffect, createMemo } from "../reactive.js";

import { FilterHandler } from "../components/FilterHandler.js";
import { SortHandler } from "../components/SortHandler.js";
import { SearchHandler } from "../components/SearchHandler.js";
import { TypeHandler } from "../components/TypeHandler.js";

const [search, setSearch] = createSignal("");
const [filter, setFilter] = createSignal([]);
const [sort, setSort] = createSignal([]);

const beatmapSearchHandler = SearchHandler();
beatmapSearchHandler.init("beatmap-search", search, setSearch);

const beatmapFilterHandler = FilterHandler();
beatmapFilterHandler.init("beatmap-filter", filter, setFilter);

const beatmapSortHandler = SortHandler();
beatmapSortHandler.init(sort, setSort);

const [groupingSearch, setGroupingSearch] = createSignal("");
const [groupingType, setGroupingType] = createSignal();

const [sourceSpec, setSourceSpec] = createSignal({ type: "local_beatmaps" });
const [groupingSpec, setGroupingSpec] = createSignal({ type: "none" });

const groupingSearchHandler = SearchHandler();
groupingSearchHandler.init("grouping-search", groupingSearch, setGroupingSearch);

const groupingTypeHandler = TypeHandler();
groupingTypeHandler.init("grouping-type-select", groupingType, setGroupingType);

const [selectedBeatmapSetId, setSelectedBeatmapSetId] = createSignal();
const [selectedBeatmapId, setSelectedBeatmapId] = createSignal();

const [selectedSourceId, setSelectedSourceId] = createSignal(undefined);
const [selectedGroupingId, setSelectedGroupingId] = createSignal(undefined);

export { 
    search, setSearch,
    filter, setFilter, 
    sort, setSort, 
    
    selectedBeatmapSetId, setSelectedBeatmapSetId, 
    selectedBeatmapId, setSelectedBeatmapId,

    groupingSearch, setGroupingSearch,
    groupingType, setGroupingType,
    
    sourceSpec, setSourceSpec,
    groupingSpec, setGroupingSpec,

    selectedSourceId, setSelectedSourceId,
    selectedGroupingId, setSelectedGroupingId,
};