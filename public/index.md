---
layout: default
title: IATI RSS Feeds
---

The missing RSS feeds for various IATI websites.

<div class="row">
  {% include card.html fname="iatistandard.xml" title="IATI Standard RSS feed" %}

  {% include card.html fname="iaticonnect.xml" title="IATI Connect RSS feed" %}

  {% include card.html fname="iaticonnect-comments.xml" title="IATI Connect comments RSS feed" %}
</div>

_Last updated: <span id="last-updated">{{ site.time | date_to_rfc822 }}</span>._
