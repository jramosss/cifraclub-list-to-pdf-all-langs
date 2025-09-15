defmodule Elixirlang.MixProject do
  use Mix.Project

  def project do
    [
      app: :elixirlang,
      version: "0.1.0",
      elixir: "~> 1.15",
      start_permanent: Mix.env() == :prod,
      deps: deps(),
      aliases: aliases()
    ]
  end

  defp aliases do
    [
      benchmark: "run -e \"Code.require_file(\\\"lib/pdf.exs\\\"); Code.require_file(\\\"lib/utils.exs\\\"); Code.require_file(\\\"lib/scraper.exs\\\"); Code.require_file(\\\"benchmark.exs\\\")\""
    ]
  end

  # Run "mix help compile.app" to learn about applications.
  def application do
    [
      extra_applications: [:logger],
      mod: {Elixirlang.Application, []}
    ]
  end

  # Run "mix help deps" to learn about dependencies.
  defp deps do
    [
      # {:dep_from_hexpm, "~> 0.3.0"},
      # {:dep_from_git, git: "https://github.com/elixir-lang/my_dep.git", tag: "0.1.0"}
      {:httpoison, "~> 2.0"},
      {:floki, "~> 0.38.0"},
      {:chromic_pdf, "~> 1.17"}
    ]
  end
end
