import { scrapeAndGenerate } from "./src/services";

function parseAsJson(obj: object) {
  return JSON.stringify(obj, null, 2);
}

export default async function benchmark() {
  const resultTiny = await scrapeAndGenerate("tiny", "https://www.cifraclub.com/musico/551928421/repertorio/12409416/");
  console.log(parseAsJson(resultTiny));

  const resultLarge = await scrapeAndGenerate("large", "https://www.cifraclub.com/musico/551928421/repertorio/favoritas/");
  console.log(resultLarge);
}

benchmark().then(() => console.log(""));