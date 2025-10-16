// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  const pathname = new URL(request.url).pathname;
  const response = NextResponse.next();

  // Attach current path as a custom header
  response.headers.set('x-pathname', pathname);
  return response;
}

// Apply to ALL routes in the app
export const config = {
  matcher: ['/((?!_next|api|static|favicon.ico).*)'],
};
