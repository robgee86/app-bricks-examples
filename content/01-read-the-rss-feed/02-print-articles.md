---
title: Print the articles
summary: Confirm the fetch worked by printing each article to the console.
patches:
  - path: ../assets/1.2_print-articles.patch
    label: Add a print loop
attachments:
  - path: ../assets/1.2_print-articles.zip
    label: rss-reader after step 1.2
---

Now that the articles live in memory, let's prove it: at the end of `fetch_feed()` we print a one-line summary plus one line per article title.

This is the simplest possible "did it work?" affordance. `print` writes to the App Lab process log, which you can read from the Logs panel. It's fine for quick verification but it's not great for a longer-lived app — in the next step we'll graduate to the brick's `Logger`, which gives us levels (info / warning / error) and a nicely tagged source.

Go to the rss-server's director UI in another tab and use **Add** / **Remove** to change the number of published articles, then restart the rss-reader. The console should print the new count each time.

**Checkpoint:** the logs show `Fetched N articles:` followed by the titles you see in the rss-server's director.
