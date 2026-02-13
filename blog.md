---
layout: page
title: null
permalink: /blog/
---

<p class="blog-intro">
    A collection of blog posts that may appear without link on topics that I think are interesting.
</p>

<ul class="post-list">
{% for post in site.posts %}
  <li class="post-item">
    <h2 class="post-item-title">
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
    </h2>
    <div class="post-item-meta">
      {{ post.date | date: "%B %d, %Y" }}
      {% assign script_parts = post.content | split: '<script' %}
      {% assign prose = script_parts.first %}
      {% for part in script_parts %}
        {% unless forloop.first %}
          {% assign after_close = part | split: '</script>' %}
          {% if after_close.size > 1 %}{% assign prose = prose | append: after_close.last %}{% endif %}
        {% endunless %}
      {% endfor %}
      {% assign words = prose | strip_html | number_of_words %}
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
