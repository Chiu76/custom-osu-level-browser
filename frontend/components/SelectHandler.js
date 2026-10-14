export function SelectHandler() {
    function updateSelect(selectElement, value) {
        selectElement.value = value;
        selectElement.dispatchEvent(new Event("change"));
    }

    function createElementOption(value) {
        const option = document.createElement("option");
        option.value = value;
        option.innerText = value;
        return option;
    }

    function init(selectElement, selectOnChange, options=[]) {
        for (let option of options) {
            selectElement.appendChild(createElementOption(option));
        }

        selectElement.addEventListener("change", (event) => {
            selectOnChange(event.target.value);
        });
    }

    return {
        init,
        updateSelect,
    }
}