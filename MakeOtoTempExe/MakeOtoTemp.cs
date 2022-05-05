using System.Diagnostics;
class MakeOtoTemp
{
	static void Main(string[] args)
	{
		string exePath = System.Reflection.Assembly.GetEntryAssembly().Location;
		String python = Path.Combine(Path.GetDirectoryName(exePath), "python-3.9.10", "python.exe");
		String endpoint = Path.Combine(Path.GetDirectoryName(exePath), "src", "MakeOtoTemp.py");
		Process p = Process.Start(python, endpoint +" " + String.Join(" ", args));
		p.WaitForExit();
	}
}