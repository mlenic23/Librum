document.addEventListener("DOMContentLoaded", () => {
    const hearts = document.querySelectorAll(".heart");
  
    hearts.forEach((heart) => {
      heart.addEventListener("click", () => {
        const liked = heart.classList.toggle("filled");
        heart.innerHTML = liked ? "&#9825;" : "&#9825;";
      });
    });
  });
  