document.addEventListener('DOMContentLoaded', function() {

    const searchBtn = document.getElementById('search-icon');
    const searchBtnmob = document.getElementById('search-icon-mob');
    const searchContainer = document.getElementById('search-container');
    const explr = document.getElementById('explr-or-comnty');

    searchBtn.addEventListener( 'click' , () =>{
        searchContainer.classList.toggle( "active" );
        explr.classList.toggle( "active" );
    });
    searchBtnmob.addEventListener( 'click' , () =>{
        searchContainer.classList.toggle( "active" );
        explr.classList.toggle( "active" );
    });
});