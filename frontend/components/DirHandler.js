export function DirHandler() {
    function init(dirElement, associatedElement, defaultDir="asc") {
        dirElement.innerText = defaultDir;
        dirElement.addEventListener("click", () => { 
            if (dirElement.innerText == "asc") dirElement.innerText = "desc";
            else if (dirElement.innerText == "desc") dirElement.innerText = "asc";
            associatedElement.dispatchEvent(new Event("change"));
        });
    }

    return {
        init,
    };
}