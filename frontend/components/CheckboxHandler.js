import { createSignal } from "../reactive.js";

export function CheckboxHandler(parentId) {
    const [checkbox, setCheckbox] = createSignal();

    const checkboxParent = document.getElementById(parentId);
    const checkboxInput = checkboxParent.getElementsByTagName("input")[0];

    function init(initialValue=false) {
        checkboxInput.addEventListener("change", (event) => setCheckbox(event.target.checked));

        setCheckbox(initialValue);

        return [checkbox, setCheckbox];
    }

    return {
        init,
    }
}