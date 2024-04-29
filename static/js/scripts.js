let humburger=document.querySelector(".burger")
let xmarq=document.querySelector(".xmark")
let nav_phone=document.querySelector(".phonenav")
let container=document.querySelector(".container")
// Function to handle hamburger click event
function handleHamburgerClick() {
    nav_phone.classList.add("active");
    container.classList.add("blur");
}

// Function to handle xmark click event
function handleXmarkClick() {
    console.log('Xmark clicked');
    nav_phone.classList.remove("active");
    container.classList.remove("blur");
}

// Event listener for hamburger click
humburger.addEventListener('click', handleHamburgerClick);

// Event listener for xmark click
xmarq.addEventListener('click', handleXmarkClick);

// Event listener for window resize
window.addEventListener('resize', function() {
    // Remove active class if window is resized
    nav_phone.classList.remove("active");
    container.classList.remove("blur");
});
