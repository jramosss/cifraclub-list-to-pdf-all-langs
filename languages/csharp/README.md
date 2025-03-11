# Cifraclub to PDF - Csharp - HAP + Playwright

## How to run
No clueeee, this language is great but everything around it is super complicated.
Just run the dockerfile or run `run_benchmark.sh`.

## Conclusions:
- GREAT LANGUAGE, i mean, all the other languages are so complicated to achieve concurrency and parallelism, but C# is just so easy to do that.
- Really, all i (GPT) had to do to achieve the parallelism was this
    ```csharp
    public string[] ScrapePages(string[] urls)
    {
        // f*ing love this language
        return urls.AsParallel()
               .Select(ScrapePage)
               .ToArray();
    }
    ```
- Tools kinda rusty, just look at the [HAP docs](https://html--agility--pack-net.translate.goog/?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=tc)
- HAP has no (easy or reliable) way to find an element via selector, only "hacks", so i had to use xPATH, which was not reliable at all.
- Just look at how many files i needed for this simple project.
- Somehow with more songs it goes faster???? It defies logic and makes me question if i did it right, but i think i did it right, super curious