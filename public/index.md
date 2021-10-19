---
layout: default
title: IATI RSS Feeds
---

The missing RSS feeds for various IATI websites.

{% include button.html fname="iatistandard.xml" title="IATI Standard RSS feed" %}

{% include button.html fname="iaticonnect.xml" title="IATI Connect RSS feed" %}

{% include button.html fname="iaticonnect-comments.xml" title="IATI Connect comments RSS feed" %}

{% assign now = site.time | date_to_rfc822 %}

_Last updated: <abbr title="{{ now }}" id="last-updated">{{ now }}</abbr>._
