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