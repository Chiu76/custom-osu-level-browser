import { createSignal, createEffect, createMemo } from "../reactive.js";

import { BeatmapFilterHandler } from "../components/BeatmapFilterHandler.js";
import { BeatmapSortHandler } from "../components/BeatmapSortHandler.js";
import { SearchHandler } from "../components/SearchHandler.js";
import { GroupingTypeHandler } from "../components/GroupingTypeHandler.js";
import { ScoreTopByHandler } from "../components/ScoreTopByHandler.js";

const [beatmapSearch, setBeatmapSearch] = SearchHandler().init("beatmap-search");
const [beatmapFilter, setBeatmapFilter] = BeatmapFilterHandler().init();
const [beatmapSort, setBeatmapSort] = BeatmapSortHandler().init();

const [groupingSearch, setGroupingSearch] = SearchHandler().init("grouping-search");

const [sourceSpec, setSourceSpec] = createSignal({ type: "local_beatmaps" });
const [groupingSpec, setGroupingSpec] = createSignal({ type: "none" });

const [groupingType, setGroupingType] = GroupingTypeHandler().init();

const [selectedBeatmapSetId, setSelectedBeatmapSetId] = createSignal();
const [selectedBeatmapId, setSelectedBeatmapId] = createSignal();

const [selectedSourceId, setSelectedSourceId] = createSignal(undefined);
const [selectedGroupingId, setSelectedGroupingId] = createSignal(undefined);

const [scoreTopBy, setScoreTopBy] = ScoreTopByHandler().init();
 
export { 
    beatmapSearch, setBeatmapSearch,
    beatmapFilter, setBeatmapFilter, 
    beatmapSort, setBeatmapSort, 
    
    selectedBeatmapSetId, setSelectedBeatmapSetId, 
    selectedBeatmapId, setSelectedBeatmapId,

    groupingSearch, setGroupingSearch,
    groupingType, setGroupingType,
    
    sourceSpec, setSourceSpec,
    groupingSpec, setGroupingSpec,

    selectedSourceId, setSelectedSourceId,
    selectedGroupingId, setSelectedGroupingId,

    scoreTopBy, setScoreTopBy,
};