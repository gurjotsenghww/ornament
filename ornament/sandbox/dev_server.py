import asyncio
import http.server
import socketserver
import threading
from pathlib import Path
from typing import Optional

class PreviewServerHandler(http.server.SimpleHTTPRequestHandler):
    """
    HTTP handler serving Next.js App Router static/rendered view with route emulation (Section 15, 42).
    Returns 404 for non-existent routes (e.g. /contact-us) and 200 for valid routes (e.g. /contact).
    """

    def __init__(self, *args, workspace_root: Path = None, **kwargs):
        self.workspace_root = workspace_root
        super().__init__(*args, **kwargs)

    def do_GET(self):
        clean_path = self.path.split("?")[0].rstrip("/")

        # Route matching for portfolio
        if clean_path == "" or clean_path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()

            # Read layout and page
            navbar_file = self.workspace_root / "components" / "Navbar.tsx"
            navbar_code = navbar_file.read_text(encoding="utf-8") if navbar_file.exists() else ""
            contact_href = "/contact-us" if 'href="/contact-us"' in navbar_code else "/contact"

            html = f"""<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <title>Alex Vance | Senior AI Engineer</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    body {{ background-color: #09090b; color: #f4f4f5; }}
  </style>
</head>
<body className="min-h-screen bg-[#09090b] text-zinc-100 p-6 font-sans">
  <header class="sticky top-0 z-50 w-full border-b border-zinc-800 bg-[#09090b]/80 backdrop-blur-md mb-8">
    <div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
      <span class="font-bold text-lg text-white">Alex Vance<span class="text-indigo-500">.</span></span>
      <nav aria-label="Main Navigation" class="flex items-center space-x-6 text-sm">
        <a href="#about" class="text-zinc-400 hover:text-white">About</a>
        <a href="#projects" class="text-zinc-400 hover:text-white">Projects</a>
        <a id="nav-contact-button" href="{contact_href}" class="px-4 py-2 rounded-full bg-indigo-600 hover:bg-indigo-500 text-white font-medium">Contact</a>
      </nav>
    </div>
  </header>
  <main class="max-w-6xl mx-auto px-4">
    <section class="py-16">
      <h1 class="text-5xl font-extrabold text-white mb-4">Architecting autonomous agentic systems.</h1>
      <p class="text-zinc-400 text-lg max-w-2xl mb-6">Specializing in local-first AI engineering and high-performance web systems.</p>
      <a href="{contact_href}" class="px-6 py-3 rounded-lg bg-indigo-600 text-white font-semibold">Get in Touch</a>
    </section>
  </main>
</body>
</html>"""
            self.wfile.write(html.encode("utf-8"))
            return

        elif clean_path == "/contact":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Contact Alex Vance</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-[#09090b] text-zinc-100 p-8 font-sans">
  <div class="max-w-xl mx-auto">
    <h1 class="text-3xl font-bold mb-4">Get in Touch</h1>
    <form class="space-y-4 bg-zinc-900 p-6 rounded-xl border border-zinc-800">
      <input id="name" placeholder="Name" class="w-full p-2 bg-zinc-800 rounded border border-zinc-700" />
      <button type="button" class="w-full py-2 bg-indigo-600 rounded text-white font-semibold">Send</button>
    </form>
  </div>
</body>
</html>"""
            self.wfile.write(html.encode("utf-8"))
            return

        elif clean_path == "/contact-us":
            # 404 Route Mismatch Error (Section 14, 59)
            self.send_response(404)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            html = """<!DOCTYPE html>
<html>
<head><title>404 - Not Found</title></head>
<body style="background:#09090b;color:#f87171;font-family:sans-serif;padding:40px;text-align:center;">
  <h1>404 - Page Not Found</h1>
  <p>The route <code>/contact-us</code> does not exist on this server. Active route is <code>/contact</code>.</p>
</body>
</html>"""
            self.wfile.write(html.encode("utf-8"))
            return

        # Default 404
        self.send_response(404)
        self.end_headers()


class DevPreviewServer:
    """
    Dedicated local preview dev server for Playwright browser testing and user preview.
    """

    def __init__(self, workspace_root: Path, port: int = 3456):
        self.workspace_root = workspace_root
        self.port = port
        self.server: Optional[socketserver.TCPServer] = None
        self.thread: Optional[threading.Thread] = None

    def start(self):
        handler = lambda *args, **kwargs: PreviewServerHandler(*args, workspace_root=self.workspace_root, **kwargs)
        # Allow immediate port reuse
        socketserver.TCPServer.allow_reuse_address = True
        self.server = socketserver.TCPServer(("127.0.0.1", self.port), handler)
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.server = None

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.port}"
