console.log("connected")
document.addEventListener("scroll", function () {
    const strip = document.querySelector(".strip");
    if (window.scrollY > 100) {
        strip.classList.add("scroll-triggered");
    } else {
        strip.classList.remove("scroll-triggered");
    }
});

function confirmDelete(eventId,eventTitle) {
    // Show a confirmation dialog
    var result = confirm("Are you sure you want to delete " + eventTitle + "?");
    if (result) {
        // Redirect to the delete route if confirmed
        window.location.href = "/delete_event/" + eventId;
    }
}