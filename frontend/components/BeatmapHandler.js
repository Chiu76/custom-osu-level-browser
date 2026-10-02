import { beatmapQuery } from "../api.js";
import { RowBeatmapSet } from "../components/RowBeatmapSet.js";
import { RowBeatmap } from "../components/RowBeatmap.js";

import { 
    selectedBeatmapSetId, setSelectedBeatmapSetId, 
    selectedBeatmapId, setSelectedBeatmapId 
} from "../app/settings.js";

export function BeatmapHandler() {
    function onClickBeatmapRow(event) {
        const row = event.target;
        if (row.className == "row-beatmap-set") {
            const beatmapSetId = row.getElementsByClassName("beatmap-set-id")[0].innerHTML;
            if (beatmapSetId == selectedBeatmapSetId()) {
                setSelectedBeatmapSetId(undefined);
                setSelectedBeatmapId(undefined);
            }
            else {
                setSelectedBeatmapSetId(beatmapSetId);
                setSelectedBeatmapId(undefined);
            }
        }
        else if (row.className == "row-beatmap") {
            const beatmapId = row.getElementsByClassName("beatmap-id")[0].innerHTML;;
            const beatmapSetId = row.getElementsByClassName("beatmap-set-id")[0].innerHTML;;
            if (beatmapId != selectedBeatmapId()) {
                setSelectedBeatmapId(beatmapId);
                if (beatmapSetId == selectedBeatmapSetId()) setSelectedBeatmapSetId(undefined);
                else setSelectedBeatmapSetId(beatmapSetId);
            }
            else {
                setSelectedBeatmapId(undefined);
                setSelectedBeatmapSetId(undefined);
            }
        }
    }

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
        onClickBeatmapRow,
    }
}