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

document.querySelectorAll("table").forEach((table) => {
  const headers = Array.from(table.querySelectorAll("thead th")).map((header) => header.textContent.trim());
  table.querySelectorAll("tbody tr").forEach((row) => {
    row.querySelectorAll("td").forEach((cell, index) => {
      if (!cell.dataset.label) {
        cell.dataset.label = headers[index] || "";
      }
    });
  });
});
