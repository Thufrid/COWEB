// /static/js/scripts.js

/**
 * Handles the logic for a tabbed interface.
 * Shows the selected tab's content and hides all other content.
 * * @param {Event} evt - The click event object.
 * @param {string} tabName - The ID of the tab content to display.
 */
function openTab(evt, tabName) {
    // Get all elements with class="tab-content" and hide them
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => {
        content.style.display = 'none';
        content.classList.remove('active');
    });

    // Get all elements with class="tab-button" and remove the "active" class
    const tabButtons = document.querySelectorAll('.tab-button');
    tabButtons.forEach(button => {
        button.classList.remove('active');
    });

    // Show the current tab's content and add an "active" class to the button
    document.getElementById(tabName).style.display = 'block';
    document.getElementById(tabName).classList.add('active');
    evt.currentTarget.classList.add('active');
}

// Ensure the first tab is open on page load
document.addEventListener('DOMContentLoaded', () => {
    // Check if a tab button and content exist before clicking
    const firstTabButton = document.querySelector('.tab-button');
    const firstTabContent = document.querySelector('.tab-content');

    if (firstTabButton && firstTabContent) {
        firstTabButton.click();
    }
});