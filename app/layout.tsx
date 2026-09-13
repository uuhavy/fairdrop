import type { Metadata } from "next";
import "./globals.css";
export const metadata:Metadata={title:"FairDrop — Community rewards",description:"Transparent contribution reviews and reward allocation for communities.",icons:{icon:"/favicon.svg"}};
export default function RootLayout({children}:Readonly<{children:React.ReactNode}>){return <html lang="en"><body>{children}</body></html>}
