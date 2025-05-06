
#!/bin/bash

echo "⚠️ Automatische Konfliktauflösung mit Bevorzugung von 'ci-setup'-Branch beginnt..."

# Nur für Dateien mit Konflikten
for file in $(git diff --name-only --diff-filter=U); do
  echo "🧩 Behandle Konflikt in: $file"
  # Nimm die Version aus ci-setup (MERGE_HEAD)
  git checkout --theirs -- "$file"
  git add "$file"
done

# Commit der bereinigten Konflikte
git commit -m "Auto-merge conflicts resolved using 'ci-setup' (theirs)"
git push origin main

echo "✅ Konflikte automatisch mit 'ci-setup'-Version aufgelöst und gepusht."
