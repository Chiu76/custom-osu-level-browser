import { groupingQuery } from "../api.js";
import { RowBeatmapSet } from "./RowBeatmapSet.js";
import { RowBeatmap } from "./RowBeatmap.js";

export function GroupingContentHandler() {
    function queryGroupings(request) {
        return groupingQuery(request);
    }

    return {
        queryGroupings,
    }
}