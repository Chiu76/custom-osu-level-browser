import { createSignal, createEffect, createMemo } from "../reactive.js";

import { BeatmapContentHandler } from "../components/BeatmapContentHandler.js";
import { BeatmapContainerHandler } from "../components/BeatmapContainerHandler.js";
import { 
    beatmapSearch, beatmapFilter, beatmapSort, 
    selectedBeatmapId, selectedBeatmapSetId,
    selectedGroupingId, selectedSourceId,
    groupingType, setGroupingType,
    sourceSpec, groupingSpec,
    scoreTopBy, setScoreTopBy,
    scoreRequired, setScoreRequired,
    modsExactFilter, setModsExactFilter,	
    modsIncludeFilter, setModsIncludeFilter,
    modsExcludeFilter, setModsExcludeFilter,
    disableBeatmapSets, setDisableBeatmapSets,
} from "./settings.js";

function buildRequest(search_spec, filter_spec, sort_spec, source_spec, grouping_spec, top_by, score_required, mods_exact, mods_include, mods_exclude) {
    return {
        core_specs: {
            star_rating_spec: {},
            attached_score_spec: {
                score_sq_spec: {
                    top_by: top_by,
                    top_score_only: true,
                    mods_exact: mods_exact,
                    mods_include: mods_include,
                    mods_exclude: mods_exclude,
                },
                score_required: score_required,
            },
            online_details_spec: {},
            source_spec: source_spec,
            filter_spec: filter_spec,
        },
        presentation_specs: {
            search_spec: search_spec,
            grouping_spec: grouping_spec,
            sort_spec: sort_spec,
        }
    }
}

const [request, setRequest] = createSignal();

createEffect(() => {
    const search_spec = { q: beatmapSearch() };
    const filter_spec = { filters: beatmapFilter() };
    const sort_spec = { sort_columns: beatmapSort() };
    // const groupingSpec = { type: groupingType(), id: selectedGroupingId() };
    const source_spec = sourceSpec();
    const grouping_spec = groupingSpec();
    const top_by = scoreTopBy();
    const score_required = scoreRequired();
    const mods_exact = modsExactFilter();
    const mods_include = modsIncludeFilter();
    const mods_exclude = modsExcludeFilter();
    const newRequest = buildRequest(search_spec, filter_spec, sort_spec, source_spec, grouping_spec, top_by, score_required, mods_exact, mods_include, mods_exclude);
    console.log("beatmaps: newRequest:", newRequest);
    setRequest(newRequest);
});

const beatmapContentHandler = BeatmapContentHandler();
const [beatmapQueryRows, setBeatmapQueryRows] = createSignal([]);

let latestId = 0;
createEffect(() => {
    const req = request();
    const id = ++latestId;
    beatmapContentHandler.queryBeatmaps(req)
        .then(response => { 
            if (id !== latestId) return;
            setBeatmapQueryRows(response.rows);
            virtualizedList?.scrollToIndex(0, "start");
        });
})

const beatmapContainerHandler = BeatmapContainerHandler();
const beatmapContainer = beatmapContainerHandler.init();

const displayRows = createMemo(() => {
    const beatmaps = beatmapQueryRows();
    const currentSelectBeatmapId = selectedBeatmapId();
    const currentSelectedBeatmapSetId = selectedBeatmapSetId();
    // const currentSelectedGroupingId = selectedGroupingId();
    // const currentSelectedSourceId = selectedSourceId();
    return beatmapContentHandler.beatmapsToDisplayRows(beatmaps, currentSelectedBeatmapSetId, disableBeatmapSets());
})

var VirtualizedList = window.VirtualizedList.default;
let virtualizedList = null;
createEffect(() => {
    const rows = displayRows();
    
    if (rows.length === 0) {
        virtualizedList?.destroy();
        virtualizedList = null;
        return;
    }
    if (!virtualizedList) {
        virtualizedList = new VirtualizedList(beatmapContainer, {
            height: 672, rowHeight: 96, rowCount: rows.length,
            renderRow: (index) => beatmapContentHandler.displayRowToElement(displayRows(), index),
        });
    }
    else {
        virtualizedList.setRowCount(rows.length);
    }
});

export { request };