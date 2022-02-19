using System.Diagnostics;
class MakeOtoTemp
{
	static void Main(string[] args)
	{
		String python = ".\\python-3.9.10\\python.exe";
		String endpoint = ".\\src\\MakeOtoTemp.py";
		Process p = Process.Start(python, endpoint +" " + String.Join(" ", args));
		p.WaitForExit();
	}
}