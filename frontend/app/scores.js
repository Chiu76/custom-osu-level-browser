let selectedScoreId = undefined;

const scoreOnClick = (element) => {
    const prevSelected = document.getElementById(selectedScoreId);
    if (prevSelected == undefined) {
        element.classList.toggle("highlighted");
        selectedScoreId = element.id;
    }
    else {
        if (prevSelected.id != element.id) {
            prevSelected.classList.toggle("highlighted")
            selectedScoreId = element.id;
        }
        else {
            selectedScoreId = undefined;
        }
        element.classList.toggle("highlighted");
    }
};

window.scoreOnClick = scoreOnClick;