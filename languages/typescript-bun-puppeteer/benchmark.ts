import { scrapeAndGenerate } from "./src/services";
import fs from "fs";

function parseAsJson(obj: object) {
  return JSON.stringify(obj, null, 2);
}

export default async function benchmark() {
  const resultTiny = await scrapeAndGenerate("tiny", "https://www.cifraclub.com/musico/551928421/repertorio/12409416/");
  const resultLarge = await scrapeAndGenerate("large", "https://www.cifraclub.com/musico/551928421/repertorio/favoritas/");

  fs.writeFileSync("benchmarks.json", parseAsJson([
    resultTiny,
    resultLarge
  ]));
}

benchmark().then(() => console.log(""));