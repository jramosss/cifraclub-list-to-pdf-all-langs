# Elixir

## How to use

`mix benchmark`

## Conclusions

- I like the pipe system, is like using bash
- Dreadful traceback for errors, like what's the error here??

  ```elixir
    (ArgumentError) argument error
      :erlang.apply(Scraper, :scrape)
      (stdlib 7.0.3) timer.erl:633: :timer.tc/3
      benchmark.exs:9: anonymous fn/1 in :elixir_compiler_3.__FILE__/1
      (elixir 1.18.4) lib/enum.ex:1714: Enum."-map/2-lists^map/1-1-"/2
      benchmark.exs:7: (file)
      nofile:1: (file)
  ```
