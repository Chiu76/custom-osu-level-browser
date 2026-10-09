import { 
    selectedSourceId, setSelectedSourceId,
    selectedGroupingId, setSelectedGroupingId, 
} from "../app/settings.js";

export function GroupingContainerHandler() {
    function toggleActiveSource(event) {
        const row = event.target.closest(".row");
        const prevSelectedId = selectedSourceId();
        if (prevSelectedId == undefined) {
            setSelectedSourceId(row.id);
        }
        else {
            if (prevSelectedId != row.id) {
                setSelectedSourceId(row.id);
            }
            else {
                setSelectedSourceId(undefined);
            }
        }
    }

    function toggleActiveGrouping(event) {
        const row = event.target.closest(".row");
        const prevSelectedId = selectedGroupingId();
        if (prevSelectedId == undefined) {
            setSelectedGroupingId(row.id);
        }
        else {
            if (prevSelectedId != row.id) {
                setSelectedGroupingId(row.id);
            }
            else {
                setSelectedGroupingId(undefined);
            }
        }
    }

    function clearActiveSource() {
        const prevSelected = document.getElementById(selectedSourceId());
        if (prevSelected != undefined) {
            prevSelected.querySelector(".source-marker").classList.toggle("hidden");
        }
        setSelectedSourceId(undefined)
    }

    function clearActiveGrouping() {
        const prevSelected = document.getElementById(selectedGroupingId());
        if (prevSelected != undefined) {
            prevSelected.querySelector(".grouping-marker").classList.toggle("hidden");
        }
        setSelectedGroupingId(undefined)
    }

    function init() {
        const groupingListContainer = document.getElementById("grouping-list-container");
        groupingListContainer.addEventListener("click", (event) => toggleActiveGrouping(event));
        groupingListContainer.addEventListener("contextmenu", (event) => { event.preventDefault(); toggleActiveSource(event); });
        return groupingListContainer;
    }

    return {
        init,
        clearActiveSource,
        clearActiveGrouping,
    }
}