let humburger=document.querySelector(".burger")
let xmarq=document.querySelector(".xmark")
let nav_phone=document.querySelector(".phonenav")
let countainer=document.querySelector(".container")
humburger.addEventListener('click', function() {
    // Your code to handle the click event here
    nav_phone.classList.add("active")
    countainer.classList.add("blur")


});

// Add an event listener for the click event on the xmark icon
xmarq.addEventListener('click', function() {
    // Your code to handle the click event here
    console.log('Xmark clicked');
    nav_phone.classList.remove("active")
    countainer.classList.remove("blur")

});