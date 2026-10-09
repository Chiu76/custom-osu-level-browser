export function TypeHandler() {    
    let getter;
    let setter;

    function init(selectId, type, setType) {
        getter = type;
        setter = setType;

        const select = document.getElementById(selectId);
        setter(select.value);

        select.addEventListener("change", (event) => {
            setter(event.target.value);
        });
    }

    return {
        init,
    }
}