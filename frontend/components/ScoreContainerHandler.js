export function ScoreContainerHandler() {
    function init() {
        const scoreListContainer = document.getElementById("score-list-container");
        scoreListContainer.addEventListener("contextmenu", (event) => { event.preventDefault(); });
        return scoreListContainer;
    }

    return {
        init,
    }
}