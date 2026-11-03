import { scrapeAndGenerate } from "./src/services";
import * as fs from "fs";

function parseAsJson(obj: object) {
  return JSON.stringify(obj, null, 2);
}

export default async function benchmark() {
  const resultLarge = await scrapeAndGenerate("large", "https://www.cifraclub.com/musico/551928421/repertorio/favoritas/");

  fs.writeFileSync("benchmarks.json", parseAsJson([
    resultLarge
  ]));
}

benchmark().then(() => console.log(""));