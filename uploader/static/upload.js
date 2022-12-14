$chooserProxy = document.getElementById('chooserProxy');
$chooser = document.getElementById('chooser');
$chooserSubmit = document.getElementById('chooserSubmit');
$chooserSpinner = document.getElementById('chooserSpinner');

// Show directory picker when proxy is clicked
$chooserProxy.addEventListener("click", function() {
  $chooser.click();
});

// Hide directory picker, etc., and show spinner when starting upload
$chooserSubmit.addEventListener("click", function() {
  $chooserProxy.style.display = "none";
  $chooserSubmit.style.display = "none";
  $chooserSpinner.classList.remove("invisible");
});
