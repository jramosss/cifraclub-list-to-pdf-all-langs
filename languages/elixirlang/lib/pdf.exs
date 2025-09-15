defmodule Pdf do
  @spec generate(String.t(), String.t()) :: {:ok, binary()} | {:error, any()}
  def generate(html, output) do
    ChromicPDF.print_to_pdf({:html, html}, output: output, discard_stderr: false)
  end
end
