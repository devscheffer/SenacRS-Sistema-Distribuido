
import java.util.logging.Level;
import java.util.logging.Logger;

public class Main {
    public static void main(String[] args) {
        for(int i=1; i<11;i++)
            new MeuThread("Multiplos de "+i,i,i*10).start();
    }
}
