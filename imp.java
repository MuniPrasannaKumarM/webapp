
class check_book{
	int a;
	int b;	
}
final class check_book1 extends check_book{
	check_book s = new check_book();

}
public class imp{
	
	public static void main(String args[])
	{
		check_book s1 = new check_book();
	}
}