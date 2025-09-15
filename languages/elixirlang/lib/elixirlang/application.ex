defmodule Elixirlang.Application do
  @moduledoc false

  use Application

  # no idea what this is
  @impl true
  def start(_type, _args) do
    children = [
      # Start ChromicPDF
      {ChromicPDF, chromic_pdf_opts()}
    ]

    opts = [strategy: :one_for_one, name: Elixirlang.Supervisor]
    Supervisor.start_link(children, opts)
  end

  defp chromic_pdf_opts do
    [no_sandbox: true, discard_stderr: false, disabled_scripts: true]
  end
end
