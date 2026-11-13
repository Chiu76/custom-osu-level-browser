import { createSignal } from "../reactive.js";
import { schemas } from "../utils.js";
import { SelectHandler } from "./SelectHandler.js";
import { DirHandler } from "./DirHandler.js";

export function StarRatingModsHandler() {
    const [starRatingMods, setStarRatingMods] = createSignal();
    
    const modsValues = ["NM", "HR", "DT", "DTHR"]
    
    const parentElement = document.getElementById("star-rating-mods");
    const selectElement = parentElement.getElementsByTagName("select")[0];

    function modsToInt(mods) {
        const mapping = {
            "NM": 0,
            "HR": 16,
            "HR": 64,
            "DTHR": 80,
        };
        return mapping[mods];
    }

    function selectOnChange(field) {
        setStarRatingMods(modsToInt(field));
    }

    function init() {
        SelectHandler().init(selectElement, selectOnChange, modsValues);

        selectOnChange(selectElement.value);

        return [starRatingMods, setStarRatingMods]
    }

    return {
        init,
    };
}