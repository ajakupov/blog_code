import java.util.Scanner;


public class Vigenere {
	public static String encode (String input, String keyword) {
		char temp;
		String encryptedText = "";
		
		for (int i = 0, j =0; i<input.length(); i++) {
			temp = (char) ('A' + (input.charAt(i)+keyword.charAt(j))%26);
			System.out.println(input.charAt(i) + " + " + keyword.charAt(j) + " = " + temp);
			j = ++j % keyword.length();
			encryptedText += temp;
		}
		
		return encryptedText;
	}
	
	public static String decode (String input, String keyword) {
		char temp;
		String encryptedText = "";
		
		for (int i = 0, j =0; i<input.length(); i++) {
			temp = (char) ('A' + (input.charAt(i)- keyword.charAt(j) + 26)%26);
			System.out.println(input.charAt(i) + " + " + keyword.charAt(j) + " = " + temp);
			j = ++j % keyword.length();
			encryptedText += temp;
		}
		
		return encryptedText;
	}
	
	public static void main (String[] args) {
		System.out.println("Enter your sequence");
		String input = "";
		String keyword = "";
		String option ="";
		
		Scanner scanner = new Scanner (System.in);
		input = scanner.nextLine();
		input = input.trim();
		System.out.println("Enter your keyword");
		keyword =scanner.nextLine();
		keyword = keyword.trim();
		System.out.println("Enter Option");
		option = scanner.nextLine();
		
		if (option.trim().toLowerCase().equals("encode")) {
			System.out.println(encode(input, keyword));
		} else if (option.trim().toLowerCase().equals("decode")) {
			System.out.println(decode(input, keyword));
		} else {
			System.out.println("Unknown Option");
		}
		
	}
}
