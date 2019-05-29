import py4j.GatewayServer;

public class Main {
    public static void main(String[] args) {
        Main app = new Main();
        GatewayServer server = new GatewayServer(app);
        server.start();
        System.out.print("\n\n########################################\n" +
                "Started the SimpleNLG Java GatewayServer" +
                "\n########################################\n\n\n");
    }
}
