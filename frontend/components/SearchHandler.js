export function SearchHandler() {
    let getSearchSignalRef;
    let setSearchSignalRef;

    function init(search, setSearch) {
        getSearchSignalRef = search;
        setSearchSignalRef = setSearch;

        const searchParent = document.getElementById("search");
        const searchInput = searchParent.getElementsByTagName("input")[0];
        
        let timeout;
        searchInput.addEventListener("input", (event) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => setSearchSignalRef(event.target.value), 250);
        });
    }

    return {
        init,
    }
}