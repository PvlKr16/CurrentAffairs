document.addEventListener("DOMContentLoaded", function () {

    const dropZone = document.getElementById("drop-zone");
    const fileInput = document.getElementById("file-input");
    const previewBox = document.getElementById("preview-box");

    if (!dropZone || !fileInput) return;

    let filesList = [];

    // ---------------- CLICK ----------------
    dropZone.addEventListener("click", () => fileInput.click());

    // ---------------- DRAG ----------------
    dropZone.addEventListener("dragover", e => {
        e.preventDefault();
        dropZone.classList.add("dragover");
    });

    dropZone.addEventListener("dragleave", () => {
        dropZone.classList.remove("dragover");
    });

    dropZone.addEventListener("drop", e => {
        e.preventDefault();
        dropZone.classList.remove("dragover");

        addFiles(e.dataTransfer.files);
    });

    // ---------------- INPUT ----------------
    fileInput.addEventListener("change", () => {
        addFiles(fileInput.files);
    });

    // ---------------- CORE ----------------
    function addFiles(newFiles) {
        for (let file of newFiles) {
            filesList.push(file);
        }
        syncInput();
        renderPreview();
    }

    function removeFile(index) {
        filesList.splice(index, 1);
        syncInput();
        renderPreview();
    }

    function syncInput() {
        const dataTransfer = new DataTransfer();

        filesList.forEach(file => dataTransfer.items.add(file));

        fileInput.files = dataTransfer.files;
    }

    function renderPreview() {
        previewBox.innerHTML = "";

        filesList.forEach((file, index) => {

            const el = document.createElement("div");
            el.className = "file-card mb-2 p-2 border rounded d-flex justify-content-between align-items-center";

            el.innerHTML = `
                <div>
                    <strong>${file.name}</strong><br>
                    <small>${(file.size / 1024).toFixed(1)} KB</small>
                </div>

                <button type="button"
                        class="btn btn-sm btn-danger">
                    ✕
                </button>
            `;

            el.querySelector("button").addEventListener("click", () => {
                removeFile(index);
            });

            previewBox.appendChild(el);
        });
    }

});
