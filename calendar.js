const monthYearEl = document.getElementById('monthYear');
const calendarDatesEl = document.getElementById('calendarDates');
const prevBtn = document.getElementById('prev');
const nextBtn = document.getElementById('next');

let currentDate = new Date();

// Define active event days (can add links here too)
const eventsData = {
  "2025-06-07": "candle.html?date=2025-07-07",
  "2025-07-04": "rangoli.html?date=2025-07-07",
  "2025-07-15": "new.html?date=2025-07-07",
  "2025-08-07": "madhubani.html?date=2025-07-07",
  "2025-08-18": "vastra.html?date=2025-07-18",
  "2025-08-24": "clay.html?date=2025-07-24",
  "2025-09-08": "string.html?date=2025-07-07",
  "2025-09-15": "warli.html?date=2025-07-07",
  "2025-10-08": "fabric.html?date=2025-07-07",
};

function renderCalendar(date) {
  const year = date.getFullYear();
  const month = date.getMonth();

  // Set month-year header
  const monthNames = ["January", "February", "March", "April", "May", "June",
                      "July", "August", "September", "October", "November", "December"];
  monthYearEl.textContent = `${monthNames[month]} ${year}`;

  // First day of the month
  const firstDay = new Date(year, month, 1).getDay();

  // Number of days in month
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  calendarDatesEl.innerHTML = "";

  // Fill empty blocks before start
  for (let i = 0; i < firstDay; i++) {
    const emptyDiv = document.createElement("div");
    emptyDiv.classList.add("inactive");
    calendarDatesEl.appendChild(emptyDiv);
  }

  // Fill days
  for (let day = 1; day <= daysInMonth; day++) {
    const dateKey = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
    const dayDiv = document.createElement("div");
    dayDiv.textContent = day;

    if (eventsData[dateKey]) {
      dayDiv.classList.add("active");
      dayDiv.style.cursor = "pointer";
      dayDiv.addEventListener("click", () => {
        window.location.href = eventsData[dateKey];
      });
    }

    calendarDatesEl.appendChild(dayDiv);
  }
}

// Navigation
prevBtn.addEventListener("click", () => {
  currentDate.setMonth(currentDate.getMonth() - 1);
  renderCalendar(currentDate);
});

nextBtn.addEventListener("click", () => {
  currentDate.setMonth(currentDate.getMonth() + 1);
  renderCalendar(currentDate);
});

renderCalendar(currentDate);




const eventList = document.getElementById("verticalEvents");
  const eventItems = eventList.children;
  const itemHeight = eventItems[0].offsetHeight + 8;
  const totalItems = eventItems.length;
  const visibleCount = 3;
  let index = 0;
  let scrollInterval;

  function verticalAutoScroll() {
    index++;
    if (index > totalItems - visibleCount) {
      index = 0;
    }
    eventList.style.transform = `translateY(-${index * itemHeight}px)`;
  }

  function startScroll() {
    scrollInterval = setInterval(verticalAutoScroll, 2800);
  }

  function stopScroll() {
    clearInterval(scrollInterval);
  }

  // Start auto-scroll
  startScroll();

  // 🛑 Stop when any "Details" button or event item is clicked
  document.querySelectorAll(".event-item a, .event-item button").forEach(el => {
    el.addEventListener("click", () => {
      stopScroll();

      // Optional: restart scroll after 10 sec
      setTimeout(() => {
        startScroll();
      }, 0); //
    });
  });


    