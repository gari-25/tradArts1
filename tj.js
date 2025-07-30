const track = document.getElementById('sliderTrack');
const cards = document.querySelectorAll('.event-card');
const cardHeight = cards[0].offsetHeight + 5; // height + margin
const visibleCount = 3;
let currentIndex = 0;

function slideUp() {
  currentIndex++;
  if (currentIndex > cards.length - visibleCount) {
    currentIndex = 0;
  }
  const translateY = -(currentIndex * cardHeight);
  track.style.transform = `translateY(${translateY}px)`;
}

window.addEventListener('load', () => {
  setInterval(slideUp, 3000);
});
