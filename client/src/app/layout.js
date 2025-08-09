import { Geist, Noto_Sans_JP } from "next/font/google";
import "./globals.css";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/common/app-sidebar";
import { AppProvider } from "@/components/common/app-provider";

const notoSansJP = Noto_Sans_JP({
  variable: "--font-noto-sans-jp",
  subsets: ["latin"],
});

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

export const metadata = {
  title: "POSレジシステムfor蒼翔祭",
  description: "会津大学学園祭・蒼翔祭のためのPOSレジシステム",
  icons: {
    icon: "/soshosai.svg",
  }
};

export default function RootLayout({ children }) {
  return (
    <html lang="ja">
        <body
          className={`${geistSans.variable} ${notoSansJP.variable} antialiased `}
        >
          <div className="bg-neutral-100">
            {/* <AppProvider> */}
              <SidebarProvider >
                <AppSidebar />
                <main className="m-2 rounded-md shadow-lg shadow-black/10 bg-white" style={{height: 'calc(100vh - 1rem)', width: 'calc(100vw - 1rem)'}} >
                  <div className="p-4">
                    <SidebarTrigger />
                    {children}
                  </div>
                </main>
              </SidebarProvider>
            {/* </AppProvider> */}
          </div>
        </body>
    </html>
  );
}
