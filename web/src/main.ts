import "./styles.css";
import { Game } from "./game";

const game = new Game();
void game.start();

document.addEventListener("keydown", (e) => {
  if (e.key === " " || e.key === "Enter") {
    const d = document.getElementById("dialogue");
    if (d && !d.hidden) {
      e.preventDefault();
      d.click();
    }
  }
});
