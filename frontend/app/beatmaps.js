import { createSignal, createEffect, createMemo } from "../reactive.js";

import { BeatmapContentHandler } from "../components/BeatmapContentHandler.js";
import { BeatmapContainerHandler } from "../components/BeatmapContainerHandler.js";
import { 
    beatmapSearch, beatmapFilter, beatmapSort, 
    selectedBeatmapId, selectedBeatmapSetId,
    selectedGroupingId, selectedSourceId,
    groupingType,
    sourceSpec, groupingSpec,
    scoreTopBy, setScoreTopBy,
} from "./settings.js";

function buildRequest(searchSpec, filterSpec, sortSpec, sourceSpec, groupingSpec, score_top_by) {
    return {
        core_specs: {
            star_rating_spec: {},
            attached_score_spec: {
                score_sq_spec: {
                    top_by: score_top_by,
                    top_score_only: true,
                    mods_exact: [],
                    mods_include: [],
                    mods_exclude: [],
                },
                score_required: true,
            },
            online_details_spec: {},
            source_spec: sourceSpec,
            filter_spec: filterSpec,
        },
        presentation_specs: {
            search_spec: searchSpec,
            grouping_spec: groupingSpec,
            sort_spec: sortSpec,
        }
    }
}

const [request, setRequest] = createSignal();
const [beatmapQueryRows, setBeatmapQueryRows] = createSignal([]);

createEffect(() => {
    const searchSpec = { q: beatmapSearch() };
    const filterSpec = { filters: beatmapFilter() };
    const sortSpec = { sort_columns: beatmapSort() };
    // const groupingSpec = { type: groupingType(), id: selectedGroupingId() };
    const source_spec = sourceSpec();
    const grouping_spec = groupingSpec();
    const score_top_by = scoreTopBy();
    const req = buildRequest(searchSpec, filterSpec, sortSpec, source_spec, grouping_spec, score_top_by);
    console.log("beatmaps: request-building effect: req:", req);
    setRequest(req);
});

const beatmapContainerHandler = BeatmapContainerHandler();
const beatmapContainer = beatmapContainerHandler.init();

const beatmapContentHandler = BeatmapContentHandler();

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

const displayRows = createMemo(() => {
    const beatmaps = beatmapQueryRows();
    const currentSelectBeatmapId = selectedBeatmapId();
    const currentSelectedBeatmapSetId = selectedBeatmapSetId();
    // const currentSelectedGroupingId = selectedGroupingId();
    // const currentSelectedSourceId = selectedSourceId();
    return beatmapContentHandler.beatmapsToDisplayRows(beatmaps, currentSelectedBeatmapSetId);
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