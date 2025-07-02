import { NextRequest, NextResponse } from "next/server";

export default function middleware(request: NextRequest) {
  const pathname = request.nextUrl.pathname;

  const response = NextResponse.next();
  response.headers.set("x-curr-path", pathname);

  if (pathname === "/") {
    return NextResponse.redirect(new URL("/verbs", request.url));
  }

  return response;
}
export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
