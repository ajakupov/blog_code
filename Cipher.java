import java.util.Scanner;

public class Cipher {
	private static String message;
	private static String option = "";
	
	public static String encode(String message, int k) {
		String encodedMessage = "";
		for (char e:message.toCharArray()) {
			if (e+k > 122) {
				e = (char) ('A' + (e+k-123));
			} else {
				e+=k;
			}
			encodedMessage+=e;
		}
		return encodedMessage;
	}
	
	public static String decode(String message, int k) {
		String decodedMessage = "";
		for (char e:message.toCharArray()) {
			if (e-k<65) {
				int a = e-k;
				int b = 65-a;
				e = (char) ('z' - b+1);
			}else {
				e-=k;
			}
			decodedMessage+=e;
		}
		return decodedMessage;
	}
	
	public static void main (String[] args) {
		int k = 0;
		System.out.println("Enter your message");		
		Scanner input = new Scanner(System.in);
		message = input.nextLine();
		System.out.println("Enter k:");
		System.out.println("Decode or encode?");
		k = input.nextInt();
		
		option = input.nextLine();
		
		if (option.trim().toLowerCase().equals("encode")) {
			System.out.println(encode(message, k));
		} else if (option.trim().toLowerCase().equals
				("decode")) {
			System.out.println(decode(message, k));
		} else {
			System.out.println("Unknown command");
		}
	}
}
