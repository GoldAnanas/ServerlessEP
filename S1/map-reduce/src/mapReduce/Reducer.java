package mapReduce;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.HashMap;
import java.util.Map.Entry;
import java.util.TreeMap;


/**
 * Reducer.java
 * 
 * utilise les résultats intermediaires de chaque Mapper pour les agréger dans
 * un seul HashMap: finalResultas
 *
 * 
 */

public class Reducer extends Thread {
	protected int id; // identifiant du Reducer (dans cet exemple on va utiliser un seul)
	public TreeMap<String, Integer> finalResults; // HashMap à remplir avec les résultats finaux

	public Reducer(int id) {
		this.id = id;
		finalResults = new TreeMap<String, Integer>();
	}
	
	public void ecritureResultatFichier(String name) throws IOException {
		File file = new File(name);
		if (!file.exists()) {
			file.createNewFile();
		}
		FileWriter fw = new FileWriter(file.getAbsoluteFile());
		BufferedWriter bw = new BufferedWriter(fw);
		for (Entry<String, Integer> entry : finalResults.entrySet()) {
			bw.write("Mot : " + entry.getKey() + " --> Nombre d'occurence : " + entry.getValue() + "\n");
		}
		bw.close();
	}

	public void run() {
		System.out.println("[MAPREDUCE] Reducer " + id + " starts processing...");

		// à compléter: compléter le HashMap finalResults avec
		// les données de tous les Mappers
		for(HashMap<String, Integer> maps : WordCount.intermediateResults) {
			for(Entry<String, Integer> entry : maps.entrySet()) {
				if (!finalResults.containsKey(entry.getKey())) {
					finalResults.put(entry.getKey(), entry.getValue());
				} else {
					finalResults.put(entry.getKey(), finalResults.get(entry.getKey()) + entry.getValue());
				}
			}
		}

		System.out.println("[MAPREDUCE] Reducer " + id + " done!");
		System.out.println("[MAPREDUCE] Final Results: ");

		/*ArrayList<String> keys = new ArrayList<String>(finalResults.keySet());
		Collections.sort(keys);
		for (String key : keys)
			System.out.println(key + ": " + finalResults.get(key));
		*/
		try {
			ecritureResultatFichier("resLettreMapReduce.txt");
		} catch (IOException e) {
			System.out.println("erreur ouverture fichier");
		}
		
	}
}