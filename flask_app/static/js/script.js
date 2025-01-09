console.log("connected")
document.addEventListener("scroll", function () {
    const strip = document.querySelector(".strip");
    if (window.scrollY > 100) {
        strip.classList.add("scroll-triggered");
    } else {
        strip.classList.remove("scroll-triggered");
    }
});

