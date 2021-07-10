
import java.util.logging.Level;
import java.util.logging.Logger;

public class Main {
	public static void main(String[] args) {
		new MeuThread().start();

		MeuRunnable meuRunnable = new MeuRunnable();
		new Thread(meuRunnable).start();
		for (int i = 0; i < 10; i++) {
			System.out.println("Main: " + i);

			try {
				Thread.sleep(10000);
			} catch (InterruptedException ex) {
				Logger.getLogger(Main.class.getName()).log(Level.SEVERE, null, ex);
			}
		}
	}
}
