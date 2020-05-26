package mapReduce;

/**
 * WordCount.java
 * Un programme qui simule l'execution MapReduce pour 
 * compter en parallele le nombre d'occurances de chaque mot
 * dans un fichier (de très grand taille)
 *
 *
 */

import java.util.*;
import java.util.concurrent.*;
import java.io.*;

public class WordCount {
	// barrière pour séparer l'execution des Mappers et des Reducers
	public static CyclicBarrier myBarrier;
	// tableau de HashMaps pour stocker les résultats des Mappers, un HashMap par
	// Mapper
	public static HashMap<String, Integer>[] intermediateResults;
	public static int nbMappers = 5;
	public static int nbReducers = 1;
	// fichier d'entrée avec le texte à analyser
	public static String fileName = "lettre.txt";
	public static String fileContent = "";

	@SuppressWarnings({ "resource", "unchecked" })
	public static void main(String[] args) {
		long debut = System.currentTimeMillis();
		
		// tableau de Mappers (un Mapper dans une file d'exécution different)
		Mapper[] mappers = new Mapper[nbMappers];
		// tableau de Reducers (dans cet exemple très simple on va utiliser un seul
		// Reducer)
		Reducer[] reducers = new Reducer[nbReducers];

		intermediateResults = new HashMap[nbMappers];

		myBarrier = new CyclicBarrier(nbMappers + 1);

		try {
			fileContent = new Scanner(new File(fileName)).useDelimiter("\\A").next();
		} catch (Exception e) {
			System.out.println("Error reading the input file.");
		}

		int chunkSize = (int) fileContent.length() / nbMappers;

		// division du texte d'entrée en morceaux (de type String) stockés dans
		// le tableau de Strings chunks[] (un morceau par Mapper)
		String[] chunks = new String[nbMappers];
		int offset = 0;
		for (int i = 0; i < nbMappers; i++) {
			chunks[i] = fileContent.substring(offset, offset + chunkSize);
			offset += chunkSize;
		}

		// initialisation des Mappers et Reducers
		for (int i = 0; i < nbMappers; i++) {
			intermediateResults[i] = new HashMap<String, Integer>();
			mappers[i] = new Mapper(i, chunks[i]);
		}
		for (int j = 0; j < nbReducers; j++)
			reducers[j] = new Reducer(j);

		// étape MAP: les Mappers sont lancés en parallèle
		for (int k = 0; k < nbMappers; k++) {
			mappers[k].start();
		}

		// on attend que tous les Mappers finissent
		try {
			myBarrier.await();
		} catch (Exception e) {
			e.printStackTrace();
		}

		// étape REDUCE: les Reducers sont lancés en parallèle (un seul dans cet
		// exemple)
		for (int l = 0; l < nbReducers; l++) {
			reducers[l].start();
		}
		
		long fin = System.currentTimeMillis()-debut;
		System.out.println("Temps d'exécution : " + fin + " ms");

	}

}
