document.addEventListener('DOMContentLoaded', function () {

    const popup = document.getElementById('quote-popup');
    if (!popup) return;

    let selectedText = '';

    document.addEventListener('selectionchange', handleSelection);
    document.addEventListener('mouseup', handleSelection);
    document.addEventListener('keyup', handleSelection);
    document.addEventListener('touchend', handleSelection);

    popup.addEventListener('click', function () {
        if (!selectedText || !window.TOPIC_ID) return;

        const text = encodeURIComponent(selectedText);

        window.location.href =
            `/topic/${window.TOPIC_ID}/comment/?quote=${text}`;
    });

    document.addEventListener('click', function (e) {
        if (!popup.contains(e.target)) {
            popup.classList.add('d-none');
        }
    });

    function handleSelection() {

        setTimeout(() => {

            const selection = window.getSelection();
            const text = selection.toString().trim();

            if (text.length < 2) {
                popup.classList.add('d-none');
                return;
            }

            const range = selection.rangeCount
                ? selection.getRangeAt(0)
                : null;

            if (!range) return;

            const container = range.commonAncestorContainer;
            const element = container.nodeType === 1
                ? container
                : container.parentElement;

            if (!element || !element.closest('.selectable-text')) {
                popup.classList.add('d-none');
                return;
            }

            selectedText = text;

            const rect = range.getBoundingClientRect();

            popup.style.top =
                (window.scrollY + rect.top - 42) + 'px';

            popup.style.left =
                (window.scrollX + rect.left) + 'px';

            popup.classList.remove('d-none');

        }, 10);
    }

});
