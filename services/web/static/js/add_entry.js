if (document.getElementById("artwork_paste")) {
    document.getElementById("artwork_paste").addEventListener('click', async (e) => {
        try {
            const clipboardItems = await navigator.clipboard.read();
            console.log(clipboardItems.length);

            for (const clipboardItem of clipboardItems) {
                const itemImageType = Array.from(clipboardItem.types).find(type => type.startsWith('image/'));

                if (itemImageType) {
                    const imageBlob = await clipboardItem.getType(itemImageType);
                    console.log('image in cb - ' + itemImageType + ' - ' + imageBlob.size);
                    
                    document.getElementById("artwork_file").value = null;
                    processArtworkImage(imageBlob);                
    
                    return;
                }
            }
        } catch (err) {
            console.error(err.name, err.message);
        }
    });
}

if (document.getElementById("artwork_file")) {
    document.getElementById("artwork_file").addEventListener('change', (e) => {
        const uplFile = document.getElementById("artwork_file").files[0];

        if (uplFile.type.startsWith('image/')) {
            console.log('image uploaded - ' + uplFile.type + ' - ' + uplFile.size);
            processArtworkImage(uplFile);
        }
    });
}

if (document.getElementById("artwork_clear")) {
    document.getElementById("artwork_clear").addEventListener('click', (e) => {
        document.getElementById("artwork_file").value = null;

        imgDisplay = document.getElementById("artwork_preview");
		imgDisplay.src = null;
        if (!imgDisplay.classList.contains("hidden")) imgDisplay.classList.add("hidden");
        
        pasteField = document.getElementById("artwork");
        if (!pasteField.classList.contains("artwork_empty")) pasteField.classList.add("artwork_empty");
    });
}

async function processArtworkImage(pasteImage, maxSize = 800, quality = .89) {
    return new Promise((resolve) => {
        const reader = new FileReader();
        
        reader.onload = function(event) {
            const img = new Image();

            img.onload = function() {
                let width = img.width;
                let height = img.height;

                if (width > maxSize) {
                    height *= maxSize / width;
                    width = maxSize;
                }
                if (height > maxSize) {
                    width = maxSize / height;
                    height = maxSize;
                }

                const canvas = document.createElement('canvas');
                canvas.width = width;
                canvas.height = height;
                const canvasContext = canvas.getContext('2d');
                canvasContext.drawImage(img, 0, 0, width, height);

                canvas.toBlob(
                    (blob) => {
                        const fileInput = document.getElementById("artwork_file");
                        let newName;

                        if (fileInput.value) { 
                            newName = fileInput.files[0].name;
                            newName = newName.substring(0, newName.lastIndexOf(".")) + ".jpg";
                        }
                        else { 
                            newName = "pasted_image.jpg"; 
                        }
                        const processedImage = new File([blob], newName, { type: "image/jpeg" });

                        console.log('processed - ' + processedImage.type + ' - ' + processedImage.size );
                        const dataTransfer = new DataTransfer();
                        dataTransfer.items.add(processedImage);
                        document.getElementById("artwork_file").files = dataTransfer.files;
                        previewImage(processedImage);
                        //resolve(processedImage);
                    },
                    "image/jpeg",
                    quality
                );
            };

            img.src = event.target.result;
        };

        reader.readAsDataURL(pasteImage);
    });
}

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