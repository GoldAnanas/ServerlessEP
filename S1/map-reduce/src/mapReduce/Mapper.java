package mapReduce;

import java.util.StringTokenizer;

/**
 * Mapper.java Prend en argument un morceau de texte et compte le nombre
 * d'occurences de chaque mot
 * 
 * les résultats sont stockés dans le HashMap correspondant au Mapper courrant:
 * WriteCount.intermediateResults[id] sous la forme: <mot, nombre d'occurences>
 * 
 */

public class Mapper extends Thread {
	protected int id; // identifiant du Mapper
	protected String myChunk; // morceau de texte à analyser

	public Mapper(int i, String chunkToProcess) {
		id = i;
		myChunk = chunkToProcess;
	}

	public void run() {
		System.out.println("[MAPREDUCE] Mapper " + id + " launched...");
		//System.out.println("[MAPREDUCE] Chunk to process: " + myChunk);
		System.out.println("[MAPREDUCE] Mapper " + id + " starts processing...");

		// ajoute chaque mot de myChunk dans
		// le HashMap WriteCount.intermediateResults[id]
		// avec son nombre d'occurences
		// pour le HashMap: clé = mot, valeur = nombre d'occurences
		StringTokenizer s = new StringTokenizer(myChunk.toLowerCase()," |\\.|,|;|\\(|\\)|\n");

		while (s.hasMoreTokens()) {

			String string = s.nextToken();

			if (!WordCount.intermediateResults[id].containsKey(string)) {
				WordCount.intermediateResults[id].put(string, 1);
			} else {
				int occurence = WordCount.intermediateResults[id].get(string);
				WordCount.intermediateResults[id].put(string, occurence + 1);
			}
		}

		System.out.println("[MAPREDUCE] Mapper " + id + " done!");
		// on attend que tous les Mappers finissent
		try {
			WordCount.myBarrier.await();
		} catch (Exception e) {
			e.printStackTrace();
		}

	}

}
