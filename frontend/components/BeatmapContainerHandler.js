import { 
    selectedBeatmapSetId, setSelectedBeatmapSetId, 
    selectedBeatmapId, setSelectedBeatmapId 
} from "../app/settings.js";

export function BeatmapContainerHandler() {
    function onClickBeatmapRow(event) {
        const row = event.target.closest(".row");
        if (row.classList.contains("beatmap-set")) {
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
        else if (row.classList.contains("beatmap")) {
            const beatmapId = row.getElementsByClassName("beatmap-id")[0].innerHTML;
            const beatmapSetId = row.getElementsByClassName("beatmap-set-id")[0].innerHTML;
            if (beatmapId != selectedBeatmapId()) {
                setSelectedBeatmapId(beatmapId);
                if (beatmapSetId != selectedBeatmapSetId()) setSelectedBeatmapSetId(beatmapSetId);
            }
            else {
                setSelectedBeatmapId(undefined);
                setSelectedBeatmapSetId(undefined);
            }
        }
    }

    function init() {
        const beatmapListContainer = document.getElementById("beatmap-list-container");
        beatmapListContainer.addEventListener("click", (event) => onClickBeatmapRow(event));
        return beatmapListContainer;
    }

    return {
        init,
    }
}