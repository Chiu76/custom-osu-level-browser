import { createSignal } from "../reactive.js";
import { schemas } from "../utils.js";
import { SelectHandler } from "./SelectHandler.js";
import { DirHandler } from "./DirHandler.js";

export function ScoreTopByHandler(parentId) {
    const [attachedScoreTopBy, setAttachedScoreTopBy] = createSignal();
    
    const topByValues = schemas["TopBy"]["properties"]["field"]["enum"].sort();
    
    const parentElement = document.getElementById(parentId);
    const selectElement = parentElement.getElementsByTagName("select")[0];
    const dirElement = parentElement.getElementsByClassName("dir")[0];

    function selectOnChange(field) {
        setAttachedScoreTopBy({
            field: field,
            dir: dirElement.innerText,
        });
    }

    function init() {
        SelectHandler().init(selectElement, selectOnChange, topByValues);
        DirHandler().init(dirElement, selectElement, "desc");

        selectOnChange(selectElement.value);

        return [attachedScoreTopBy, setAttachedScoreTopBy]
    }

    return {
        init,
    };
}