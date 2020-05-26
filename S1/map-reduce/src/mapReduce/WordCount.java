package mapReduce;

/**
 * WordCount.java
 * Un programme qui simule l'execution MapReduce pour 
 * compter en parallele le nombre d'occurances de chaque mot
 * dans un fichier (de tr�s grand taille)
 *
 *
 */

import java.util.*;
import java.util.concurrent.*;
import java.io.*;

public class WordCount {
	// barri�re pour s�parer l'execution des Mappers et des Reducers
	public static CyclicBarrier myBarrier;
	// tableau de HashMaps pour stocker les r�sultats des Mappers, un HashMap par
	// Mapper
	public static HashMap<String, Integer>[] intermediateResults;
	public static int nbMappers = 5;
	public static int nbReducers = 1;
	// fichier d'entr�e avec le texte � analyser
	public static String fileName = "lettre.txt";
	public static String fileContent = "";

	@SuppressWarnings({ "resource", "unchecked" })
	public static void main(String[] args) {
		long debut = System.currentTimeMillis();
		
		// tableau de Mappers (un Mapper dans une file d'ex�cution different)
		Mapper[] mappers = new Mapper[nbMappers];
		// tableau de Reducers (dans cet exemple tr�s simple on va utiliser un seul
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

		// division du texte d'entr�e en morceaux (de type String) stock�s dans
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

		// �tape MAP: les Mappers sont lanc�s en parall�le
		for (int k = 0; k < nbMappers; k++) {
			mappers[k].start();
		}

		// on attend que tous les Mappers finissent
		try {
			myBarrier.await();
		} catch (Exception e) {
			e.printStackTrace();
		}

		// �tape REDUCE: les Reducers sont lanc�s en parall�le (un seul dans cet
		// exemple)
		for (int l = 0; l < nbReducers; l++) {
			reducers[l].start();
		}
		
		long fin = System.currentTimeMillis()-debut;
		System.out.println("Temps d'ex�cution : " + fin + " ms");

	}

}
