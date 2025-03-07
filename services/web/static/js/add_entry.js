document.addEventListener('paste', async (e) => {
    e.preventDefault();
    console.log(e.clipboardData.files.length);
    
    for (const clipboardItem of e.clipboardData.files) {
        if (clipboardItem.type.startsWith('image/')) {
            console.log('image in cb');
		    previewImage(clipboardItem);
            document.getElementById("artwork_file").value = null;
            return;
        }
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