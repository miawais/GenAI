document.getElementById('invoiceForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const inputPrompt = document.getElementById('inputPrompt').value;
    const imageUpload = document.getElementById('imageUpload');
    const uploadedImageDiv = document.getElementById('uploadedImage');
    const responseText = document.getElementById('responseText');

    if (imageUpload.files.length === 0) {
        alert("Please upload an image.");
        return;
    }

    const formData = new FormData();
    formData.append('inputPrompt', inputPrompt);
    formData.append('imageUpload', imageUpload.files[0]);

    fetch('/explain_invoice', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            responseText.textContent = data.response;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('An error occurred while processing the request.');
    });
});