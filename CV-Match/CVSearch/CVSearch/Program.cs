using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using iTextSharp.text.pdf;
using iTextSharp.text.pdf.parser;
using Newtonsoft.Json;
using Spire.Doc;
using Spire.Doc.Documents;
using static SautinSoft.UseOffice;

namespace CVSearch
{
    class Program
    {
        static void Main(string[] args)
        {     
            string[] files = Directory.GetFiles("C:/Users/t-abv/Documents/HK/Match");
            string result;

            foreach(var x in files)
            {
                Console.WriteLine(x);
                if (x.Contains(".pdf"))
                {
                    result = getTextFromPdf(x);
                    SautinSoft.PdfFocus focus = new SautinSoft.PdfFocus();
                    focus.OpenPdf(x);
                    focus.ToHtml(x.Substring(0, x.Length - 5) + ".html");
                }

                else
                {
                    result = getTextFromDoc(x);
                    SautinSoft.RtfToHtml focus = new SautinSoft.RtfToHtml();

                    try
                    {
                        focus.OpenDocx(x);
                        focus.ToHtml(x.Substring(0, x.Length - 5) + "xx.html");
                    }
                    catch
                    {
                        try
                        {
                            SautinSoft.UseOffice office = new SautinSoft.UseOffice();
                            office.ConvertFile(x, x.Substring(0, x.Length - 5) + ".html", eDirection.DOC_to_HTML);
                        }

                        catch
                        {
                            Console.WriteLine("ERROR" + x);
                        }
                    }
                      
                }

                Result temp = new Result();
                temp.FileName = x;
                temp.Contents = result;
                string json = JsonConvert.SerializeObject(temp, Formatting.Indented);
                Console.WriteLine(json);
            }
            Console.ReadLine();
        }

        private static string getTextFromPdf(string path)
        {
            StringBuilder text = new StringBuilder();
            if (File.Exists(path))
            {
                PdfReader pdfReader = new PdfReader(path);
                for (int page = 1; page <= pdfReader.NumberOfPages; page++)
                {
                    string currentText = PdfTextExtractor.GetTextFromPage(pdfReader, page);
                    text.Append(currentText);
                }

                pdfReader.Close();
            }
            return text.ToString();
        }

        private static string getTextFromDoc(string path)
        {
                Document doc = new Document(path);
                StringBuilder temp = new StringBuilder();
                foreach (Section s in doc.Sections)
                {
                    foreach (Paragraph p in s.Paragraphs)               
                    {
                        temp.Append(p.Text);
                    }
                }
                return temp.ToString();
        }

        class Result
        {
            public string FileName { get; set; }
            public string Contents { get; set; }
        }
    }
}
