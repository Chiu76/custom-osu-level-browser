export function SearchHandler() {
    let getter;
    let setter;

    function init(id, search, setSearch) {
        getter = search;
        setter = setSearch;

        const searchParent = document.getElementById(id);
        const searchInput = searchParent.getElementsByTagName("input")[0];
        
        let timeout;
        searchInput.addEventListener("input", (event) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => setter(event.target.value), 250);
        });
    }

    return {
        init,
    }
}