import { createSignal } from "../reactive.js";

export function CheckboxHandler() {
    const [checkbox, setCheckbox] = createSignal();

    function init(id) {
        const checkboxParent = document.getElementById(id);
        const checkboxInput = checkboxParent.getElementsByTagName("input")[0];
        
        checkboxInput.addEventListener("change", (event) => setCheckbox(event.target.checked));

        setCheckbox(checkboxInput.checked);

        return [checkbox, setCheckbox];
    }

    return {
        init,
    }
}