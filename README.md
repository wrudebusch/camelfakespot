# camelfakespot
Camel Camel Camel and FakeSpot Amazon product Python crawler

## Quick start
Hint: Use Chromedriver and don't do the Fakespot step. (change the `webdriver.Firefox` to `webdriver.Chrome` wherever you see it).

```sudo python3 -m pip install -U pip```

```sudo python3 -m pip install pandas selenium bs4```

## ARM geckodriver
Below is the process to crosscompile the ARM (Raspberry Pi 4 compatible) Geckodriver for Firefox. Which is needed because Fakespot.com on ARM Chrome will not let you use the search bar for some reason?

```sudo apt-get install mercurial```

```hg clone https://hg.mozilla.org/mozilla-central/ firefox-source```

Then follow these instructions: https://firefox-source-docs.mozilla.org/testing/geckodriver/ARM.html

I've also included the one I built in this repo. It took like 2 hours and many GB of precious microSD space so you're weeeeeeelcome.
