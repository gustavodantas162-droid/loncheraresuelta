import type { Metadata } from 'next';
import './globals.css';
export const metadata: Metadata = {
  title: 'Lonchera Resuelta',
  description: 'Cuatro semanas de loncheras organizadas en un solo PDF. 20 combinaciones, 40 recetas y 4 listas de compras.',
  robots: { index: false, follow: false },
  openGraph: { title: 'Lonchera Resuelta', description: 'Mañana hay clases. La lonchera ya tiene plan.', images: ['https://loncheraresuelta.vercel.app/images/lonchera-16.webp'] },
};
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="es-419"><head>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,500;0,600;0,700;0,800;0,900;1,700;1,800;1,900&family=Playfair+Display:ital,wght@0,700;0,800;0,900;1,700;1,800;1,900&display=swap" rel="stylesheet" />
      <script src="/tracking.js" />
  </head><body>{children}</body></html>;
}

