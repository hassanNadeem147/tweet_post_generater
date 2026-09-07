import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'TweetAI Generator',
  description: 'Generate polished, publish-ready tweets with AI.',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
