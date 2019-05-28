import py4j.GatewayServer;

public class Main {
    public static void main(String[] args) {
        Main app = new Main();
        GatewayServer server = new GatewayServer(app);
        server.start();
    }
}
