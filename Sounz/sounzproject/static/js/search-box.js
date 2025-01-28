document.addEventListener("DOMContentLoaded", () => {
    const placeholders = [
        "Search for music...",
        "Find your favorite composers...",
        "Explore new collaborations...",
        "Discover inspiration..."
    ];

    const searchInput = document.getElementById("search-input-field");
    let currentIndex = 0;

    function updatePlaceholder() {
        if (!searchInput) return; // Prevent errors if input is not found

        // Fade out the current placeholder
        searchInput.classList.add("placeholder-fade-out");

        setTimeout(() => {
            // Update the placeholder text
            currentIndex = (currentIndex + 1) % placeholders.length;
            searchInput.placeholder = placeholders[currentIndex];

            // Fade in the new placeholder
            searchInput.classList.remove("placeholder-fade-out");
            searchInput.classList.add("placeholder-fade-in");

            // Remove the fade-in class after the animation
            setTimeout(() => {
                searchInput.classList.remove("placeholder-fade-in");
            }, 500);
        }, 500);
    }

    // Change the placeholder every 3 seconds
    setInterval(updatePlaceholder, 3000);
});