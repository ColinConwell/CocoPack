// Custom JavaScript for Coco-Pack documentation

const hideEmptySearchContainers = false

// Function to hide empty search containers
function hideEmptySearchContainers() {
  // Hide empty search containers
  $('.bd-search').each(function() {
    if ($(this).children().length === 0 || 
        ($(this).children().length === 1 && $(this).children().first().html() === '')) {
      $(this).hide();
    }
  });
  
  // Hide empty search button wrappers
  $('.search-button__wrapper').each(function() {
    if ($(this).children().length === 0 || 
        ($(this).children().length === 1 && $(this).children().first().html() === '')) {
      $(this).hide();
    }
  });
}



$(document).ready(function() {
  // Set the document title
  document.title = 'Coco-Pack Docs ' + $('.version').text().trim();
  if (hideEmptySearchContainers) {
    // Run immediately
    hideEmptySearchContainers();
    // Run after a short delay to catch dynamically loaded elements
    setTimeout(hideEmptySearchContainers, 500);
  }
});