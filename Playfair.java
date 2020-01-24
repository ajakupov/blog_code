import java.util.Scanner;

import sun.reflect.ReflectionFactory.GetReflectionFactoryAction;

public class Playfair {
	private static char[][] alphaMatrix;
	private static String key;
	private static String message;
	private static Scanner scanner;
	private static String encryptedMessage = "";
	
	public static int getRow(char letter, char[][] alphaMatrix) {
		int row = -1;
		
		for (int i = 0; i<5; i++) {
			for (int j =0; j<5; j++ ) {
				if (alphaMatrix[i][j]==letter) {
					row = i;
				}
			}
		}
		
		return row;
	}
	
	public static int getColumn(char letter, char[][] alphaMatrix) {
		int column = -1;
		
		for (int i = 0; i<5; i++) {
			for (int j =0; j<5; j++ ) {
				if (alphaMatrix[i][j]==letter) {
					column = j;
				}
			}
		}
		
		return column;
	}
	
	public static void main (String[] args) {
		System.out.println("Welcome");
		scanner = new Scanner(System.in);
		System.out.println("Enter your key:");
		key = scanner.nextLine();
		key = key.replaceAll("\\s","").trim().toUpperCase();
		String temp = "";
		
		for (char letter:key.toCharArray()) {
			if (!(temp.indexOf(letter)>=0)) {
				temp+=letter;
			}
		}
		
		key = temp;
		
		alphaMatrix = new char[5][5];
		
		int counter = 0;
		char symbol;
		
		//create a string then transform to matrix
		while (key.toCharArray().length != 26) {
			symbol = (char) ('A' + counter);
			if ((key.indexOf(symbol)<0) && (symbol!= 'Q') ) {
				key +=symbol;
			}
			symbol = (char) ('A' + counter++);
		}
		System.out.println(key);
		
		//transform a string to matrix
		for (int i = 0, k =0; i<5; i++) {
			for (int j =0; j<5; j++) {
				alphaMatrix[i][j] = key.toCharArray()[k];
				k = ++k % key.length();
			}
		}
		//now the matrix is ready
		
		for (int i = 0; i<5; i++) {
			for (int j =0; j<5; j++ ) {
				System.out.print(alphaMatrix[i][j] + " ");
			}
			System.out.println();
		}
		
		System.out.println("Enter your message: ");
		message = scanner.nextLine();
		message = message.replaceAll("\\s","").trim().toUpperCase();
		
		//replace the repeating symbols
		
		for (int i =0; i < message.length()-1; i++) {
			if (message.
					toCharArray()[i]==
						message.toCharArray()[i+1]) {
				message = message.substring(0,i+1) 
				+ 'X' + message.substring(i+1,message.length());
			}
		}
		
		
		if (message.length()%2 !=0) {
			message +='Z';
		}
		System.out.println(message);
		
		//start working with letter pairs
		//if the letters get columns and getrows correspond...
		//either...
		for (int i =0; i< message.length(); i++) {
			System.out.println(message.
					toCharArray()[i] + "~" + 
					message.toCharArray()[i+1]);
			if (getColumn(message.
					toCharArray()[i], alphaMatrix) == getColumn(message.
							toCharArray()[i+1], alphaMatrix)) {
				System.out.println("The columns are equal");
				if (getRow(message.
						toCharArray()[i], alphaMatrix) != 4) {
					encryptedMessage +=alphaMatrix[getRow(message.
							toCharArray()[i], alphaMatrix)+1]
							[getColumn(message.
									toCharArray()[i], alphaMatrix)];
				} else {
					encryptedMessage +=alphaMatrix[0]
							[getColumn(message.
									toCharArray()[i], alphaMatrix)];
				}
				if (getRow(message.
						toCharArray()[i+1], alphaMatrix) != 4) {
					encryptedMessage +=alphaMatrix[getRow(message.
							toCharArray()[i+1], alphaMatrix)+1]
							[getColumn(message.
									toCharArray()[i+1], alphaMatrix)];
				} else {
					encryptedMessage +=alphaMatrix[0]
							[getColumn(message.
									toCharArray()[i+1], alphaMatrix)];
				}
			}else if (getRow(message.
					toCharArray()[i], alphaMatrix) == getRow(message.
							toCharArray()[i+1], alphaMatrix)) {
				System.out.println("The rows are equal");
				if (getColumn(message.
						toCharArray()[i], alphaMatrix) != 4) {
					encryptedMessage +=alphaMatrix[getRow(message.
							toCharArray()[i], alphaMatrix)]
							[getColumn(message.
									toCharArray()[i], alphaMatrix)+1];
				} else {
					encryptedMessage +=alphaMatrix[getRow(message.
							toCharArray()[i], alphaMatrix)]
							[0];
				}
				if (getRow(message.
						toCharArray()[i+1], alphaMatrix) != 4) {
					encryptedMessage +=alphaMatrix[getRow(message.
							toCharArray()[i+1], alphaMatrix)]
							[getColumn(message.
									toCharArray()[i+1], alphaMatrix)+1];
				} else {
					encryptedMessage +=alphaMatrix[getRow(message.
							toCharArray()[i+1], alphaMatrix)]
							[0];
				}
			} else {
				System.out.println("Neither");
				encryptedMessage +=alphaMatrix[getRow(message.
						toCharArray()[i], alphaMatrix)]
						[getColumn(message.
								toCharArray()[i+1], alphaMatrix)];
				encryptedMessage +=alphaMatrix[getRow(message.
						toCharArray()[i+1], alphaMatrix)]
						[getColumn(message.
								toCharArray()[i], alphaMatrix)];
			}
			i++;
		}
		
		System.out.println(encryptedMessage);
	}
}
