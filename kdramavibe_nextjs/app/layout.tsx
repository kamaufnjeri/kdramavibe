import './globals.css'; // Import global CSS including Tailwind and custom styles
import Footer from '@/components/common/Footer'; // Footer component
import Header from '@/components/common/Header'; // Header component
import { ThemeProvider } from "next-themes"; // Theme provider for dark/light mode

// Metadata for the app
export const metadata = {
  title: 'KdramaVibe', // Browser tab title
  description: 'K-Drama Dreams, K-Actor Gleams', // App description
  icons: {
    icon: "/images/icon.png", // Favicon
  }
};

// RootLayout component wraps all pages with HTML structure, theme, header, footer
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className="transition-theme max-h-screen max-w-screen custom-scrollbar overflow-y-auto">
        {/* ThemeProvider provides dark/light mode support */}
        <ThemeProvider attribute="class" defaultTheme="system">
          {/* Header displayed on all pages */}
          <Header />
          {/* Main content */}
          <main className="transition-theme">{children}</main>
          {/* Footer displayed on all pages */}
          <Footer />
        </ThemeProvider>
      </body>
    </html>
  );
}
