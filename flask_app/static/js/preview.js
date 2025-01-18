console.log("connected")

// Get the file input and the preview image element
const fileInput = document.getElementById('pic_location');
const previewImage = document.getElementById('preview');

// Listen for changes in the file input
fileInput.addEventListener('change', function(event) {
    console.log("event triggered")
    const file = event.target.files[0]; // Get the selected file
    if (file) {
        const reader = new FileReader();

        // When the file is loaded, set the image source to the result
        console.log("image loaded")
        reader.onload = function(e) {
            previewImage.src = e.target.result;
            previewImage.style.display = 'block'; // Show the image
        };

        reader.readAsDataURL(file); // Read the file as a data URL
    }
});