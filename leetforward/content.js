// Very simple functionality for adding a banner to webpages

// Function to create and add the banner
function addBanner() {
  // Create a new div element for our banner
  const banner = document.createElement('div');

  // Add the 'chrome-extension-banner' class to apply the CSS styling we'll use
  banner.className = 'chrome-extension-banner';

  // Set the text content
  banner.textContent = 'This page was modified by a Chrome extension!';

  // Insert the banner at the top of the HTML body
  document.body.insertBefore(banner, document.body.firstChild);
}

// Run our function when the page loads
window.addEventListener('load', addBanner);