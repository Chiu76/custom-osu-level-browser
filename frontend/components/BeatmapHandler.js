import { beatmapQuery } from "../api.js";
import { RowBeatmapSet } from "../components/RowBeatmapSet.js";
import { RowBeatmap } from "../components/RowBeatmap.js";

export function BeatmapHandler() {
    async function queryBeatmaps(request) {
        return await beatmapQuery(request);
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
                for (const beatmap of current) results.push({ type: "beatmap", content: beatmap });
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

    async function getDisplayRows(request) {
        return beatmapsToDisplayRows(await queryBeatmaps(request))
    }

    function displayRowToElement(displayRows, index) {
        const row = displayRows[index];
        return ( 
            row.type == "set" 
            ? RowBeatmapSet(row.content) 
            : RowBeatmap(row.content)
        );
    }

    return {
        getDisplayRows,
        displayRowToElement,
    }
}