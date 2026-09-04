'use client';
import { useEffect, useRef } from 'react';
import { pageHtml } from './content';
import { initializePage } from './interactions';
export default function Home() {
  const root = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (root.current) return initializePage(root.current);
  }, []);
  return <div ref={root} style={{ fontWeight: 600 }} dangerouslySetInnerHTML={{ __html: pageHtml }} />;
}
