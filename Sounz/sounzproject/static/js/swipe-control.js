document.addEventListener('DOMContentLoaded', function() {
    const mediaContainer = document.getElementById('media');
const swipeTip = document.getElementById('swipeTip');
let startX, endX;
let threshold = 100; // Minimum distance required for a swipe

// Read from data attributes - VS Code won't show errors for this
let hasPrevious = mediaContainer.dataset.hasPrevious === 'true';
let hasNext = mediaContainer.dataset.hasNext === 'true';
let prevUrl = mediaContainer.dataset.prevUrl;
let nextUrl = mediaContainer.dataset.nextUrl;

// Touch start event
mediaContainer.addEventListener('touchstart', function(e) {
startX = e.changedTouches[0].screenX;
}, { passive: true });

// Touch end event
mediaContainer.addEventListener('touchend', function(e) {
endX = e.changedTouches[0].screenX;
handleSwipe();
}, { passive: true });

function handleSwipe() {
const distance = endX - startX;

// If swiped left and there's a next post
if (distance < -threshold && hasNext) {
    window.location.href = nextUrl;
}
// If swiped right and there's a previous post
else if (distance > threshold && hasPrevious) {
    window.location.href = prevUrl;
}
// If swipe wasn't strong enough, show the tip
else if (Math.abs(distance) > 20 && Math.abs(distance) < threshold) {
    showSwipeTip();
}
}

function showSwipeTip() {
swipeTip.classList.add('visible');
setTimeout(() => {
    swipeTip.classList.remove('visible');
}, 2000); // Tip disappears after 2 seconds
}
});