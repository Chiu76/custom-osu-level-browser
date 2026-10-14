import { createSignal } from "../reactive.js";

export function SearchHandler() {
    const [search, setSearch] = createSignal("");

    function init(id) {
        const searchParent = document.getElementById(id);
        const searchInput = searchParent.getElementsByTagName("input")[0];
        
        let timeout;
        searchInput.addEventListener("input", (event) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => setter(event.target.value), 250);
        });

        return [search, setSearch];
    }

    return {
        init,
    }
}