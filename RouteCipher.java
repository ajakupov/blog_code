import java.util.Random;
import java.util.Scanner;

import sun.net.www.content.text.plain;


public class RouteCipher {
	private static String plainText = "";
	private static int rows = 0;
	private static int columns = 0;
	private static char[][] array;
	private static Scanner scanner;
	private static String encodedMessage = "";
	private static String decodedMessage;
	
	
	public static void main (String[] args) {
		scanner = new Scanner (System.in);
		System.out.println("Enter text");
		plainText = scanner.nextLine();
		plainText = plainText.trim();
		plainText = plainText.replaceAll("\\s","");
		Random random = new Random();
		
		if (plainText.length()%4 ==0) {
			rows = plainText.length()/4;
			columns = 4;
		} else {
			while (plainText.length()%4!=0) {
				plainText += (char)('A' 
				+ random.nextInt(41));
			}
			System.out.println(plainText);
			rows = plainText.length()/4;
			columns = 4;
		}
		
		array = new char[rows][columns];
		
		for (int i = 0, k =0; i<rows; i++) {
			for (int j =0; j<columns; j++) {
				System.out.println(
						plainText.toCharArray()[k]);
				array[i][j] = plainText.toCharArray()[k];
				k = ++k % plainText.length();
			}
		}
		
		System.out.println("Message in a table");
		for (int i = 0; i<rows; i++) {
			for (int j =0; j<columns; j++) {
				System.out.print(array[i][j] + " ");
			}
			System.out.println();
		}
		
		System.out.println("Transformation matrix");
		for (int j = columns-1; j >= 0; j--) {
			for (int i = rows-1; i >= 0; i--) {
				System.out.print(array[i][j] + " ");
				encodedMessage += array[i][j];
			}
			System.out.println();
		}
		
		System.out.println("The " +
				"encrypted message is: "+ encodedMessage);
	}
}
