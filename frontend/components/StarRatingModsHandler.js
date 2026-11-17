import { createSignal } from "../reactive.js";
import { schemas } from "../utils.js";
import { SelectHandler } from "./SelectHandler.js";
import { DirHandler } from "./DirHandler.js";

export function StarRatingModsHandler() {
    const [starRatingMods, setStarRatingMods] = createSignal();
    
    const parentElement = document.getElementById("star-rating-mods");
    const selectElement = parentElement.getElementsByTagName("select")[0];

    const modsValues = {
        "NM": ["nm"],
        "HR": ["hr"],
        "DT": ["dt"],
        "DTHR": ["dt", "hr"],
    }

    function selectOnChange(field) {
        setStarRatingMods(modsValues[field]);
    }

    function init() {
        SelectHandler().init(selectElement, selectOnChange, Object.keys(modsValues));

        selectOnChange(selectElement.value);

        return [starRatingMods, setStarRatingMods]
    }

    return {
        init,
    };
}