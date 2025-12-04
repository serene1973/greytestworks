HttpProxyServer server =
        DefaultHttpProxyServer.bootstrap()
            .withPort(0)
            .withFiltersSource(new HttpFiltersSourceAdapter() {
                @Override
                public HttpFilters filterRequest(HttpRequest originalRequest, ChannelHandlerContext ctx) {
                    return new HttpFiltersAdapter(originalRequest) {
                        @Override
                        public HttpResponse clientToProxyRequest(HttpObject httpObject) {
                            if (httpObject instanceof HttpRequest) {
                                HttpRequest req = (HttpRequest) httpObject;

                                String auth = Base64.getEncoder().encodeToString(("corp\\qa-test:@Gkb6.cT!").getBytes());
                                req.headers().set("Authorization", "Basic " + auth);
                            }
                            return null;
                        }
                    };
                }
            })
            .start();

int proxyPort = server.getListenAddress().getPort();



<dependency>
  <groupId>org.littleshoot</groupId>
  <artifactId>littleproxy-mitm</artifactId>
  <version>2.0.1</version>
</dependency>


Proxy seleniumProxy = new Proxy();
seleniumProxy.setHttpProxy("localhost:" + proxyPort);
seleniumProxy.setSslProxy("localhost:" + proxyPort);

ChromeOptions options = new ChromeOptions();
options.setProxy(seleniumProxy);


