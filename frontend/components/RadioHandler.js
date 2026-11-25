import { createSignal } from "../reactive.js";
import { schemas } from "../utils.js";

export function RadioHandler(parentId) {
    const [radio, setRadio] = createSignal();

    const radioParent = document.getElementById(parentId);
    const radioInputs = radioParent.getElementsByTagName("input");

    function init(values, name) {
        for (const value of values) {
            const input = document.createElement("input");
            input.type = "radio";
            input.name = name;
            input.value = value;
            input.id = name.concat("-", value);

            const label = document.createElement("label");
            label.htmlFor = name.concat("-", value);
            label.innerText = value;

            input.addEventListener("change", (event) => setRadio(event.target.value));
            
            radioParent.appendChild(input)
            radioParent.appendChild(label)
        }

        radioInputs[0].checked = true;
        radioInputs[0].dispatchEvent(new Event("change"));

        return [radio, setRadio];
    }

    return {
        init,
    }
}