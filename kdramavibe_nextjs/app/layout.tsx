import './globals.css';
import Footer from '@/components/Footer';
import Header from '@/components/Header';
import { ThemeProvider } from "next-themes";

export const metadata = {
  title: 'KdramaVibe',
  description: 'K-Drama Dreams, K-Actor Gleams',
  icons: {
    icon: "/images/icon.png",
  }
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (

   <html lang="en" suppressHydrationWarning>
      <body className="transition-theme max-h-screen max-w-screen custom-scrollbar overflow-y-auto">
       
        <ThemeProvider attribute="class" defaultTheme="system">
           <Header/>
        <main className="transition-theme">{children}</main>
        <Footer/>
        </ThemeProvider>
       
      </body>
    </html>
  );
}
