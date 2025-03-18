function toggleLike(postId) {
    const likeImage = document.getElementById(`likeImage-${postId}`);
    const likeCount = document.getElementById(`likeCount-${postId}`);
    const isLiked = likeImage.getAttribute("data-liked") === "true";

    // Update the image source and data-liked attribute
    if (isLiked) {
        likeImage.setAttribute("src", "{% static 'images/Like-black.svg' %}");
        likeImage.setAttribute("data-liked", "false");
        likeCount.textContent = parseInt(likeCount.textContent) - 1;
    } else {
        likeImage.setAttribute("src", "{% static 'images/onclick.svg' %}");
        likeImage.setAttribute("data-liked", "true");
        likeCount.textContent = parseInt(likeCount.textContent) + 1;
    }

    // Add animation class
    likeImage.classList.add("liked");

    // Remove animation class after animation ends
    likeImage.addEventListener("animationend", () => {
        likeImage.classList.remove("liked");
    }, { once: true });
}
let touchStartX = 0;
let touchEndX = 0;

// Select the post container
const postContainer = document.querySelector(".master-div"); // Adjust based on your structure

if (postContainer) {
    postContainer.addEventListener("touchstart", function (event) {
        touchStartX = event.touches[0].clientX;
    });

    postContainer.addEventListener("touchend", function (event) {
        touchEndX = event.changedTouches[0].clientX;
        handleSwipe();
    });
}

function handleSwipe() {
    const swipeThreshold = 50; // Minimum distance for swipe detection

    if (touchStartX - touchEndX > swipeThreshold) {
        console.log("Swiped Left - Next Post");

    } else if (touchEndX - touchStartX > swipeThreshold) {
        console.log("Swiped Right - Previous Post");

    }
}