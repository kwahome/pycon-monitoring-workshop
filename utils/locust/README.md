### Installing Locust:
The example script illustrate how to use Locust to load test an HTTP server.

Follow this link to install Locust.

### Start Locust:

You can run [Locust](https://locust.io/) on the web interface or the CLI tool.

**No-Web/CLI**:

```
locust -f {{YOUR_.py_SCRIPT}} --host=http://0.0.0.0:9300 --no-web -c 10 -r 1 -t 1m
```

**Web**:

```
locust -f {{YOUR_.py_SCRIPT}} --host=http://0.0.0.0:9300
```

To see all available options type `locust --help`. :heart::sparkles::sunglasses: