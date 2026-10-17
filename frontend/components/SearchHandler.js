import { createSignal } from "../reactive.js";

export function SearchHandler(parentId) {
    const [search, setSearch] = createSignal("");

    const searchParent = document.getElementById(parentId);
    const searchInput = searchParent.getElementsByTagName("input")[0];

    function init() {
        let timeout;
        searchInput.addEventListener("input", (event) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => setSearch(event.target.value), 250);
        });

        return [search, setSearch];
    }

    return {
        init,
    }
}