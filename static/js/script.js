
document.getElementById("patternForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const formData = new FormData(this);

  fetch("/generate", {
    method: "POST",
    body: formData
  })
    .then(response => response.json())
    .then(data => {
      if (data.status === "success") {
        const img = document.getElementById("patternImage");
        img.src = data.image_url + "?t=" + new Date().getTime(); // prevent caching
        img.style.display = "block";
      } else {
        alert("Error: " + data.message);
      }
    })
    .catch(err => {
      alert("Something went wrong!");
      console.error(err);
    });
});
