document.addEventListener('DOMContentLoaded', function() {
    const rightSection = document.querySelector('.suggestions');
    const container = document.querySelector('.main-explore');

    window.addEventListener('scroll', function() {
        const rightSectionBottom = rightSection.getBoundingClientRect().bottom;
        const containerBottom = container.getBoundingClientRect().bottom;

        if (rightSectionBottom <= window.innerHeight) {
            rightSection.classList.add('fixed');
        } else {
            rightSection.classList.remove('fixed');
        }
    });
});
