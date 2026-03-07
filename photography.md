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
      {% unless file.path contains '/thumbnails/' %}
        {% if file.extname == '.webp' %}
          {% assign thumb_path = file.path | replace: '/assets/images/photography/', '/assets/images/photography/thumbnails/' %}
          <div class="masonry-item" data-full="{{ file.path | relative_url }}">
            <img src="{{ thumb_path | relative_url }}" alt="Photography" loading="lazy">
          </div>
        {% endif %}
      {% endunless %}
    {% endif %}
  {% endfor %}
</div>

<!-- Lightbox container -->
<div class="lightbox" id="lightbox">
  <button class="lightbox-close" aria-label="Close">&times;</button>
  <div class="lightbox-content">
    <img src="" alt="" id="lightbox-img">
  </div>
</div>

<script>
  document.addEventListener('DOMContentLoaded', function() {
    const grid = document.querySelector('.masonry-grid');
    const items = Array.from(grid.querySelectorAll('.masonry-item'));
    for (let i = items.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [items[i], items[j]] = [items[j], items[i]];
    }
    items.forEach(item => grid.appendChild(item));
  });
</script>
