const $chooserProxy = document.getElementById("chooserProxy");
const $chooser = document.getElementById("chooser");
const $chooserSubmit = document.getElementById("chooserSubmit");
const $chooserSpinner = document.getElementById("chooserSpinner");
const $chooserFeedback = document.getElementById("chooserFeedback");

// Show directory picker when proxy is clicked
$chooserProxy.addEventListener("click", function() {
  $chooser.click();
});

// Show number of file after directory is selected
$chooser.addEventListener("change", function() {
  const message = ($chooser.files.length) + " files selected";
  $chooserFeedback.textContent = message;
  $chooserSubmit.removeAttribute("disabled");
  $chooserSubmit.classList.remove("opacity-25");
});

// Hide directory picker, etc., and show spinner when starting upload
$chooserSubmit.addEventListener("click", function() {
  $chooserProxy.style.display = "none";
  $chooserSubmit.style.display = "none";
  $chooserFeedback.style.display = "none";
  $chooserSpinner.classList.remove("invisible");
});
