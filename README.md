PySpeedTest
===========

PySpeedTest is a simple package that uses Selenium to automate tests from speedtest.net.

## Requirements

You need Python3 with the `selenium` package. Be sure that WebDrivers are in your system `$PATH`.

To use `tcpdump` and get traffic traces, you need to execute it as `root`.

Follow this instructions:
https://gist.github.com/zapstar/3d2ff4f345b43ce7918889053503ef84

For Mac OS, just install Wireshark that does the magic. Note that you must specify the interface.


## Example
You can run a test with:
```
results_chrome  = pyspeedtest.run_speedtest(browser="chrome", pcap_path="trace.pcap")
print(results_chrome)
```
