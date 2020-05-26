package myfile;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Map;
import java.util.Map.Entry;
import java.util.TreeMap;

public class MyFile {
	private String name;
	private BufferedReader lecteur;
	private Map<String, Integer> mots;

	public MyFile(String n) {
		name = n;
		lecteur = null;
		mots = new TreeMap<String, Integer>();
	}

	public void ouvrirFichier() {
		try {
			lecteur = new BufferedReader(new FileReader(name));
		} catch (FileNotFoundException e) {
			System.out.println("Erreur ouverture fichier");
		}
	}

	public void nbOccurence() throws IOException {
		ouvrirFichier();
		String line;
		String[] lines;
		while ((line = lecteur.readLine()) != null) {
			lines = line.split(" |\\.|,|;|\\(|\\)");
			for (int i = 0; i < lines.length; i++) {
				if (mots.containsKey(lines[i].toLowerCase())) {
					mots.put(lines[i].toLowerCase(), mots.get(lines[i].toLowerCase()) + 1);
				} else {
					mots.put(lines[i].toLowerCase(), 1);
				}
			}
		}
		lecteur.close();
	}

	public String affichageOccurence() throws IOException {
		nbOccurence();
		String s = "";
		for (Entry<String, Integer> entry : mots.entrySet()) {
			s += "Mot : " + entry.getKey() + " --> Nombre d'occurence : " + entry.getValue() + "\n";
		}
		return s;
	}

	public void ecritureResultatFichier(String name) throws IOException {
		File file = new File(name);
		if (!file.exists()) {
			file.createNewFile();
		}
		FileWriter fw = new FileWriter(file.getAbsoluteFile());
		BufferedWriter bw = new BufferedWriter(fw);
		for (Entry<String, Integer> entry : mots.entrySet()) {
			bw.write("Mot : " + entry.getKey() + " --> Nombre d'occurence : " + entry.getValue() + "\n");
		}
		bw.close();
	}

	public static void main(String[] args) throws IOException {
		long debut = System.currentTimeMillis();
		MyFile myFile1 = new MyFile("lettre.txt");
		System.out.println(myFile1.affichageOccurence());
		myFile1.ecritureResultatFichier("resLettreClassique.txt");
		long fin = System.currentTimeMillis()-debut;
		System.out.println("Temps d'exécution : " + fin + " ms");
	}
}
