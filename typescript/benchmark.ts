import { scrapeAndGenerate } from "./src/services";

export default async function benchmark() {
  const resultTiny = await scrapeAndGenerate("tiny", "https://www.cifraclub.com/musico/551928421/repertorio/12409416/");
  const resultLarge = await scrapeAndGenerate("large", "https://www.cifraclub.com/musico/551928421/repertorio/favoritas/");

  console.log("Tiny: ", resultTiny);
  console.log("Large: ", resultLarge);
}

benchmark().then(() => console.log(""));