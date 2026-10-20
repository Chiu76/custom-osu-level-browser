import { createSignal } from "../reactive.js";

import { BeatmapFilterHandler } from "../components/BeatmapFilterHandler.js";
import { BeatmapSortHandler } from "../components/BeatmapSortHandler.js";
import { SearchHandler } from "../components/SearchHandler.js";
import { GroupingTypeHandler } from "../components/GroupingTypeHandler.js";
import { ScoreTopByHandler } from "../components/ScoreTopByHandler.js";
import { CheckboxHandler } from "../components/CheckboxHandler.js";
import { ModFilterHandler } from "../components/ModFilterHandler.js";

const [beatmapSearch, setBeatmapSearch] = SearchHandler("beatmap-search").init();
const [beatmapFilter, setBeatmapFilter] = BeatmapFilterHandler().init();
const [beatmapSort, setBeatmapSort] = BeatmapSortHandler().init();

const [groupingSearch, setGroupingSearch] = SearchHandler("grouping-search").init();

const [sourceSpecs, setSourceSpecs] = createSignal([{ type: "local_beatmaps" }]);
const [groupingSpecs, setGroupingSpecs] = createSignal([{ type: "none" }]);

const [groupingType, setGroupingType] = GroupingTypeHandler().init();

const [selectedBeatmapSetId, setSelectedBeatmapSetId] = createSignal();
const [selectedBeatmapId, setSelectedBeatmapId] = createSignal();

const [selectedSourceId, setSelectedSourceId] = createSignal(undefined);
const [selectedGroupingId, setSelectedGroupingId] = createSignal(undefined);

const [scoreSortBy, setScoreSortBy] = ScoreTopByHandler("score-sort-by").init();
const [attachedScoreTopBy, setAttachedScoreTopBy] = ScoreTopByHandler("attached-score-top-by").init();
const [scoreRequired, setScoreRequired] = CheckboxHandler("score-required").init();

const [modsExactFilter, setModsExactFilter] = ModFilterHandler("mods-exact-filter").init();
const [modsIncludeFilter, setModsIncludeFilter] = ModFilterHandler("mods-include-filter").init();
const [modsExcludeFilter, setModsExcludeFilter] = ModFilterHandler("mods-exclude-filter").init();

const [disableBeatmapSets, setDisableBeatmapSets] = CheckboxHandler("disable-beatmap-sets").init();

export { 
    beatmapSearch, setBeatmapSearch,
    beatmapFilter, setBeatmapFilter, 
    beatmapSort, setBeatmapSort, 
    
    selectedBeatmapSetId, setSelectedBeatmapSetId, 
    selectedBeatmapId, setSelectedBeatmapId,

    groupingSearch, setGroupingSearch,
    groupingType, setGroupingType,
    
    sourceSpecs, setSourceSpecs,
    groupingSpecs, setGroupingSpecs,

    selectedSourceId, setSelectedSourceId,
    selectedGroupingId, setSelectedGroupingId,

    scoreSortBy, setScoreSortBy,
    attachedScoreTopBy, setAttachedScoreTopBy,
    scoreRequired, setScoreRequired,

    modsExactFilter, setModsExactFilter,	
    modsIncludeFilter, setModsIncludeFilter,
    modsExcludeFilter, setModsExcludeFilter,

    disableBeatmapSets, setDisableBeatmapSets,
};