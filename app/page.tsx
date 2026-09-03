'use client';
import { useEffect, useRef } from 'react';
import { pageHtml } from './content';
export default function Home() {
  const root = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const el = root.current;
    if (!el) return;
    const progress = () => {
      const bar = el.querySelector<HTMLElement>('#progressBar');
      const total = document.documentElement.scrollHeight - innerHeight;
      if (bar) bar.style.width = `${total > 0 ? Math.min(scrollY / total * 100, 100) : 0}%`;
    };
    const click = (event: Event) => {
      const button = (event.target as Element).closest<HTMLButtonElement>('.faq-question');
      if (!button) return;
      const item = button.closest('.faq-item')!;
      const wasOpen = item.classList.contains('open');
      el.querySelectorAll('.faq-item').forEach(x => {
        x.classList.remove('open');
        x.querySelector('button')?.setAttribute('aria-expanded', 'false');
      });
      if (!wasOpen) { item.classList.add('open'); button.setAttribute('aria-expanded', 'true'); }
    };
    const tracks = ['carouselTrack', 'depoCarouselTrack'].map(id => el.querySelector<HTMLElement>(`#${id}`));
    const clones: Node[] = [];
    tracks.forEach(track => {
      if (!track) return;
      [...track.children].forEach(child => {
        const clone = child.cloneNode(true) as HTMLElement;
        clone.setAttribute('aria-hidden', 'true'); clone.dataset.clone = 'true';
        track.append(clone); clones.push(clone);
      });
    });
    const resize = () => tracks.forEach(track => {
      const firstClone = track?.querySelector<HTMLElement>('[data-clone]');
      if (track && firstClone) track.style.setProperty(track.id === 'carouselTrack' ? '--scroll-distance' : '--depo-scroll-distance', `${firstClone.offsetLeft}px`);
    });
    resize();
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('visible', 'animated'); observer.unobserve(entry.target); }
    }), { threshold: 0.1 });
    el.querySelectorAll('.ideal-card-wrap,.bonus-card,.dor-box,.produto-inner,.bonus-bridge,.garantia-card,.autoridade-inner,.faq-item,.checklist').forEach(x => observer.observe(x));
    el.addEventListener('click', click);
    window.addEventListener('scroll', progress, { passive: true });
    window.addEventListener('resize', resize);
    return () => {
      observer.disconnect(); clones.forEach(x => x.parentNode?.removeChild(x));
      el.removeEventListener('click', click);
      window.removeEventListener('scroll', progress); window.removeEventListener('resize', resize);
    };
  }, []);
  return <div ref={root} style={{ fontWeight: 600 }} dangerouslySetInnerHTML={{ __html: pageHtml }} />;
}
