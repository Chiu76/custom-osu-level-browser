import { groupingQuery } from "../api.js";
import { RowBeatmapSet } from "./RowBeatmapSet.js";
import { RowBeatmap } from "./RowBeatmap.js";

export function GroupingContentHandler() {
    function queryGroupings(request) {
        return groupingQuery(request);
    }

    function beatmapsToDisplayRows(beatmaps, selectedSetId) {
        const results = [];
        let current = [];

        function flushCurrent() {
            if (current.length === 0) return;
            results.push(current.length > 1
                ? { type: "set", content: current }
                : { type: "beatmap", content: current[0] }
            );
            if (current.length > 1 && current[0].beatmap_set_id == selectedSetId) {
                for (const row of current) results.push({ type: "beatmap", content: row });
            }
            current = [];
        }

        for (const beatmap of beatmaps) {
            if (current.length > 0 && beatmap.beatmap_set_id !== current[0].beatmap_set_id) {
                flushCurrent();
            }
            current.push(beatmap);
        }
        flushCurrent(current);

        return results;
    }

    function displayRowToElement(rows, index) {
        const row = rows[index];
        return ( 
            row.type == "set" 
            ? RowBeatmapSet(row.content) 
            : RowBeatmap(row.content)
        );
    }

    return {
        queryGroupings,
    }
}