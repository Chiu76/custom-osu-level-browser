import { 
    selectedBeatmapSetId, setSelectedBeatmapSetId, 
    selectedBeatmapId, setSelectedBeatmapId, 
    beatmapFilter, setBeatmapFilter,
} from "../app/settings.js";

export function BeatmapContainerHandler() {
    function onClickBeatmapRow(event) {
        const row = event.target.closest(".row");
        if (row.classList.contains("beatmap-set")) {
            const beatmapSetId = row.getElementsByClassName("beatmap-set-id")[0].innerHTML;
            if (beatmapSetId != selectedBeatmapSetId()) {
                setSelectedBeatmapSetId(beatmapSetId);
                setSelectedBeatmapId(undefined);
            }
            else {
                setSelectedBeatmapSetId(undefined);
                setSelectedBeatmapId(undefined);
            }
        }
        else if (row.classList.contains("beatmap")) {
            console.log("coloi", event.target);
            const beatmapId = row.getElementsByClassName("beatmap-id")[0].innerHTML;
            const beatmapSetId = row.getElementsByClassName("beatmap-set-id")[0].innerHTML;
            if (beatmapId != selectedBeatmapId()) {
                setSelectedBeatmapId(beatmapId);
            }
            else {
                setSelectedBeatmapId(undefined);
            }
        }
    }

    function onRightClickBeatmapRow(event) {
        const inputElement = document.getElementById("beatmap-search-filter").getElementsByTagName("input")[0];
        if (event.target.classList[0] === "bpm") {
            const value = parseFloat(event.target.innerText.split(" ")[0]);
            const valueLower = (value - 5).toString()
            const valueHigher = (value + 5).toString()
            const filterValue = "".concat("bpm=", valueLower, "-", valueHigher);
            inputElement.value = filterValue;
        }
    }

    function init() {
        const beatmapListContainer = document.getElementById("beatmap-list-container");
        beatmapListContainer.addEventListener("click", (event) => onClickBeatmapRow(event));
        beatmapListContainer.addEventListener("contextmenu", (event) => { event.preventDefault(); onRightClickBeatmapRow(event) });
        return beatmapListContainer;
    }

    return {
        init,
    }
}