---
layout: page
title: null
permalink: /photography/
---

<p class="photography-intro">
  In my free time, I enjoy doing very amateur photographer, a small selection of those are presented below. 
  Click on any image to view it larger.
</p>

<div class="masonry-grid">
  {% for file in site.static_files %}
    {% if file.path contains '/assets/images/photography/' %}
      {% assign ext = file.extname | downcase %}
      {% if ext == '.jpg' or ext == '.jpeg' or ext == '.png' or ext == '.gif' or ext == '.webp' %}
      <div class="masonry-item">
        <img src="{{ file.path | relative_url }}" alt="Photography" loading="lazy">
      </div>
      {% endif %}
    {% endif %}
  {% endfor %}
</div>

<!-- Lightbox container -->
<div class="lightbox" id="lightbox">
  <button class="lightbox-close" aria-label="Close">&times;</button>
  <div class="lightbox-content">
    <img src="" alt="" id="lightbox-img">
    <div class="lightbox-caption" id="lightbox-caption"></div>
  </div>
</div>
