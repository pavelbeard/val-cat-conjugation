import { NextRequest, NextResponse } from "next/server";

export default function middleware(request: NextRequest) {
  // Middleware logic can be added here
  // For example, you can check for authentication, modify headers, etc.

  // Currently, this middleware does nothing and just returns the request

  const pathname = request.nextUrl.pathname;

  const response = NextResponse.next();
  response.headers.set("x-curr-path", pathname);

  if (pathname === "/") {
    return NextResponse.redirect(new URL("/search", request.url));
  }

  return response;
}
export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
