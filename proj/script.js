document.getElementById('fileInput').addEventListener('change', function (event) {
          const file = event.target.files[0];
          if (file) {
            alert(`Uploaded: ${file.name}`);
          }
        });
