import { 
    selectedSourceId, setSelectedSourceId,
    selectedGroupingId, setSelectedGroupingId, 
} from "../app/settings.js";

export function GroupingContainerHandler() {
    function setActiveSource(element) {
        const prevSelected = document.getElementById(selectedSourceId());
        if (prevSelected == undefined) {
            element.querySelector(".source-marker").classList.toggle("hidden");
            setSelectedSourceId(element.id);
        }
        else {
            if (prevSelected.id != element.id) {
                prevSelected.querySelector(".source-marker").classList.toggle("hidden");
                setSelectedSourceId(element.id);
            }
            else {
                setSelectedSourceId(undefined);
            }
            element.querySelector(".source-marker").classList.toggle("hidden");
        }
    }

    function clearActiveSource() {
        const prevSelected = document.getElementById(selectedSourceId());
        if (prevSelected != undefined) {
            prevSelected.querySelector(".source-marker").classList.toggle("hidden");
        }
        setSelectedSourceId(undefined)
    }

    function setActiveGrouping(element) {
        const prevSelected = document.getElementById(selectedGroupingId());
        if (prevSelected == undefined) {
            element.querySelector(".grouping-marker").classList.toggle("hidden");
            setSelectedGroupingId(element.id);
        }
        else {
            if (prevSelected.id != element.id) {
                prevSelected.querySelector(".grouping-marker").classList.toggle("hidden");
                setSelectedGroupingId(element.id);
            }
            else {
                setSelectedGroupingId(undefined);
            }
            element.querySelector(".grouping-marker").classList.toggle("hidden");
        }
    }

    function clearActiveGrouping() {
        const prevSelected = document.getElementById(selectedGroupingId());
        if (prevSelected != undefined) {
            prevSelected.querySelector(".grouping-marker").classList.toggle("hidden");
        }
        setSelectedGroupingId(undefined)
    }

    function getGroupingNameFromId(id) {
        return document.getElementById(id).querySelector(".name").innerHTML;
    }

    function init() {
        const groupingListContainer = document.getElementById("grouping-list-container");
        // groupingListContainer.addEventListener("click", (event) => onClickBeatmapRow(event));
        return groupingListContainer;
    }

    return {
        init,
        setActiveSource,
        clearActiveSource,
        setActiveGrouping,
        clearActiveGrouping,
        getGroupingNameFromId,
    }
}