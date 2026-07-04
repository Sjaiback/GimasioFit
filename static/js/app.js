document.querySelectorAll("[data-confirm]").forEach((button) => {
  button.addEventListener("click", (event) => {
    if (!window.confirm(button.dataset.confirm)) {
      event.preventDefault();
    }
  });
});

document.querySelectorAll(".stat").forEach((card, index) => {
  card.style.animationDelay = `${index * 70}ms`;
});
