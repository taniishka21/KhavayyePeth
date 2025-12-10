// scripts.js

// Bootstrap carousel auto-slide interval
var myCarousel = document.querySelector('#staybiteCarousel');
if (myCarousel) {
  var carousel = new bootstrap.Carousel(myCarousel, {
    interval: 5000,
    ride: 'carousel'
  });
}

// Smooth scroll for in-page links
document.addEventListener("DOMContentLoaded", function () {
  const links = document.querySelectorAll('a[href^="#"]');
  for (let link of links) {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute("href"));
      if (target) {
        target.scrollIntoView({ behavior: "smooth" });
      }
    });
  }
});
