export function ScoreContainerHandler() {
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

    function init() {
        const groupingListContainer = document.getElementById("score-list-container");
        groupingListContainer.addEventListener("click", (event) => toggleActiveGrouping(event));
        groupingListContainer.addEventListener("contextmenu", (event) => { event.preventDefault(); toggleActiveSource(event); });
        return groupingListContainer;
    }

    return {
        init,
    }
}