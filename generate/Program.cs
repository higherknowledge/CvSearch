using System;
using System.Diagnostics;
using System.IO;

namespace generate
{
    class Program
    {
        static void Main(string[] args)
        {
            if(!Directory.Exists("./Output"))
            {
                Directory.CreateDirectory("Output");
            }
            
            foreach(var file in Directory.EnumerateFiles("./CVs"))
            {
                var parts = file.Split('\\');
                Console.WriteLine("Filename : " + file + " parts : " + parts[0]);
                string outputPath = "./Output/" + parts[1].Split('.')[0] + ".json";
                Console.WriteLine("Output path is : " + outputPath);
                string fullPath = Path.GetFullPath(file);
                ProcessStartInfo info;
                if(Path.GetExtension(file) == ".docx")
                {
                    info  = new ProcessStartInfo("python", "../docx2json.py " + fullPath + " " + outputPath);
                    Process python = new Process();
                    python.StartInfo = info;
                    python.Start();
                    python.WaitForExit();
                }

                else if(Path.GetExtension(file) == ".pdf")
                {
                    info = new ProcessStartInfo("python", "../pdf2txt.py -t xml -o output.xml " + fullPath);
                    Process python = new Process();
                    python.StartInfo = info;
                    python.Start();
                    python.WaitForExit();
                    info = new ProcessStartInfo("python", "../xmlParser.py " + outputPath);
                    python = new Process();
                    python.StartInfo = info;
                    python.Start();
                    python.WaitForExit();
                }
            }
            Console.WriteLine("Done extracting");
        }
    }
}
