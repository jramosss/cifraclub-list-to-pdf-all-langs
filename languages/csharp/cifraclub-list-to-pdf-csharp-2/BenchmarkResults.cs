namespace cifraclub_list_to_pdf_csharp;

public interface IBenchmarkResults
{
    int scrape_time { get; set; }
    int pdf_generate_time { get; set; }
    int total_songs { get; set; }
}

public class BenchmarkResults : IBenchmarkResults
{
    public int scrape_time { get; set; }
    public int pdf_generate_time { get; set; }
    public int total_songs { get; set; }
}