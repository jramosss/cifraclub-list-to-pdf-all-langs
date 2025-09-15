# Elixir + HTTPoison + Floki + ChromicPDF

## How to use

`mix benchmark`

## Conclusions

A functional language but somehow super super flexible, i feel like there is a pronounced learning curve, super fast but i wouldn't recommend it for production, only for making some beautiful code and frame it.

- Pretty easy to setup
- I like the pipe system, is like using bash
- Builtin JSON parser, Java watch and learn
- I don't like non expicit return types, what good does it make?
- Type system is midway, is like using jsdoc but types are not so useful
- Compiler shows the values of the variables used in the function call, that's great
- Still not sure how to import stuff from other files, really complicated
- So fast omg
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

- Looks like a really good language, seems like there is lot to it that i could not discover with a small project. Anyhow i don't think i could ever use it in production.
