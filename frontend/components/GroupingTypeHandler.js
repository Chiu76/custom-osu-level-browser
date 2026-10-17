import { createSignal } from "../reactive.js";
import { schemas } from "../utils.js";
import { SelectHandler } from "./SelectHandler.js";

export function GroupingTypeHandler() {
    const [groupingType, setGroupingType] = createSignal();
    
    const groupingTypeValues = schemas["GroupingIdentifier"]["properties"]["type"]["enum"].sort();
    
    const parentElement = document.getElementById("grouping-type-select");
    const selectElement = parentElement.getElementsByTagName("select")[0];

    function selectOnChange(field) {
        setGroupingType(field);
    }

    function init() {
        const selectHandler = SelectHandler();
        selectHandler.init(selectElement, selectOnChange, groupingTypeValues);
        selectHandler.updateSelect(selectElement, "collections");

        return [groupingType, setGroupingType];
    }

    return {
        init,
    };
}