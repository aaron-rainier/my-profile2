import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

// Remplace `site` par l'URL réelle une fois le site publié : elle sert au
// sitemap, aux URL canoniques et aux aperçus de partage.
export default defineConfig({
  site: "https://exemple-a-remplacer.netlify.app",
  integrations: [sitemap()],
  build: { format: "directory" },
});
