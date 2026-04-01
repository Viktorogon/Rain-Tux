# RainTux Skin Manager — build spec & agent prompt

Use this document to generate the **`ui/`** folder (React + Vite) yourself or to give another tool a complete instruction set. It matches the existing Python **FastAPI** backend in `raintux/api/rest_api.py`.

---

## What you’re building (summary)

A **local-only** web app (React 18 + TypeScript + Vite) that feels like a **compact desktop utility in the spirit of classic Rainmeter → Manage**: muted grays, left tree + right details, toolbar actions, green “active” dots, and tabs for Manage / Marketplace / About. It talks to RainTux at **`http://127.0.0.1:7272`**, uses **TanStack Query** for HTTP, **Zustand** for UI state, optional **shadcn/ui** + **Tailwind**, and a simple log area (or **xterm.js** later). **No authentication.**

---

## Architecture

```text
┌─────────────────┐     HTTP/WS      ┌──────────────────────────┐
│  Browser (ui)   │ ◄──────────────► │  FastAPI :7272           │
│  Vite dev :5173 │   (or static)    │  GET/POST … + WS /ws     │
└─────────────────┘                  └───────────┬──────────────┘
                                                  │
                                                  ▼
                                       RainTux engine (GTK overlays)
```

- **Development**: run RainTux (`make dev` / `python -m raintux`), then `cd ui && npm run dev`. Set `VITE_API_URL=http://127.0.0.1:7272`.
- **Production (optional later)**: `npm run build` → `ui/dist/`; mount static files from FastAPI for a single origin.

---

## Backend contract (must match)

Base URL: **`http://127.0.0.1:7272`** — override with `VITE_API_URL`.

| Method | Path | Notes |
|--------|------|--------|
| GET | `/skins` | `[{ id, path }]` — `id` is relative, e.g. `Minimal/skin.ini` |
| GET | `/skins/active` | `[{ id, path }]` for loaded skins |
| POST | `/skins/{skin_path:path}/load` | Path may contain `/` — use FastAPI path rules (see `rest_api.py`) |
| POST | `/skins/{skin_path:path}/unload` | Same |
| POST | `/skins/{skin_path:path}/refresh` | Same |
| GET | `/skins/{skin_path:path}/config` | Loaded skin metadata |
| PUT | `/skins/{skin_path:path}/config` | JSON body (may be partial/no-op until engine implements) |
| GET | `/system/status` | `{ compositor, skins_loaded, api: { host, port } }` |
| WS | `/ws` | Accept; append incoming text to a log view |

Encode paths correctly when `id` includes slashes (e.g. `Minimal/skin.ini`).

---

## How it should look

1. **Shell**  
   Top bar: RainTux title, compositor badge from `/system/status`, API host pill.

2. **Tabs**  
   **Manage skins** | **Marketplace** | **About & settings**

3. **Manage skins**  
   - Left (~35%): folder tree of installed skins; leaves = `.ini` files.  
   - **Green dot** if `id` ∈ `/skins/active`.  
   - Toolbar: **Load**, **Unload**, **Refresh**, **Open in editor** (copy path or `xdg-open` when available).  
   - Right: details for selection — `id`, `path`, placeholder thumbnail; author/description if you add parsing later.  
   - **Drag-and-drop reorder**: persist in `localStorage` if backend has no order yet; show a short note.

4. **Skin settings (modal/drawer)**  
   X/Y, monitor, layer, transparency, snap, click-through, keep on screen, load on startup, update rate — bind to `PUT /config` when implemented; disable + tooltip where backend is noop.

5. **Marketplace**  
   Feed URL: `VITE_MARKETPLACE_URL` or `public/marketplace.example.json`. Grid: image, name, author, downloads, **Install** (stub OK until install API exists).

6. **About & settings**  
   Version string, compositor, GNOME extension placeholder, **log viewer** (WS + optional status polling).

7. **Visual style**  
   Rainmeter-ish: background `#2d2d30`, panels `#3e3e42`, accent blue (e.g. `#007acc`), active `#4ec9b0`. Font: **Inter** (web). Dense spacing, small controls.

---

## Recommended folder layout

The Skin Manager should live **directly under** `ui/` at the repo root (not `ui/some-subfolder/`), so `cd ui && npm run dev` works.

```text
ui/
  package.json
  vite.config.ts
  tsconfig.json
  tailwind.config.js
  postcss.config.js
  index.html
  public/
    marketplace.example.json
  src/
    main.tsx
    App.tsx
    index.css
    lib/
      api.ts
      queryClient.ts
      types.ts
      useWebSocket.ts
    components/
      Layout.tsx
      ManageSkins.tsx
      SkinTree.tsx
      SkinDetails.tsx
      Toolbar.tsx
      Marketplace.tsx
      AboutSettings.tsx
      LogViewer.tsx
    store/
      uiStore.ts
```

---

## Copy-paste prompt for an AI / Cursor agent

Paste the block below as the task for generating the full `ui/` tree:

```markdown
You are generating the **RainTux Skin Manager**: a local React + TypeScript + Vite web UI in a new folder `ui/` at the repository root (sibling to `raintux/`).

Constraints:
- React 18, TypeScript, Vite, Tailwind CSS, shadcn/ui (Radix), Zustand, TanStack Query (React Query).
- No authentication. API base URL from `import.meta.env.VITE_API_URL` defaulting to `http://127.0.0.1:7272`.
- Implement screens: Manage Skins (tree + details + toolbar), Marketplace (read JSON feed from `VITE_MARKETPLACE_URL` or `/marketplace.example.json`), About & Settings (version, compositor from `/system/status`, log viewer).
- Manage tab: fetch `GET /skins` and `GET /skins/active`; show green dot for active; buttons call `POST /skins/{path}/load`, `/unload`, `/refresh` with correct path encoding for skin ids that contain slashes. On error show toast or inline error.
- Open WebSocket to `ws://127.0.0.1:7272/ws` (derive host/port from `VITE_API_URL`); append log lines when messages arrive.
- Visual style: dark Rainmeter-like palette (#2d2d30, #3e3e42, accent blue, #4ec9b0 active dot). Compact desktop-tool layout: left tree ~35%, right details, top tabs.
- Drag-and-drop reorder in tree: persist order in localStorage (document that backend may not apply order yet).
- Marketplace “Install” can be stubbed with alert/TODO if no install API exists.
- Add `ui/README.md` with: `npm install`, `npm run dev`, set `VITE_API_URL`, run RainTux backend first.
- Provide working `package.json` scripts: `dev`, `build`, `preview`, and `lint` if ESLint is added.

Output: full file tree with complete source files; avoid empty “TODO” stubs for core UI behavior.

Reference backend: `raintux/api/rest_api.py` and `docs/UI_BUILD_PROMPT.md` in this repo.
```

---

## After you add `ui/`

1. `cd ui && npm install && npm run dev`
2. Start RainTux so `127.0.0.1:7272` is listening.
3. Open the Vite dev URL (typically `http://localhost:5173`).

Optional: add a `Makefile` target `ui-dev` and document mounting `ui/dist` from FastAPI in a later change.
