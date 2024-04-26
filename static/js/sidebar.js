
let open_sidebar=document.querySelector(".open")
let close_sidebar=document.querySelector(".close")
let sidebar=document.querySelector(".sidebar")

open_sidebar.addEventListener('click', function() {
    // Your code to handle the click event here
console.log('kdok');
    sidebar.classList.remove("closed")
    


});

// Add an event listener for the click event on the xmark icon
close_sidebar.addEventListener('click', function() {

    sidebar.classList.add("closed")

});