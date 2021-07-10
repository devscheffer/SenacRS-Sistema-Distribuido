
import java.util.logging.Level;
import java.util.logging.Logger;

public class MeuThread extends Thread {
	private String nome;
	private int multiplo, maximo;

	public MeuThread(String nome, int multiplo, int maximo) {
		this.nome = nome;
		this.multiplo = multiplo;
		this.maximo = maximo;
	}

	@Override
	public void run() {
		for (int i = multiplo; i <= maximo; i += multiplo) {
			System.out.println(nome + ": " + i);
			try {
				Thread.sleep(10000);
			} catch (InterruptedException ex) {
				Logger.getLogger(MeuThread.class.getName()).log(Level.SEVERE, null, ex);
			}
		}
	}
}
