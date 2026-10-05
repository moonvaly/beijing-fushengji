import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../..");
const game = path.join(root, "beijing_fushengji", "game");
const dest = path.join(root, "web", "public");

function copyDir(from, to) {
  fs.mkdirSync(to, { recursive: true });
  for (const name of fs.readdirSync(from)) {
    const src = path.join(from, name);
    const out = path.join(to, name);
    if (fs.statSync(src).isDirectory()) copyDir(src, out);
    else fs.copyFileSync(src, out);
  }
}

fs.mkdirSync(dest, { recursive: true });
copyDir(path.join(game, "images"), path.join(dest, "images"));
copyDir(path.join(game, "audio"), path.join(dest, "audio"));
fs.copyFileSync(path.join(game, "engine", "events.json"), path.join(dest, "events.json"));
fs.copyFileSync(
  path.join(game, "SourceHanSansLite.ttf"),
  path.join(dest, "SourceHanSansLite.ttf"),
);
const menu = path.join(game, "gui", "main_menu.png");
if (fs.existsSync(menu)) fs.copyFileSync(menu, path.join(dest, "main_menu.png"));
console.log("synced assets -> web/public");
