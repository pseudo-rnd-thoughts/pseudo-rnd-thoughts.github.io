// Main JavaScript file

(function() {
  'use strict';

  // Lightbox functionality
  function initLightbox() {
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxCaption = document.getElementById('lightbox-caption');
    const closeBtn = document.querySelector('.lightbox-close');
    const masonryItems = document.querySelectorAll('.masonry-item');

    if (!lightbox || !masonryItems.length) return;

    // Open lightbox
    masonryItems.forEach(item => {
      item.addEventListener('click', function() {
        const img = this.querySelector('img');
        const caption = this.dataset.caption || '';

        lightboxImg.src = img.src;
        lightboxImg.alt = img.alt;
        lightboxCaption.textContent = caption;
        lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
      });
    });

    // Close lightbox
    function closeLightbox() {
      lightbox.classList.remove('active');
      document.body.style.overflow = '';
    }

    closeBtn.addEventListener('click', closeLightbox);

    lightbox.addEventListener('click', function(e) {
      if (e.target === lightbox) {
        closeLightbox();
      }
    });

    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && lightbox.classList.contains('active')) {
        closeLightbox();
      }
    });
  }

  // TOC scroll highlighting (optional enhancement)
  function initTocHighlight() {
    const toc = document.querySelector('.toc');
    if (!toc) return;

    const tocLinks = toc.querySelectorAll('a');
    const headings = [];

    tocLinks.forEach(link => {
      const id = link.getAttribute('href').slice(1);
      const heading = document.getElementById(id);
      if (heading) {
        headings.push({ id, element: heading, link });
      }
    });

    if (!headings.length) return;

    function highlightToc() {
      const scrollPos = window.scrollY + 100;

      let current = headings[0];
      for (const heading of headings) {
        if (heading.element.offsetTop <= scrollPos) {
          current = heading;
        }
      }

      tocLinks.forEach(link => link.classList.remove('active'));
      current.link.classList.add('active');
    }

    window.addEventListener('scroll', highlightToc);
    highlightToc();
  }

  // Initialize on DOM ready
  document.addEventListener('DOMContentLoaded', function() {
    initLightbox();
    initTocHighlight();
  });
})();
