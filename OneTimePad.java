import java.util.Random;
import java.util.Scanner;

import sun.net.www.content.text.plain;


public class OneTimePad {
	private static String plainText = "";
	private static String key = "";
	private static String encryptedMessage = "";
	private static int messageSize;
	private static Scanner scanner;
	private static String option;
	
	public static String encrypt (String plainText, String key) {
		String encryptedMessage = "";
		char letter;
		int index;
		
		for (int i =0 ; i < plainText.length(); i++) {
			index = plainText.toCharArray()[i] + key.toCharArray()[i];
			
			if (index <26) {
				index= index;
			} else {
				index = index%26;
			}
			letter = (char) ('A' + index);
			System.out.println(
					plainText.toCharArray()[i] + 
					" + " + key.toCharArray()[i] + 
					" = " + index + " ~ " + 
					letter); 
			encryptedMessage += letter;
		}
		
		return encryptedMessage;
	}
	
	public static String decrypt (String plainText, String key) {
		String decryptedMessage = "";
		char letter;
		int index;
		
		for (int i =0 ; i < plainText.length(); i++) {
			index = plainText.toCharArray()[i] - key.toCharArray()[i];
			
			if (index > 0) {
				index = index;
			} else {
				index +=26;
			}
			if (index == 26) {
				index = 0;
			}
			letter = (char) ('A' + index);
			System.out.println(
					plainText.toCharArray()[i] + 
					" - " + key.toCharArray()[i] + 
					" = " + index + " ~ " + 
					letter); 
			decryptedMessage += letter;
		}
		
		return decryptedMessage;
	}
	
	public static void main (String[] args) {
		System.out.println("Welcome");
		
		scanner = new Scanner (System.in);
		Random random = new Random();
		
		System.out.println("Enter your message:");
		
		plainText = scanner.nextLine();
		plainText = plainText.replaceAll("\\s","").trim().toUpperCase();
		plainText = plainText.replace("1", "ONE");
		plainText = plainText.replace("2", "TWO");
		plainText = plainText.replace("3", "THREE");
		plainText = plainText.replace("4", "FOUR");
		plainText = plainText.replace("5", "FIVE");
		plainText = plainText.replace("6", "SIX");
		plainText = plainText.replace("7", "SEVEN");
		plainText = plainText.replace("8", "EIGHT");
		plainText = plainText.replace("9", "NINE");
		plainText = plainText.replace("0", "ZERO");
		
		messageSize = plainText.length();
		
		System.out.println("The modified message is: " + plainText);
		
		System.out.println("Enter option");
		option = scanner.nextLine();
		
		if (option.trim().toLowerCase().equals("encrypt")) {
			for (int i =0; i< messageSize; i++) {
				key += (char) ('A' + random.nextInt(26));
			}
			
			System.out.println("The key is:" + key);
			
			encryptedMessage = encrypt(plainText, key);
			
			System.out.println("The encrypted message is: " + encryptedMessage);
		} else if (option.trim().toLowerCase().equals
				("decrypt")) {
			System.out.println("Eneter key");
			
			key = scanner.nextLine();
			
			encryptedMessage = decrypt (plainText, key);
			
			System.out.println("The source text is: " + encryptedMessage);
		} else {
			System.out.println("Unknown command");
		}
	}
}
