const imageInput = document.getElementById('imageInput');
const preview = document.getElementById('preview');
const resultText = document.getElementById('resultText');

// Image Preview
imageInput.addEventListener('change', () => {
  const file = imageInput.files[0];
  if (file) {
    const reader = new FileReader();

    reader.onload = function(e) {
      preview.src = e.target.result;
      preview.style.display = 'block';
    };

    reader.readAsDataURL(file);
  } else {
    preview.src = '#';
    preview.style.display = 'none';
    resultText.innerText = '';
  }
});





function uploadImage() {
  const file = imageInput.files[0];

  if (!file) {
    alert('Please select an image.');
    return;
  }

  const formData = new FormData();
  formData.append('file', file);

  fetch('/predict', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    if (data.error) {
      resultText.innerText = 'Error: ' + data.error;
    } else {
      resultText.innerText =
        `Predicted Pokémon: ${data.name}\n` +
        `Confidence: ${(data.probability * 100).toFixed(2)}%`;
    }
  })
  .catch(err => {
    resultText.innerText = 'Error: ' + err;
  });
}

