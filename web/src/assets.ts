const BASE = import.meta.env.BASE_URL;

export function media(path: string): string {
  return BASE + path.split("/").map(encodeURIComponent).join("/");
}

export function imageFile(name: string): string {
  return media("images/" + name);
}

export function audioFile(name: string): string {
  return media("audio/" + name);
}

export const NPC_SPRITE: Record<string, string> = {
  chief: "npc chief.png",
  doctor: "npc doctor.png",
  nurse: "npc nurse.png",
  agent: "npc agent.png",
  netbar: "npc netbar.png",
  xiebufeng: "npc xiebufeng.png",
  teller: "npc teller.png",
  wife: "npc chief.png",
};

export const SPEAKER_NAME: Record<string, string> = {
  me: "俺",
  news: "北京晚报",
  chief: "村长",
  doctor: "大夫",
  nurse: "小护士",
  wife: "村长老婆",
  agent: "中介",
  netbar: "网管",
  xiebufeng: "谢不疯",
  teller: "柜员",
  stallkeep: "摊主",
};
