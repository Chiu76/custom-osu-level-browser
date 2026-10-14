import { createSignal } from "../reactive.js";
import { schemas } from "../utils.js";
import { SelectHandler } from "./SelectHandler.js";

export function GroupingTypeHandler() {
    const [groupingType, setGroupingType] = createSignal();
    
    const groupingTypeValues = schemas["GroupingType"]["enum"].sort();
    
    const parentElement = document.getElementById("grouping-type");
    const selectElement = parentElement.getElementsByTagName("select")[0];

    function selectOnChange(field) {
        setGroupingType({
            field: field,
        });
    }

    function init() {
        SelectHandler().init(selectElement, selectOnChange, groupingTypeValues);

        setGroupingType(selectElement.value);

        return [groupingType, setGroupingType]
    }

    return {
        init,
    };
}