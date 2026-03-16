import './globals.css';

export const metadata = { title: 'NGBI user' };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body>{children}</body></html>;
}
