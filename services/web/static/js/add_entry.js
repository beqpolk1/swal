document.getElementById("artwork_paste").addEventListener('click', async (e) => {
    try {
        const clipboardItems = await navigator.clipboard.read();
        console.log(clipboardItems.length);

        for (const clipboardItem of clipboardItems) {
            const itemImageType = Array.from(clipboardItem.types).find(type => type.startsWith('image/'));

            if (itemImageType) {
                console.log('image in cb');

                const imageBlob = await clipboardItem.getType(itemImageType);
                previewImage(imageBlob);

                document.getElementById("artwork_file").value = null;
                return;
            }
        }
    } catch (err) {
        console.error(err.name, err.message);
    }
});

document.getElementById("artwork_file").addEventListener('change', (e) => {
    const uplFile = document.getElementById("artwork_file").files[0];
    if (uplFile) previewImage(uplFile);
});

function previewImage(imgFile) {
	let reader = new FileReader();

	reader.onload = e => {
        imgDisplay = document.getElementById("artwork_preview");
		imgDisplay.src = e.target.result;
        if (imgDisplay.classList.contains("hidden")) imgDisplay.classList.remove("hidden");
        
        pasteField = document.getElementById("artwork");
        if (pasteField.classList.contains("artwork_empty")) pasteField.classList.remove("artwork_empty");
	}

	reader.readAsDataURL(imgFile);
}