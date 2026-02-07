---
layout: page
title: null
permalink: /blog/
---

<p class="blog-intro">
    A collection of blog posts that may appear without link and are just on topics that I think are interesting.
</p>

<ul class="post-list">
{% for post in site.posts %}
  <li class="post-item">
    <h2 class="post-item-title">
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    </h2>
    <div class="post-item-meta">
      {{ post.date | date: "%B %d, %Y" }}
      {% assign words = post.content | number_of_words %}
      {% assign minutes = words | divided_by: 200 %}
      {% if minutes < 1 %}{% assign minutes = 1 %}{% endif %}
      · {{ minutes }} min read
    </div>
    {% if post.excerpt %}
    <p class="post-item-excerpt">{{ post.excerpt | strip_html | truncate: 160 }}</p>
    {% endif %}
  </li>
{% endfor %}
</ul>

{% if site.posts.size == 0 %}
<p>No posts yet. Check back soon!</p>
{% endif %}
