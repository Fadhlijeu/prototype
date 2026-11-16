# ASCII Christmas Tree

A browser-native adaptation of the procedural 3D ASCII Christmas tree. The scene is drawn locally with the Canvas 2D API and does not require a build step, Python, Pygame, or third-party graphics libraries.

## Open

Visit the GitHub Pages deployment:

https://fadhlijeu.github.io/prototype/ui/web/apps/ascii-christmas-tree/

Or open `index.html` directly in a modern browser.

## Scene sequence

| Time | Event |
| --- | --- |
| 0.2–4.6 s | Snowy ground, trunk, and branches grow from bottom to top |
| 4.8–7.0 s | Gold garland winds around the tree |
| 6.6–8.6 s | Red and gold ornaments appear |
| 7.8–10.4 s | Warm fairy lights switch on |
| 9.2–10.9 s | Wrapped gifts pop into place |
| 11.4 s | The star lights up |
| 13.2 s | “Merry Christmas 2026” is typed beneath the tree |

## Controls

- **Space** — pause / resume
- **R** — restart the animation
- **S** — save the current frame as a PNG
- **Rotation** — freeze or resume the camera rotation
- **Timeline** — jump to a moment in the sequence

The layout adapts the character grid for narrow screens. The animation and screenshot export run entirely on the client.
